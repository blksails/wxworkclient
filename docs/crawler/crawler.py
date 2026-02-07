#!/usr/bin/env python3
"""
企业微信 API 文档爬虫
用于爬取企业微信开发者文档中的 API 接口文档，并生成 Markdown 格式的文档
"""

import os
import json
import time
import re
import io
import tempfile
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, asdict
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# LLM 相关导入
try:
    from markitdown import MarkItDown
    from openai import OpenAI
    import httpx
    MARKITDOWN_AVAILABLE = True
except ImportError:
    MARKITDOWN_AVAILABLE = False
    print("⚠️  警告: markitdown 或 openai 未安装，将使用传统的 BeautifulSoup 解析方式")
    print("   安装方法: pip install 'markitdown[all]>=0.1.0' 'openai>=1.0.0'")


class CaptchaDetectedException(Exception):
    """检测到验证码页面的异常"""
    pass


@dataclass
class Parameter:
    """API 参数"""
    name: str
    type: str
    required: bool
    description: str


@dataclass
class Section:
    """文档章节"""
    title: str
    content: str


@dataclass
class CodeExample:
    """代码示例"""
    title: str
    language: str
    code: str


@dataclass
class APIDoc:
    """API 文档"""
    title: str
    url: str
    path: str
    description: str = ""
    method: str = ""
    api_url: str = ""  # API 请求地址
    api_name: str = ""  # API 名称（从 URL 路径提取，如 get_sheet_priv）
    group_title: str = ""  # 分组标题（同一页面中的接口分组）
    request: str = ""
    response: str = ""
    request_params: List[Parameter] = None  # 请求参数
    response_params: List[Parameter] = None  # 响应参数
    query_params: List[Parameter] = None  # Query 参数
    body_params: List[Parameter] = None  # Body 参数
    request_examples: List[CodeExample] = None  # 请求示例
    response_examples: List[CodeExample] = None  # 响应示例
    parameters: List[Parameter] = None  # 通用参数
    sections: List[Section] = None

    def __post_init__(self):
        if self.request_params is None:
            self.request_params = []
        if self.response_params is None:
            self.response_params = []
        if self.query_params is None:
            self.query_params = []
        if self.body_params is None:
            self.body_params = []
        if self.request_examples is None:
            self.request_examples = []
        if self.response_examples is None:
            self.response_examples = []
        if self.parameters is None:
            self.parameters = []
        if self.sections is None:
            self.sections = []


class WeChatWorkAPICrawler:
    """企业微信 API 文档爬虫"""
    
    def __init__(self, base_url: str, start_path: str, output_dir: str, resume: bool = True, doc_ids: List[str] = None, split_multi_api: bool = False, use_llm_extraction: bool = True, llm_model: str = "gpt-3.5-turbo", fallback_to_bs4: bool = False, route_filter: List[str] = None, route_exclude: List[str] = None):
        self.base_url = base_url
        self.start_url = urljoin(base_url, start_path)
        self.output_dir = Path(output_dir)
        self.visited = set()
        self.api_docs = []
        self.resume = resume
        self.queue = []  # 待爬取的 URL 队列
        self.doc_ids = doc_ids  # 指定要爬取的文档 ID 列表
        self.split_multi_api = split_multi_api  # 是否分割多接口页面（已弃用，由 LLM 自动处理）
        self.failed_docs = []  # 记录失败的文档 ID 和错误信息
        self.route_filter = route_filter or []  # 路由过滤器数组，必须包含所有关键词才通过 - AND 逻辑（如 ["第三方应用开发", "服务端API"]）
        self.route_exclude = route_exclude or []  # 路由排除器数组，包含任意一个就排除 - OR 逻辑（如 ["服务商代开发"]）
        
        # LLM 提取配置
        self.use_llm_extraction = use_llm_extraction and MARKITDOWN_AVAILABLE
        self.llm_model = llm_model
        self.fallback_to_bs4 = fallback_to_bs4
        
        # 初始化 MarkItDown 和 OpenAI 客户端
        if self.use_llm_extraction:
            try:
                self.markitdown = MarkItDown()
                self.openai_client = OpenAI()  # 从环境变量 OPENAI_API_KEY 读取
                print(f"✓ LLM 提取模式已启用 (模型: {self.llm_model})")
                    
            except Exception as e:
                print(f"⚠️  警告: LLM 初始化失败: {e}")
                if not self.fallback_to_bs4:
                    raise
                print("   将使用传统的 BeautifulSoup 解析方式")
                self.use_llm_extraction = False
        else:
            self.markitdown = None
            self.openai_client = None
            if not MARKITDOWN_AVAILABLE:
                print("ℹ️  使用传统的 BeautifulSoup 解析方式")

        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 配置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # 加载已爬取的 URL 和待爬取队列（用于断点续爬）
        if resume:
            self._load_visited_urls()
            self._load_queue()
        
        # 如果指定了文档 ID，只爬取这些文档
        if self.doc_ids:
            print(f"指定爬取 {len(self.doc_ids)} 个文档: {', '.join(self.doc_ids)}")
            self.queue = [urljoin(base_url, f'/document/path/{doc_id}') for doc_id in self.doc_ids]
            self.need_rescan = False
        # 如果队列为空，需要重新扫描已访问的页面来发现新链接
        elif not self.queue:
            if self.visited and resume:
                print(f"队列为空但有 {len(self.visited)} 个已访问页面")
                print("将重新扫描部分页面来发现未爬取的链接...")
                self.need_rescan = True
                # 添加起始 URL 用于重新扫描
                self.queue.append(self.start_url)
            else:
                # 首次运行，正常添加起始 URL
                self.queue.append(self.start_url)
                self.need_rescan = False
        else:
            self.need_rescan = False
        
    def crawl(self):
        """开始爬取（使用 BFS 队列）"""
        print("开始爬取企业微信 API 文档...")
        print(f"输出目录: {self.output_dir}")
        if self.resume and self.visited:
            print(f"断点续爬模式: 已访问 {len(self.visited)} 个页面，队列中还有 {len(self.queue)} 个待爬取")
        print()
        
        try:
            # 使用 BFS 队列方式爬取
            while self.queue:
                url = self.queue.pop(0)  # 从队列头部取出
                self._crawl_page(url)
                
                # 定期保存队列状态（每10个页面）
                if len(self.visited) % 10 == 0:
                    self._save_queue()
            
            print(f"\n共爬取 {len(self.api_docs)} 个 API 文档")
            
            # 最后生成总索引和完整 JSON
            self._save_to_json()
            self._save_visited_urls()
            self._save_queue()
            self._generate_index()
            self._save_failed_docs()  # 保存失败的文档列表
            
            print("\n爬取完成！")
            
            # 显示失败统计
            if self.failed_docs:
                print(f"\n⚠️  {len(self.failed_docs)} 个文档处理失败，详见 .failed_docs.json")
            
        except CaptchaDetectedException as e:
            # 验证码检测异常，已在 _crawl_page 中处理，直接返回
            pass
        except KeyboardInterrupt:
            print("\n\n" + "=" * 60)
            print("⚠️  用户中断爬取")
            print("=" * 60)
            print()
            print("正在保存当前进度...")
            
            # 保存当前进度
            self._save_to_json()
            self._save_visited_urls()
            self._save_queue()
            self._generate_index()
            
            print(f"\n✓ 进度已保存")
            print(f"  - 已爬取: {len(self.api_docs)} 个 API 文档")
            print(f"  - 已访问: {len(self.visited)} 个页面")
            print(f"  - 队列剩余: {len(self.queue)} 个待爬取")
            print(f"  - 输出目录: {self.output_dir}")
            if self.failed_docs:
                print(f"  - 失败文档: {len(self.failed_docs)} 个（见 .failed_docs.json）")
            print()
            print("重新运行命令继续爬取：")
            print("  python3 crawler.py")
            print("=" * 60)
            raise
        
    def _crawl_page(self, url: str):
        """爬取单个页面（BFS 方式）"""
        # 检查是否已访问
        already_visited = url in self.visited
        
        # 如果已访问但需要重新扫描链接
        if already_visited and not self.need_rescan:
            return
        
        if already_visited:
            print(f"重新扫描链接: {url}")
        else:
            self.visited.add(url)
            print(f"正在爬取: {url}")
        
        try:
            # 延迟请求，避免给服务器造成压力
            if not already_visited:
                time.sleep(2)
            else:
                time.sleep(0.5)  # 重新扫描时使用更短的延迟
            
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 检查路由过滤器（在处理文档之前）
            if (self.route_filter or self.route_exclude) and not already_visited:
                route_path = self._extract_route_path(soup)
                if route_path:
                    print(f"  → 路由: {' > '.join(route_path)}")
                    
                    # 检查包含过滤器（数组匹配：必须包含所有关键词才通过 - AND 逻辑）
                    if self.route_filter:
                        matched = all(filter_keyword in route_path for filter_keyword in self.route_filter)
                        if not matched:
                            missing = [f for f in self.route_filter if f not in route_path]
                            print(f"  ⊗ 跳过: 缺少必需的路由关键词 {missing}")
                            return
                    
                    # 检查排除过滤器（数组匹配：包含任意一个就排除 - OR 逻辑）
                    if self.route_exclude:
                        for exclude_keyword in self.route_exclude:
                            if exclude_keyword in route_path:
                                print(f"  ⊗ 跳过: 包含已排除的 '{exclude_keyword}' 路由")
                                return
                else:
                    print(f"  ⚠️  未找到路由信息")
                    # 如果设置了过滤器但没找到路由，跳过
                    if self.route_filter or self.route_exclude:
                        print(f"  ⊗ 跳过: 无法确定路由")
                        return
            
            # 检测反爬虫验证码页面
            if self._check_captcha_page(soup):
                print("\n" + "=" * 60)
                print("⚠️  检测到反爬虫验证码页面")
                print("=" * 60)
                print("页面标题: 企业微信-验证码")
                print(f"触发 URL: {url}")
                print()
                print("正在保存当前进度...")
                
                # 保存当前进度
                self._save_to_json()
                self._save_visited_urls()
                self._save_queue()
                self._generate_index()
                
                print(f"\n✓ 进度已保存")
                print(f"  - 已爬取: {len(self.api_docs)} 个 API 文档")
                print(f"  - 已访问: {len(self.visited)} 个页面")
                print(f"  - 队列剩余: {len(self.queue)} 个待爬取")
                print(f"  - 输出目录: {self.output_dir}")
                print()
                print("💡 建议操作：")
                print("  1. 等待一段时间后重新运行（建议 30 分钟以上）")
                print("  2. 更换 IP 地址或使用代理")
                print("  3. 增加请求延迟时间")
                print("  4. 使用浏览器手动完成验证后再继续")
                print()
                print("重新运行命令继续爬取：")
                print("  python3 crawler.py")
                print("=" * 60)
                
                # 抛出特殊异常，停止爬取
                raise CaptchaDetectedException("检测到验证码页面，已停止爬取")
            
            # 提取 API 文档（仅未访问的页面）
            if not already_visited:
                try:
                    api_doc = self._extract_api_doc(soup, url)
                    if api_doc:
                        self.api_docs.append(api_doc)
                        print(f"  ✓ 提取文档: {api_doc.title}")
                        
                        # 立即保存 Markdown 文件
                        self._save_single_markdown(api_doc)
                        
                        # 更新索引文件
                        self._update_index()
                except Exception as e:
                    # 记录失败的文档
                    doc_id_match = re.search(r'/document/path/(\d+)', url)
                    doc_id = doc_id_match.group(1) if doc_id_match else url
                    
                    error_info = {
                        'doc_id': doc_id,
                        'url': url,
                        'error': str(e),
                        'error_type': type(e).__name__,
                        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    self.failed_docs.append(error_info)
                    
                    print(f"  ✗ 文档处理失败 (ID: {doc_id}): {e}")
                    
                    # 保存失败列表
                    self._save_failed_docs()
                    
                    # 如果设置了严格模式，则抛出异常
                    if not self.fallback_to_bs4:  # 使用这个标志作为严格模式
                        raise
            
            # 查找相关链接并加入队列（除非指定了文档 ID）
            if not self.doc_ids:
                new_links_count = 0
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    
                    # 只爬取文档页面
                    if '/document/path/' in href:
                        full_url = urljoin(self.base_url, href)
                        
                        # 限制在同一域名下，且未访问过，且不在队列中
                        if (urlparse(full_url).netloc == urlparse(self.base_url).netloc and
                            full_url not in self.visited and
                            full_url not in self.queue):
                            self.queue.append(full_url)
                            new_links_count += 1
                
                if already_visited and new_links_count > 0:
                    print(f"  ✓ 发现 {new_links_count} 个新链接")
                    self.need_rescan = False  # 发现新链接后，关闭重新扫描模式
                        
        except CaptchaDetectedException:
            # 重新抛出，让上层处理
            raise
        except Exception as e:
            print(f"  ✗ 爬取失败: {e}")
    
    def _create_extraction_prompt(self) -> str:
        """创建用于 LLM 提取的 system prompt"""
        return """你是一个专业的 API 文档解析专家，负责从企业微信 API 文档的 Markdown 格式中提取结构化信息。

**任务**：
分析给定的 Markdown 文档，提取所有 API 接口的结构化信息。

**重要规则**：
1. **⭐ 自动识别多个 API（关键）**：
   - 仔细查看文档中是否包含多个不同的"请求地址"或"接口地址"
   - 如果找到多个不同的 URL（即使在同一个页面），每个 URL 对应一个独立的 API
   - 常见模式：
     - "请求方式：POST（HTTPS）请求地址：https://..."
     - "接口地址：https://..."
     - 标题如："设置XXX" 和 "获取XXX" 通常是两个不同的 API
   - 即使标题相似，只要请求地址不同，就是不同的 API
   - 每个 API 应该有自己的请求参数、响应参数和示例
2. **⭐ 必须提取 api_name**：从每个 API 的接口地址 URL 路径中提取 API 名称（最后一部分，不含 query 参数）
   例如：`https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/add_field_group?access_token=TOKEN` → `add_field_group`
3. **智能内容归属**：每段描述、参数、示例都要判断属于哪个 API（通过上下文语义）
4. **处理共享内容**：页面开头的通用说明可以包含在每个 API 的描述中
5. **⭐ 参数分类（关键）**：
   - query_params: **必须从 API URL 中提取** ? 后的参数（如 access_token, suite_access_token）
     - 例如 URL `https://qyapi.weixin.qq.com/cgi-bin/service/v2/get_auth_info?suite_access_token=SUITE_ACCESS_TOKEN`
     - 必须提取 query_params: [{"name": "suite_access_token", "type": "string", "required": true, "description": "第三方应用凭证"}]
   - body_params: 请求体中的参数（通常是 JSON 中的字段）
   - response_params: 响应中的参数
6. **⭐ 嵌套字段处理**（重要）：
   - 对于 object 和 array 类型，必须展开内部字段
   - 使用点号表示法表示嵌套关系：
     - `rule_list[].rule_id` 表示数组中对象的 rule_id 字段
     - `record_priv.record_range_type` 表示对象的嵌套字段
   - 示例：如果响应示例中有 `{"rule_list": [{"rule_id": 1, "name": "全员"}]}`
     则应提取：
     - `rule_list` (array) - 权限列表
     - `rule_list[].rule_id` (int) - 规则ID
     - `rule_list[].name` (string) - 规则名称
7. **代码示例语言识别**：
   - 包含 { } 或 [ ] 的是 json
   - 包含 <xml> 的是 xml
   - 包含 curl 的是 bash
   - 其他是 text

**输出格式**（严格的 JSON）：
```json
{
  "page_title": "页面标题",
  "apis": [
    {
      "group_title": "API 功能名称（如：添加编组）",
      "api_name": "从 URL 提取的 API 名称（如：add_field_group）",
      "method": "HTTP 方法（GET/POST/PUT/DELETE）",
      "api_url": "完整的 API 地址",
      "description": "API 描述",
      "query_params": [
        {
          "name": "参数名",
          "type": "类型（string/int32/uint32/bool）",
          "required": true,
          "description": "说明"
        }
      ],
      "body_params": [
        {
          "name": "参数名（使用点号表示嵌套，如 items[].id）",
          "type": "类型（string/int32/uint32/bool/object/array/object[]）",
          "required": true,
          "description": "说明"
        }
      ],
      "response_params": [
        {
          "name": "参数名（使用点号表示嵌套，如 rule_list[].rule_id）",
          "type": "类型（string/int32/uint32/bool/object/array/object[]）",
          "required": false,
          "description": "说明"
        }
      ],
      "request_examples": [
        {
          "title": "示例标题",
          "language": "json/xml/bash/text",
          "code": "代码内容"
        }
      ],
      "response_examples": [
        {
          "title": "示例标题",
          "language": "json/xml/bash/text",
          "code": "代码内容"
        }
      ],
      "sections": [
        {
          "title": "章节标题",
          "content": "章节内容"
        }
      ]
    }
  ]
}
```

**注意事项**：
- 必须返回有效的 JSON 格式
- api_name 字段必填且必须从 URL 中提取
- 如果只有一个 API，apis 数组也只包含一个元素
- 参数的 type 应该是具体类型（string/int32/uint32/bool/object/array/object[]），而不是"是"或"否"
- required 字段应该是 boolean 值（true/false）
- **⭐ 必须展开嵌套字段**：对于 object 和 array 类型，不要只列出顶层字段，要列出所有嵌套字段
- 嵌套字段使用点号表示法：`parent[].child` 或 `parent.child`
- 代码示例要保留完整内容，不要截断

**示例 1 - 多个 API 识别**：
如果文档包含：

```
# 设置日志打印级别

请求方式：POST（HTTPS）
请求地址：https://qyapi.weixin.qq.com/cgi-bin/chatdata/set_log_level?access_token=ACCESS_TOKEN

...（set_log_level 的参数和示例）

# 获取当前日志打印级别

请求方式：POST（HTTPS）
请求地址：https://qyapi.weixin.qq.com/cgi-bin/chatdata/get_log_level?access_token=ACCESS_TOKEN

...（get_log_level 的参数和示例）
```

应该识别为 **2 个 API**：
- API 1: set_log_level
- API 2: get_log_level

**示例 2 - 嵌套字段展开**：
如果响应示例是：
```json
{
  "rule_list": [{
    "rule_id": 1,
    "priv_list": [{"sheet_id": "abc", "priv": 2}]
  }]
}
```

response_params 应该包含：
- errcode (int32) - 错误码
- errmsg (string) - 错误信息
- rule_list (object[]) - 权限列表
- rule_list[].rule_id (int32) - 规则ID
- rule_list[].priv_list (object[]) - 权限详情列表
- rule_list[].priv_list[].sheet_id (string) - 子表ID
- rule_list[].priv_list[].priv (int32) - 权限级别
"""
    
    def _json_to_apidoc(self, api_data: Dict, url: str, path: str) -> APIDoc:
        """将 JSON 数据转换为 APIDoc 对象"""
        # 创建 APIDoc 对象
        api_doc = APIDoc(
            title=api_data.get('group_title', ''),
            url=url,
            path=path,
            description=api_data.get('description', ''),
            method=api_data.get('method', ''),
            api_url=api_data.get('api_url', ''),
            api_name=api_data.get('api_name', ''),
            group_title=api_data.get('group_title', '')
        )
        
        # 转换 query 参数
        for param_data in api_data.get('query_params', []):
            param = Parameter(
                name=param_data.get('name', ''),
                type=param_data.get('type', 'string'),
                required=param_data.get('required', False),
                description=param_data.get('description', '')
            )
            api_doc.query_params.append(param)
        
        # 后处理：确保从 API URL 中提取 query 参数（如果 LLM 没有正确提取）
        if api_doc.api_url:
            self._ensure_query_params_from_url(api_doc)
        
        # 转换 body 参数
        for param_data in api_data.get('body_params', []):
            param = Parameter(
                name=param_data.get('name', ''),
                type=param_data.get('type', 'string'),
                required=param_data.get('required', False),
                description=param_data.get('description', '')
            )
            api_doc.body_params.append(param)
        
        # 转换响应参数
        for param_data in api_data.get('response_params', []):
            param = Parameter(
                name=param_data.get('name', ''),
                type=param_data.get('type', 'string'),
                required=False,  # 响应参数通常不标记必填
                description=param_data.get('description', '')
            )
            api_doc.response_params.append(param)
        
        # 转换请求示例
        for example_data in api_data.get('request_examples', []):
            example = CodeExample(
                title=example_data.get('title', ''),
                language=example_data.get('language', 'text'),
                code=example_data.get('code', '')
            )
            api_doc.request_examples.append(example)
        
        # 转换响应示例
        for example_data in api_data.get('response_examples', []):
            example = CodeExample(
                title=example_data.get('title', ''),
                language=example_data.get('language', 'text'),
                code=example_data.get('code', '')
            )
            api_doc.response_examples.append(example)
        
        # 转换章节
        for section_data in api_data.get('sections', []):
            section = Section(
                title=section_data.get('title', ''),
                content=section_data.get('content', '')
            )
            api_doc.sections.append(section)
        
        return api_doc
    
    def _extract_api_doc_with_llm(self, soup: BeautifulSoup, url: str) -> Optional[APIDoc]:
        """使用 LLM 提取 API 文档信息"""
        try:
            # 提取标题和路径 ID
            title = ""
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text(strip=True)
            else:
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
            
            if not title:
                return None
            
            path_match = re.search(r'/document/path/(\d+)', url)
            path = path_match.group(1) if path_match else ""
            
            # 步骤 1: 提取核心内容区域（排除 sidebar、nav 等）
            content_area = soup.find(class_='ep-layout-cnt')
            if content_area:
                # 找到了核心内容区域，只转换这部分
                html_content = str(content_area)
                print(f"    → 提取核心内容区域 (.ep-layout-cnt)")
            else:
                # 未找到核心内容区域，使用整个页面
                html_content = str(soup)
                print(f"    ⚠ 未找到 .ep-layout-cnt，使用完整页面")
            
            # 步骤 2: 将 HTML 转换为 Markdown
            # MarkItDown 需要文件扩展名来识别格式，所以创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(html_content)
                temp_path = temp_file.name
            
            try:
                md_result = self.markitdown.convert(temp_path)
                markdown_text = md_result.text_content
            finally:
                # 删除临时文件
                try:
                    os.unlink(temp_path)
                except:
                    pass
            
            # 步骤 3: 调用 GPT-3.5 提取结构化信息
            print(f"    → 使用 LLM 提取结构化信息...")
            
            completion = self.openai_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": self._create_extraction_prompt()},
                    {"role": "user", "content": markdown_text}
                ],
                response_format={"type": "json_object"},
                temperature=0.1  # 低温度确保一致性
            )
            
            # 步骤 4: 解析 LLM 响应
            response_text = completion.choices[0].message.content
            api_data = json.loads(response_text)
            
            # 记录 token 使用情况
            usage = completion.usage
            print(f"    → Token 使用: {usage.prompt_tokens} + {usage.completion_tokens} = {usage.total_tokens}")
            
            # 保存 LLM 生成的 JSON 文件
            json_file = self.output_dir / f"{path}_llm.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(api_data, f, ensure_ascii=False, indent=2)
            print(f"    → 已保存 LLM JSON: {json_file.name}")
            
            # 步骤 5: 处理响应
            apis = api_data.get('apis', [])
            
            # 调试输出：显示识别到的 API 列表
            if apis:
                print(f"    → LLM 识别到 {len(apis)} 个 API:")
                for i, api in enumerate(apis, 1):
                    api_name = api.get('api_name', '未知')
                    api_title = api.get('group_title', api.get('title', '未命名'))
                    print(f"       {i}. {api_title} ({api_name})")
            
            if not apis:
                print(f"    ⚠ 警告: LLM 未提取到任何 API")
                return None
            
            if len(apis) > 1:
                # 多个 API，分别处理
                print(f"    → 检测到 {len(apis)} 个独立的 API 接口")
                for i, api_info in enumerate(apis, 1):
                    api_doc = self._json_to_apidoc(api_info, url, path)
                    self.api_docs.append(api_doc)
                    
                    # 保存单个 API 的 JSON
                    api_json_file = self.output_dir / f"{path}-{i}-{api_doc.api_name}.json"
                    with open(api_json_file, 'w', encoding='utf-8') as f:
                        json.dump(api_info, f, ensure_ascii=False, indent=2)
                    
                    # 立即保存 Markdown 文件
                    self._save_single_markdown_grouped(api_doc, i, len(apis))
                    
                    print(f"    ✓ 提取接口 {i}/{len(apis)}: {api_doc.group_title or api_doc.title}")
                
                # 删除可能存在的总文档（旧的 BS4 方式生成的）
                old_total_file = self.output_dir / f"{path}-6.md"
                if old_total_file.exists():
                    try:
                        old_total_file.unlink()
                        print(f"    → 已删除旧的总文档: {old_total_file.name}")
                    except:
                        pass
                
                # 返回 None 表示已自行处理，不需要调用处再保存总文档
                return None
            else:
                # 单个 API，JSON 已经在前面保存了
                api_doc = self._json_to_apidoc(apis[0], url, path)
                return api_doc
                
        except Exception as e:
            print(f"    ✗ LLM 提取失败: {e}")
            # 不允许回退到 BS4，直接抛出异常
            raise
            
    def _extract_api_doc(self, soup: BeautifulSoup, url: str) -> Optional[APIDoc]:
        """从页面中提取 API 文档信息，可能返回多个接口
        
        必须使用 LLM 提取，不再支持 BeautifulSoup 方式
        """
        # 如果启用了 LLM 提取，使用 LLM 方式
        if self.use_llm_extraction:
            return self._extract_api_doc_with_llm(soup, url)
        else:
            # 未启用 LLM 提取，报错
            raise RuntimeError("LLM 提取模式未启用，无法解析文档。请设置 OPENAI_API_KEY 环境变量。")
    
    # 以下为旧的 BeautifulSoup 解析方法，仅作为备用参考
    def _extract_api_doc_bs4_legacy(self, soup: BeautifulSoup, url: str) -> Optional[APIDoc]:
        title = ""
        h1 = soup.find('h1')
        if h1:
            title = h1.get_text(strip=True)
        else:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)
        
        if not title:
            return None
        
        # 提取路径 ID
        path_match = re.search(r'/document/path/(\d+)', url)
        path = path_match.group(1) if path_match else ""
        
        # 检查是否包含多个接口（仅在启用分割时）
        api_groups = []
        if self.split_multi_api:
            api_groups = self._detect_multiple_apis(soup)
        
        if len(api_groups) > 1:
            # 页面包含多个接口，分别处理
            print(f"    → 检测到 {len(api_groups)} 个独立的 API 接口")
            for i, group in enumerate(api_groups, 1):
                api_doc = APIDoc(
                    title=title,
                    url=url,
                    path=path,
                    group_title=group.get('title', ''),
                    api_url=group.get('api_url', ''),
                    method=group.get('method', '')
                )
                
                # 从 API URL 提取 API 名称
                if api_doc.api_url:
                    api_doc.api_name = self._extract_api_name_from_url(api_doc.api_url)
                
                # 提取该接口的内容区域（从标题到下一个标题之间）
                heading_element = group.get('heading_element')
                if heading_element:
                    group_soup = self._extract_section_for_api(soup, heading_element)
                    
                    # 提取描述
                    first_p = group_soup.find('p')
                    if first_p:
                        api_doc.description = first_p.get_text(strip=True)
                    
                    # 提取代码示例
                    self._extract_code_examples(group_soup, api_doc)
                    
                    # 提取章节
                    self._extract_sections(group_soup, api_doc)
                    
                    # 提取参数表格
                    self._extract_parameters(group_soup, api_doc)
                    
                    # 提取 query 参数
                    if api_doc.api_url:
                        self._extract_query_params_from_url(api_doc)
                
                self.api_docs.append(api_doc)
                
                # 立即保存 Markdown 文件
                self._save_single_markdown_grouped(api_doc, i, len(api_groups))
            
            # 返回 None 表示已经自己处理了
            return None
        else:
            # 单个接口，使用原有逻辑
            api_doc = APIDoc(title=title, url=url, path=path)
            
            # 提取描述（通常是第一个段落）
            first_p = soup.find('p')
            if first_p:
                api_doc.description = first_p.get_text(strip=True)
            
            # 提取 HTTP 方法和请求 URL
            self._extract_http_info(soup, api_doc)
            
            # 从 API URL 提取 API 名称
            if api_doc.api_url:
                api_doc.api_name = self._extract_api_name_from_url(api_doc.api_url)
            
            # 提取代码示例
            self._extract_code_examples(soup, api_doc)
            
            # 提取章节
            self._extract_sections(soup, api_doc)
            
            # 提取参数表格
            self._extract_parameters(soup, api_doc)
            
            return api_doc
    
    def _detect_multiple_apis(self, soup: BeautifulSoup) -> List[Dict]:
        """检测页面中是否包含多个 API 接口
        
        返回格式：[
            {
                'title': 'API 标题',
                'api_url': 'https://...',
                'method': 'POST',
                'heading_element': BeautifulSoup 标题元素
            },
            ...
        ]
        """
        api_groups = []
        
        # 查找所有 h3 或 h4 标题
        headings = soup.find_all(['h3', 'h4'])
        
        for heading in headings:
            # 获取标题后的内容区域
            heading_text = heading.get_text(strip=True)
            
            # 查找标题后的内容中是否包含"请求方式：POST（HTTPS）请求地址:"模式
            content_after = []
            for sibling in heading.find_next_siblings():
                if sibling.name in ['h2', 'h3', 'h4']:
                    break
                content_after.append(sibling)
            
            # 在这些内容中查找 API URL 和方法
            section_text = ' '.join([elem.get_text() for elem in content_after])
            
            # 模式：请求方式：POST（HTTPS）请求地址: https://...
            pattern = r'请求方式[：:]\s*(GET|POST|PUT|DELETE)\s*[（(]HTTPS[）)]\s*请求地址\s*[：:]\s*(https://qyapi\.weixin\.qq\.com[^\s\n]*)'
            match = re.search(pattern, section_text, re.IGNORECASE)
            
            if match:
                method = match.group(1).upper()
                api_url = match.group(2).strip()
                
                api_groups.append({
                    'title': heading_text,
                    'api_url': api_url,
                    'method': method,
                    'heading_element': heading
                })
        
        if len(api_groups) <= 1:
            # 只有一个或没有，返回空表示不需要分组
            return []
        
        return api_groups
    
    def _extract_section_for_api(self, soup: BeautifulSoup, heading_element) -> BeautifulSoup:
        """为特定 API 提取相关的内容区域（从标题到下一个同级标题之间的内容）"""
        # 创建一个新的 soup 对象，只包含该接口的内容
        from bs4 import BeautifulSoup as BS
        
        section_html = []
        
        # 收集标题后的所有内容，直到遇到下一个同级标题
        for sibling in heading_element.find_next_siblings():
            if sibling.name in ['h2', 'h3', 'h4']:
                # 遇到下一个标题，停止
                break
            section_html.append(str(sibling))
        
        # 创建新的 soup 对象
        combined_html = ''.join(section_html)
        return BS(combined_html, 'html.parser')
    
    def _extract_api_name_from_url(self, api_url: str) -> str:
        """从 API URL 中提取 API 名称
        
        例如：
        - https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/get_sheet_priv?access_token=TOKEN
        - 提取：get_sheet_priv
        """
        try:
            from urllib.parse import urlparse
            parsed = urlparse(api_url)
            path_parts = parsed.path.strip('/').split('/')
            
            # 取最后一个部分作为 API 名称
            if path_parts:
                api_name = path_parts[-1]
                # 移除查询参数
                if '?' in api_name:
                    api_name = api_name.split('?')[0]
                return api_name
        except:
            pass
        
        return ""
    
    def _extract_http_info(self, soup: BeautifulSoup, api_doc: APIDoc):
        """提取 HTTP 信息（方法、URL等）"""
        # 1. 尝试从 strong 标签中提取（企业微信文档常用格式）
        for strong in soup.find_all('strong'):
            strong_text = strong.get_text(strip=True)
            
            # 提取请求方式
            if '请求方式' in strong_text:
                # 获取后面的文本
                next_text = ''
                for sibling in strong.next_siblings:
                    if isinstance(sibling, str):
                        next_text += sibling
                    elif sibling.name:
                        next_text += sibling.get_text()
                        if sibling.name in ['p', 'br', 'div']:
                            break
                    if len(next_text) > 50:
                        break
                
                # 提取 HTTP 方法
                if 'POST' in next_text.upper():
                    api_doc.method = 'POST'
                elif 'GET' in next_text.upper():
                    api_doc.method = 'GET'
                elif 'PUT' in next_text.upper():
                    api_doc.method = 'PUT'
                elif 'DELETE' in next_text.upper():
                    api_doc.method = 'DELETE'
            
            # 提取请求地址
            if '请求地址' in strong_text:
                # 获取后面的文本
                next_text = ''
                for sibling in strong.next_siblings:
                    if isinstance(sibling, str):
                        next_text += sibling
                    elif sibling.name:
                        next_text += sibling.get_text()
                        if sibling.name in ['p', 'br', 'div', 'strong']:
                            break
                    if len(next_text) > 200:
                        break
                
                # 提取 URL
                url_match = re.search(r'https://qyapi\.weixin\.qq\.com[^\s\n<>]*', next_text)
                if url_match:
                    api_doc.api_url = url_match.group(0).strip()
        
        # 2. 查找所有的 code 和 pre 标签
        for code_tag in soup.find_all(['code', 'pre']):
            text = code_tag.get_text()
            
            # 查找 API URL
            if 'https://qyapi.weixin.qq.com' in text:
                # 如果还没有方法，提取 HTTP 方法
                if not api_doc.method:
                    if 'POST' in text.upper():
                        api_doc.method = 'POST'
                    elif 'GET' in text.upper():
                        api_doc.method = 'GET'
                    elif 'PUT' in text.upper():
                        api_doc.method = 'PUT'
                    elif 'DELETE' in text.upper():
                        api_doc.method = 'DELETE'
                
                # 如果还没有 URL，提取 API URL
                if not api_doc.api_url:
                    url_match = re.search(r'https://qyapi\.weixin\.qq\.com[^\s\n<>]*', text)
                    if url_match:
                        api_doc.api_url = url_match.group(0)
                
                # 保存完整请求示例
                if not api_doc.request:
                    api_doc.request = text.strip()
        
        # 3. 如果还没找到，尝试从整个页面文本中提取
        if not api_doc.api_url or not api_doc.method:
            page_text = soup.get_text()
            
            # 尝试匹配 "请求方式： POST" 格式
            if not api_doc.method:
                method_match = re.search(r'请求方式[：:]\s*(GET|POST|PUT|DELETE)', page_text, re.IGNORECASE)
                if method_match:
                    api_doc.method = method_match.group(1).upper()
            
            # 尝试匹配 "请求地址： https://..." 格式
            if not api_doc.api_url:
                url_match = re.search(r'请求地址[：:]\s*(https://qyapi\.weixin\.qq\.com[^\s\n]*)', page_text)
                if url_match:
                    api_doc.api_url = url_match.group(1)
            
            # 尝试匹配 "GET https://..." 或 "POST https://..." 格式
            if not api_doc.api_url or not api_doc.method:
                http_match = re.search(r'(GET|POST|PUT|DELETE)\s+(https://qyapi\.weixin\.qq\.com[^\s\n]*)', page_text)
                if http_match:
                    if not api_doc.method:
                        api_doc.method = http_match.group(1)
                    if not api_doc.api_url:
                        api_doc.api_url = http_match.group(2)
        
        # 4. 提取 URL 中的 query 参数
        if api_doc.api_url:
            self._extract_query_params_from_url(api_doc)
    
    def _ensure_query_params_from_url(self, api_doc: APIDoc):
        """确保从 URL 中提取 query 参数（LLM 后处理）
        
        这个方法在 LLM 提取后调用，确保 URL 中的 query 参数被正确提取。
        """
        from urllib.parse import urlparse
        
        try:
            parsed_url = urlparse(api_doc.api_url)
            
            # 解析 query 字符串
            if parsed_url.query:
                # 手动解析 query 参数，因为参数值可能是占位符（如 SUITE_ACCESS_TOKEN）
                query_parts = parsed_url.query.split('&')
                extracted_count = 0
                
                for part in query_parts:
                    if '=' in part:
                        key, value = part.split('=', 1)
                        
                        # 检查是否已经存在相同名称的参数
                        existing_names = {p.name for p in api_doc.query_params}
                        if key not in existing_names:
                            # 推测参数类型和描述
                            param_type = self._infer_query_param_type(key, value)
                            description = self._infer_query_param_description(key, value)
                            
                            # 创建 query 参数
                            param = Parameter(
                                name=key,
                                type=param_type,
                                required=True,  # URL 中的参数通常是必填的
                                description=description
                            )
                            
                            api_doc.query_params.append(param)
                            extracted_count += 1
                
                if extracted_count > 0:
                    print(f"    → 补充从 URL 提取的 {extracted_count} 个 Query 参数: {[p.name for p in api_doc.query_params[-extracted_count:]]}")
        
        except Exception as e:
            print(f"    ⚠ 解析 URL query 参数时出错: {e}")
    
    def _infer_query_param_description(self, key: str, value: str) -> str:
        """推测 query 参数的描述"""
        key_lower = key.lower()
        
        # 常见的 token 参数描述
        token_descriptions = {
            'access_token': '调用接口凭证',
            'suite_access_token': '第三方应用凭证',
            'provider_access_token': '服务商凭证',
            'corpid': '企业ID',
            'agentid': '应用ID',
            'userid': '成员ID',
            'cursor': '分页游标',
            'limit': '分页大小',
        }
        
        if key_lower in token_descriptions:
            return token_descriptions[key_lower]
        
        # 根据值推测
        if 'TOKEN' in value.upper():
            return '调用接口凭证'
        
        return f"Query参数"
    
    def _extract_query_params_from_url(self, api_doc: APIDoc):
        """从 URL 中提取 query 参数"""
        from urllib.parse import urlparse, parse_qs
        
        try:
            parsed_url = urlparse(api_doc.api_url)
            
            # 解析 query 字符串
            if parsed_url.query:
                # 手动解析 query 参数，因为参数值可能是占位符（如 SUITE_ACCESS_TOKEN）
                query_parts = parsed_url.query.split('&')
                extracted_count = 0
                
                for part in query_parts:
                    if '=' in part:
                        key, value = part.split('=', 1)
                        
                        # 检查是否已经存在相同名称的参数
                        existing_names = {p.name for p in api_doc.query_params}
                        if key not in existing_names:
                            # 推测参数类型
                            param_type = self._infer_query_param_type(key, value)
                            
                            # 创建 query 参数
                            param = Parameter(
                                name=key,
                                type=param_type,
                                required=True,  # URL 中的参数通常是必填的
                                description=f"Query参数，示例值: {value}"
                            )
                            
                            api_doc.query_params.append(param)
                            extracted_count += 1
                
                if extracted_count > 0:
                    print(f"    → 从请求地址中提取了 {extracted_count} 个 Query 参数")
        
        except Exception as e:
            print(f"    ⚠ 解析 URL query 参数时出错: {e}")
    
    def _infer_query_param_type(self, key: str, value: str) -> str:
        """推测 query 参数的类型"""
        # 根据参数名推测类型
        key_lower = key.lower()
        
        # 常见的 token 类型参数
        if 'token' in key_lower or 'key' in key_lower or 'secret' in key_lower:
            return 'string'
        
        # 常见的 ID 类型参数
        if key_lower.endswith('id') or key_lower.startswith('id'):
            return 'string'
        
        # 常见的数字类型参数
        if any(keyword in key_lower for keyword in ['limit', 'offset', 'page', 'size', 'count', 'num']):
            return 'int'
        
        # 根据值推测类型
        if value.isdigit():
            return 'int'
        
        # 检查是否是布尔值
        if value.lower() in ['true', 'false', '0', '1']:
            return 'bool'
        
        # 默认为字符串
        return 'string'
    
    def _extract_code_examples(self, soup: BeautifulSoup, api_doc: APIDoc):
        """提取代码示例"""
        # 查找所有代码块
        for pre_tag in soup.find_all('pre'):
            code = pre_tag.get_text(strip=True)
            
            # 跳过空代码块或太短的代码块
            if not code or len(code) < 5:
                continue
            
            # 判断是请求还是响应示例
            parent_heading = self._find_parent_heading(pre_tag)
            
            if parent_heading:
                heading_text = parent_heading.lower()
                
                # 判断语言
                language = 'text'
                if '<xml' in code or '</xml>' in code:
                    language = 'xml'
                elif ('{' in code and '}' in code) or code.startswith('['):
                    language = 'json'
                elif 'curl' in code.lower():
                    language = 'bash'
                elif 'http' in code.lower() and ('post' in code.lower() or 'get' in code.lower()):
                    language = 'http'
                
                example = CodeExample(
                    title=parent_heading,
                    language=language,
                    code=code
                )
                
                # 分类存储 - 更精确的判断
                if '请求包体' in heading_text or '请求体' in heading_text or '请求示例' in heading_text:
                    api_doc.request_examples.append(example)
                elif '返回结果' in heading_text or '响应' in heading_text or 'response' in heading_text:
                    api_doc.response_examples.append(example)
                elif '请求' in heading_text or 'request' in heading_text:
                    api_doc.request_examples.append(example)
                elif '返回' in heading_text or '结果' in heading_text:
                    api_doc.response_examples.append(example)
                else:
                    # 默认：JSON 格式且包含 errcode 的是响应，否则是请求
                    if language == 'json' and 'errcode' in code.lower():
                        api_doc.response_examples.append(example)
                    else:
                        api_doc.request_examples.append(example)
    
    def _find_parent_heading(self, element) -> str:
        """查找元素前最近的标题"""
        # 同时查找 h 标签和 strong 标签（企业微信文档常用 strong 作为小标题）
        for sibling in element.find_all_previous(['h2', 'h3', 'h4', 'h5', 'strong']):
            heading_text = sibling.get_text(strip=True)
            # 过滤掉一些非标题的 strong 标签（如果文本太短或太长）
            if len(heading_text) > 1 and len(heading_text) < 100:
                return heading_text
        return ""
    
    def _extract_sections(self, soup: BeautifulSoup, api_doc: APIDoc):
        """提取文档章节"""
        for heading in soup.find_all(['h2', 'h3', 'h4']):
            section_title = heading.get_text(strip=True)
            
            # 跳过参数相关的章节（会单独处理）
            if '参数' in section_title.lower() or 'parameter' in section_title.lower():
                continue
            
            # 收集该标题后的内容，直到下一个标题
            content_parts = []
            for sibling in heading.find_next_siblings():
                if sibling.name in ['h2', 'h3', 'h4']:
                    break
                # 跳过表格和代码块（会单独处理）
                if sibling.name not in ['table', 'pre']:
                    text = sibling.get_text(strip=True)
                    if text:
                        content_parts.append(text)
            
            content = '\n'.join(content_parts).strip()
            
            if content:
                api_doc.sections.append(Section(title=section_title, content=content))
    
    def _extract_params_from_json_examples(self, soup: BeautifulSoup, api_doc: APIDoc, is_request: bool = True) -> Dict[str, str]:
        """从 JSON 示例中提取参数，返回参数名到类型的映射
        
        Args:
            soup: BeautifulSoup 对象
            api_doc: API 文档对象
            is_request: True 表示提取请求参数，False 表示提取响应参数
        """
        json_params_map = {}  # 参数名 -> 类型的映射
        
        # 根据 is_request 确定要匹配的关键词
        if is_request:
            keywords = ['请求包体', '请求体', '请求参数', '请求示例']
        else:
            keywords = ['返回结果', '响应包体', '响应示例', '返回示例', '响应参数']
        
        # 查找所有代码块
        for pre_tag in soup.find_all('pre'):
            code = pre_tag.get_text(strip=True)
            
            # 跳过空代码块
            if not code or len(code) < 5:
                continue
            
            # 查找前面的标题
            parent_heading = self._find_parent_heading(pre_tag)
            
            # 检查是否匹配关键词
            is_match = any(keyword in parent_heading for keyword in keywords)
            
            # 对于响应，也可以通过检查 JSON 中是否包含 errcode 来判断
            if not is_match and not is_request:
                try:
                    json_str = code.strip()
                    if json_str.startswith('```'):
                        lines = json_str.split('\n')
                        json_str = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_str
                    test_obj = json.loads(json_str)
                    if isinstance(test_obj, dict) and 'errcode' in test_obj:
                        is_match = True
                except:
                    pass
            
            if is_match:
                # 尝试解析 JSON
                try:
                    # 清理代码（可能包含注释等）
                    json_str = code.strip()
                    # 移除可能的 markdown 标记
                    if json_str.startswith('```'):
                        lines = json_str.split('\n')
                        json_str = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_str
                    
                    # 尝试解析 JSON
                    json_obj = json.loads(json_str)
                    
                    # 从 JSON 推测参数
                    params = self._infer_json_params(json_obj)
                    
                    # 构建参数映射
                    for param in params:
                        json_params_map[param.name] = param.type
                    
                    # 标记找到了 JSON 参数
                    if params:
                        param_type = "请求" if is_request else "响应"
                        print(f"    → 从 {param_type}JSON 中推测了 {len(params)} 个参数的类型")
                    
                except json.JSONDecodeError:
                    # 不是有效的 JSON，跳过
                    pass
                except Exception as e:
                    # 其他错误，记录但继续
                    print(f"    ⚠ 解析 JSON 参数时出错: {e}")
        
        return json_params_map
    
    def _infer_json_params(self, json_obj, parent_key='') -> List[Parameter]:
        """从 JSON 对象中推测参数信息"""
        params = []
        
        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                param_name = f"{parent_key}.{key}" if parent_key else key
                
                # 处理嵌套对象和数组
                if isinstance(value, dict):
                    # 对象类型，递归处理
                    param_type = "object"
                    param = Parameter(
                        name=param_name,
                        type=param_type,
                        required=False,
                        description=""
                    )
                    params.append(param)
                    
                    # 递归处理嵌套字段
                    nested_params = self._infer_json_params(value, param_name)
                    params.extend(nested_params)
                    
                elif isinstance(value, list) and len(value) > 0:
                    if isinstance(value[0], dict):
                        # 数组中包含对象
                        param_type = "array[object]"
                        param = Parameter(
                            name=param_name,
                            type=param_type,
                            required=False,
                            description=""
                        )
                        params.append(param)
                        
                        # 递归处理数组中的对象字段
                        nested_params = self._infer_json_params(value[0], param_name)
                        params.extend(nested_params)
                    else:
                        # 数组中是基本类型
                        elem_type = self._infer_type(value[0])
                        param_type = f"array[{elem_type}]"
                        param = Parameter(
                            name=param_name,
                            type=param_type,
                            required=False,
                            description=""
                        )
                        params.append(param)
                else:
                    # 基本类型
                    param_type = self._infer_type(value)
                    param = Parameter(
                        name=param_name,
                        type=param_type,
                        required=False,
                        description=""
                    )
                    params.append(param)
        
        return params
    
    def _infer_type(self, value) -> str:
        """推测值的类型"""
        if value is None:
            return "string"
        elif isinstance(value, bool):
            return "bool"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            if len(value) == 0:
                return "array"
            else:
                elem_type = self._infer_type(value[0])
                return f"array[{elem_type}]"
        elif isinstance(value, dict):
            return "object"
        else:
            return "unknown"
    
    def _extract_parameters(self, soup: BeautifulSoup, api_doc: APIDoc):
        """提取参数表格"""
        # 首先尝试从 JSON 示例中提取参数
        request_json_params = self._extract_params_from_json_examples(soup, api_doc, is_request=True)
        response_json_params = self._extract_params_from_json_examples(soup, api_doc, is_request=False)
        
        # 然后从表格中提取参数
        json_params = request_json_params  # 用于后续处理请求参数
        for table in soup.find_all('table'):
            # 找到表格前最近的标题
            parent_heading = ""
            for sibling in table.find_all_previous(['h2', 'h3', 'h4', 'h5']):
                parent_heading = sibling.get_text(strip=True).lower()
                break
            
            # 检查表格前是否有 "返回结果" 相关文本
            has_return_result_before = False
            context_text = ""
            # 限制搜索范围：只查看表格前最近的几个元素
            prev_elements = 0
            for sibling in table.find_all_previous(['p', 'strong', 'h2', 'h3', 'h4', 'h5']):
                text = sibling.get_text(strip=True)
                context_text = text + " " + context_text
                prev_elements += 1
                
                # 限制搜索范围：最多查看前10个元素或200字符
                if prev_elements > 10 or len(context_text) > 200:
                    break
                
                # 检测是否出现 "返回结果" 相关关键词（支持带冒号或不带冒号）
                text_lower = text.lower()
                return_keywords = ['返回结果', '返回参数', '响应参数', '返回值', '返回说明']
                response_keywords = ['response', 'return']
                
                # 检查中文关键词
                for keyword in return_keywords:
                    if keyword in text:
                        has_return_result_before = True
                        break
                
                # 检查英文关键词（需要整词匹配）
                if not has_return_result_before:
                    for keyword in response_keywords:
                        if keyword in text_lower and (
                            keyword + ' ' in text_lower or 
                            keyword + ':' in text_lower or
                            keyword + '：' in text_lower
                        ):
                            has_return_result_before = True
                            break
                
                if has_return_result_before:
                    break
            
            rows = table.find_all('tr')
            if len(rows) < 2:
                continue
            
            # 解析表头
            header_row = rows[0]
            headers = [th.get_text(strip=True).lower() for th in header_row.find_all(['th', 'td'])]
            
            # 查找列索引
            name_idx = self._find_column_index(headers, ['参数', 'name', '字段', 'field'])
            type_idx = self._find_column_index(headers, ['类型', 'type'])
            required_idx = self._find_column_index(headers, ['必填', 'required', '必须'])
            desc_idx = self._find_column_index(headers, ['说明', 'description', '描述'])
            
            # 如果找不到描述列，使用最后一列
            if desc_idx == -1 and len(headers) > 0:
                desc_idx = len(headers) - 1
            
            # 解析数据行
            params_list = []
            for row in rows[1:]:
                cells = row.find_all('td')
                if len(cells) < 2:
                    continue
                
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                
                param_name = cell_texts[name_idx] if name_idx != -1 and name_idx < len(cell_texts) else cell_texts[0]
                param_type = cell_texts[type_idx] if type_idx != -1 and type_idx < len(cell_texts) else ""
                param_desc = cell_texts[desc_idx] if desc_idx != -1 and desc_idx < len(cell_texts) else ""
                
                # 如果表格中没有类型信息，尝试从 JSON 推测的类型中获取
                # 根据上下文判断是请求还是响应参数
                if not param_type:
                    if has_return_result_before and param_name in response_json_params:
                        param_type = response_json_params[param_name]
                    elif param_name in request_json_params:
                        param_type = request_json_params[param_name]
                
                # 检查该参数是否已经作为 query 参数存在
                existing_query_param = None
                for qp in api_doc.query_params:
                    if qp.name == param_name:
                        existing_query_param = qp
                        break
                
                # 如果已经是 query 参数，更新其信息（保留 query 标记）
                if existing_query_param:
                    # 更新类型（如果表格提供了类型信息）
                    if param_type:
                        existing_query_param.type = param_type
                    # 更新描述
                    if param_desc:
                        existing_query_param.description = param_desc
                    # 更新必填状态
                    if required_idx != -1 and required_idx < len(cell_texts):
                        required_text = cell_texts[required_idx].lower()
                        existing_query_param.required = any(keyword in required_text for keyword in ['是', 'yes', 'true', '必填', '必须'])
                    # 不添加到 params_list，因为已经在 query_params 中
                    continue
                
                param = Parameter(
                    name=param_name,
                    type=param_type,
                    required=False,
                    description=param_desc
                )
                
                # 判断是否必填
                if required_idx != -1 and required_idx < len(cell_texts):
                    required_text = cell_texts[required_idx].lower()
                    param.required = any(keyword in required_text for keyword in ['是', 'yes', 'true', '必填', '必须'])
                
                params_list.append(param)
            
            # 智能分类参数
            self._classify_parameters(params_list, parent_heading, api_doc, has_return_result_before)
        
        # 处理请求 JSON 中存在但表格中不存在的参数
        if request_json_params:
            # 收集所有已经添加的参数名
            all_param_names = {p.name for p in (
                api_doc.request_params + 
                api_doc.response_params + 
                api_doc.query_params + 
                api_doc.body_params + 
                api_doc.parameters
            )}
            
            # 添加 JSON 中独有的参数到 body_params
            json_only_params = []
            for param_name, param_type in request_json_params.items():
                if param_name not in all_param_names:
                    json_only_params.append(Parameter(
                        name=param_name,
                        type=param_type,
                        required=False,
                        description="(从请求示例中推测)"
                    ))
            
            if json_only_params:
                api_doc.body_params.extend(json_only_params)
                print(f"    → 从请求JSON中补充了 {len(json_only_params)} 个表格中不存在的参数")
        
        # 处理响应 JSON 中存在但表格中不存在的参数
        if response_json_params:
            # 收集所有已经添加的参数名
            all_param_names = {p.name for p in (
                api_doc.request_params + 
                api_doc.response_params + 
                api_doc.query_params + 
                api_doc.body_params + 
                api_doc.parameters
            )}
            
            # 添加 JSON 中独有的参数到 response_params
            json_only_params = []
            for param_name, param_type in response_json_params.items():
                if param_name not in all_param_names:
                    json_only_params.append(Parameter(
                        name=param_name,
                        type=param_type,
                        required=False,
                        description="(从响应示例中推测)"
                    ))
            
            if json_only_params:
                api_doc.response_params.extend(json_only_params)
                print(f"    → 从响应JSON中补充了 {len(json_only_params)} 个表格中不存在的参数")
    
    def _classify_parameters(self, params_list: List[Parameter], parent_heading: str, api_doc: APIDoc, has_return_result_before: bool = False):
        """智能分类参数到请求参数或响应参数"""
        # 优先检查：如果表格前有 "返回结果" 相关文本，直接归类为响应参数
        if has_return_result_before:
            api_doc.response_params.extend(params_list)
            return
        
        # 明确的标题指示
        if '请求参数' in parent_heading or 'request' in parent_heading:
            api_doc.request_params.extend(params_list)
            return
        elif '响应参数' in parent_heading or 'response' in parent_heading or '返回参数' in parent_heading:
            api_doc.response_params.extend(params_list)
            return
        elif 'query' in parent_heading:
            api_doc.query_params.extend(params_list)
            return
        elif 'body' in parent_heading:
            api_doc.body_params.extend(params_list)
            return
        
        # 没有明确标题时，智能判断
        # 明确的响应参数（只会在响应中出现）
        response_only_names = {
            'errcode', 'errmsg', 'error_code', 'error_msg',
            'result', 'data', 'info', 'detail',
            'next_cursor', 'has_more', 'total', 'count',
            'expires_in', 'refresh_token', 'openid', 'unionid'
        }
        
        # 明确的请求参数（只会在请求中出现）
        request_only_names = {
            'provider_access_token', 'suite_access_token',
            'corpid', 'userid', 'agentid', 'suite_id', 
            'cursor', 'limit', 'offset', 'size',
            'start_time', 'end_time', 'begin_time',
            'filter', 'sort', 'order'
        }
        
        # 可能在请求或响应中的参数（需要根据上下文判断）
        ambiguous_names = {
            'access_token', 'list', 'page', 'status', 'code', 'message'
        }
        
        # 分离请求参数和响应参数
        request_params = []
        response_params = []
        
        for param in params_list:
            param_name_lower = param.name.lower()
            desc_lower = param.description.lower()
            
            # 1. 包含点号的通常是响应参数（如 order_list.order_id）
            if '.' in param.name:
                response_params.append(param)
                continue
            
            # 2. 明确的响应参数
            if param_name_lower in response_only_names:
                response_params.append(param)
                continue
            
            # 3. 明确的请求参数  
            if param_name_lower in request_only_names:
                request_params.append(param)
                continue
            
            # 4. 特殊描述判断
            # "由上次调用返回" 说明是响应参数，但要在下次请求中使用
            if '由上一次调用返回' in desc_lower or '由上次调用返回' in desc_lower:
                response_params.append(param)
                continue
            
            # 5. 必填参数通常是请求参数（响应参数很少标记为必填）
            if param.required:
                request_params.append(param)
                continue
            
            # 6. 根据描述中的关键词判断
            response_keywords = ['返回', '输出', '结果', 'return', 'output']
            request_keywords = ['传入', '输入', '填写', '指定', '查询', 'input', 'specify', 'query']
            
            has_response_keyword = any(k in desc_lower for k in response_keywords)
            has_request_keyword = any(k in desc_lower for k in request_keywords)
            
            if has_response_keyword and not has_request_keyword:
                response_params.append(param)
                continue
            elif has_request_keyword and not has_response_keyword:
                request_params.append(param)
                continue
            
            # 7. 默认规则：一旦遇到明确的响应参数（如 errcode），后面的都是响应参数
            if response_params:
                response_params.append(param)
            else:
                # 前面没有明确的响应参数时，判断为请求参数
                request_params.append(param)
        
        # 如果所有参数都被判断为请求参数或响应参数，直接使用
        if request_params and response_params:
            api_doc.request_params.extend(request_params)
            api_doc.response_params.extend(response_params)
        elif request_params:
            api_doc.request_params.extend(request_params)
        elif response_params:
            api_doc.response_params.extend(response_params)
        else:
            # 都无法判断，放到通用参数
            api_doc.parameters.extend(params_list)
    
    def _find_column_index(self, headers: List[str], keywords: List[str]) -> int:
        """查找包含关键词的列索引"""
        for i, header in enumerate(headers):
            for keyword in keywords:
                if keyword in header:
                    return i
        return -1
    
    def _save_to_json(self):
        """保存为 JSON 格式"""
        output_file = self.output_dir / 'api_docs.json'
        
        # 转换为可序列化的字典
        data = []
        for doc in self.api_docs:
            doc_dict = {
                'title': doc.title,
                'url': doc.url,
                'path': doc.path,
                'description': doc.description,
                'method': doc.method,
                'api_url': doc.api_url,
                'api_name': doc.api_name,
                'group_title': doc.group_title,
                'request': doc.request,
                'response': doc.response,
                'request_params': [asdict(p) for p in doc.request_params],
                'response_params': [asdict(p) for p in doc.response_params],
                'query_params': [asdict(p) for p in doc.query_params],
                'body_params': [asdict(p) for p in doc.body_params],
                'request_examples': [asdict(e) for e in doc.request_examples],
                'response_examples': [asdict(e) for e in doc.response_examples],
                'parameters': [asdict(p) for p in doc.parameters],
                'sections': [asdict(s) for s in doc.sections]
            }
            data.append(doc_dict)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n已保存完整 JSON 文件: {output_file}")
    
    def _save_single_markdown_grouped(self, doc: APIDoc, index: int, total: int):
        """保存分组的 API Markdown 文件"""
        # 计算完整度分数
        score = self._calculate_completeness_score(doc)
        
        # 生成文件名：使用 path-index-api_name-score.md
        api_name_part = f"-{doc.api_name}" if doc.api_name else ""
        filename = f"{doc.path}-{index}{api_name_part}-{score}.md"
        output_file = self.output_dir / filename
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(self._generate_markdown_grouped(doc, index, total))
            print(f"    → 已保存: {output_file.name} (完整度: {score}/6, {index}/{total})")
        except Exception as e:
            print(f"    ✗ 保存失败: {e}")
    
    def _save_single_markdown(self, doc: APIDoc):
        """立即保存单个 API 的 Markdown 文件"""
        # 计算完整度分数
        score = self._calculate_completeness_score(doc)
        
        # 生成文件名，加上完整度后缀
        filename = doc.path if doc.path else self._sanitize_filename(doc.title)
        output_file = self.output_dir / f"{filename}-{score}.md"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(self._generate_markdown(doc))
            print(f"    → 已保存: {output_file.name} (完整度: {score}/6)")
        except Exception as e:
            print(f"    ✗ 保存失败: {e}")
    
    def _calculate_completeness_score(self, doc: APIDoc) -> int:
        """
        计算文档完整度分数（0-6分）
        
        必选项：
        1. 请求方法 (method)
        2. 接口地址 (api_url)
        3. 请求参数 (request_params/query_params/body_params)
        4. 请求示例 (request_examples)
        5. 响应参数 (response_params)
        6. 响应示例 (response_examples)
        """
        score = 0
        
        # 1. 请求方法
        if doc.method:
            score += 1
        
        # 2. 接口地址
        if doc.api_url:
            score += 1
        
        # 3. 请求参数（任意一种即可）
        if doc.request_params or doc.query_params or doc.body_params:
            score += 1
        
        # 4. 请求示例
        if doc.request_examples:
            score += 1
        
        # 5. 响应参数
        if doc.response_params:
            score += 1
        
        # 6. 响应示例
        if doc.response_examples:
            score += 1
        
        return score
    
    def _update_index(self):
        """实时更新索引文件"""
        output_file = self.output_dir / 'README.md'
        
        lines = [
            "# 企业微信 API 文档索引\n",
            f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"共 {len(self.api_docs)} 个 API 接口\n",
            "",
            "## 说明\n",
            "文件名格式：`{id}-{score}.md`，其中 score 表示完整度（0-6分）",
            "- 6分：包含所有必选信息（请求方法、接口地址、请求参数、请求示例、响应参数、响应示例）",
            "- 5分：缺少1项",
            "- 4分：缺少2项",
            "- 以此类推\n",
            "## API 列表\n"
        ]
        
        for doc in self.api_docs:
            score = self._calculate_completeness_score(doc)
            filename = doc.path if doc.path else self._sanitize_filename(doc.title)
            desc = doc.description[:50] + "..." if len(doc.description) > 50 else doc.description
            
            # 添加完整度标识
            score_badge = "🟢" if score == 6 else "🟡" if score >= 4 else "🔴"
            lines.append(f"- {score_badge} [{doc.title}]({filename}-{score}.md) `[{score}/6]` - {desc}")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))
        except Exception as e:
            print(f"    ✗ 更新索引失败: {e}")
    
    def _generate_markdown_grouped(self, doc: APIDoc, index: int, total: int) -> str:
        """生成分组 API 的 Markdown 文档"""
        lines = []
        
        # 标题（包含分组信息）
        if doc.group_title:
            lines.append(f"# {doc.group_title}\n")
        else:
            lines.append(f"# {doc.title} - 接口 {index}/{total}\n")
        
        # 基本信息
        lines.append("## 基本信息\n")
        lines.append(f"- **文档地址**: [{doc.url}]({doc.url})")
        if doc.path:
            lines.append(f"- **文档 ID**: `{doc.path}`")
        if doc.api_name:
            lines.append(f"- **API 名称**: `{doc.api_name}`")
        if doc.method:
            lines.append(f"- **请求方法**: `{doc.method}`")
        if doc.api_url:
            lines.append(f"- **接口地址**: `{doc.api_url}`")
        if total > 1:
            lines.append(f"- **分组信息**: 第 {index} 个接口，共 {total} 个")
        lines.append("")
        
        # 其余部分与原方法相同
        # 描述
        if doc.description:
            lines.append(f"## 接口描述\n")
            lines.append(f"{doc.description}\n")
        
        # 请求信息
        has_request_info = (doc.request_params or doc.query_params or 
                           doc.body_params or doc.request_examples)
        
        if has_request_info:
            lines.append("## 请求信息\n")
            
            # HTTP 请求格式
            if doc.request:
                lines.append("### 请求格式\n")
                # 判断语言
                lang = 'http'
                if '<xml' in doc.request or '</xml>' in doc.request:
                    lang = 'xml'
                elif '{' in doc.request and '}' in doc.request:
                    lang = 'json'
                lines.append(f"```{lang}")
                lines.append(doc.request)
                lines.append("```\n")
            
            # Query 参数
            if doc.query_params:
                lines.append("### Query 参数\n")
                lines.append("| 参数名 | 类型 | 必填 | 说明 |")
                lines.append("|--------|------|------|------|")
                for param in doc.query_params:
                    required = "是" if param.required else "否"
                    lines.append(f"| {param.name} | {param.type} | {required} | {param.description} |")
                lines.append("")
            
            # Body 参数
            if doc.body_params:
                lines.append("### Body 参数\n")
                lines.append("| 参数名 | 类型 | 必填 | 说明 |")
                lines.append("|--------|------|------|------|")
                for param in doc.body_params:
                    required = "是" if param.required else "否"
                    lines.append(f"| {param.name} | {param.type} | {required} | {param.description} |")
                lines.append("")
            
            # 请求参数（通用）
            if doc.request_params:
                lines.append("### 请求参数\n")
                lines.append("| 参数名 | 类型 | 必填 | 说明 |")
                lines.append("|--------|------|------|------|")
                for param in doc.request_params:
                    required = "是" if param.required else "否"
                    lines.append(f"| {param.name} | {param.type} | {required} | {param.description} |")
                lines.append("")
            
            # 请求示例
            if doc.request_examples:
                lines.append("### 请求示例\n")
                for i, example in enumerate(doc.request_examples, 1):
                    if len(doc.request_examples) > 1:
                        lines.append(f"#### 示例 {i}: {example.title}\n")
                    lines.append(f"```{example.language}")
                    lines.append(example.code)
                    lines.append("```\n")
        
        # 响应信息
        has_response_info = doc.response_params or doc.response_examples
        
        if has_response_info:
            lines.append("## 响应信息\n")
            
            # 响应参数
            if doc.response_params:
                lines.append("### 响应参数\n")
                lines.append("| 参数名 | 类型 | 说明 |")
                lines.append("|--------|------|------|")
                for param in doc.response_params:
                    lines.append(f"| {param.name} | {param.type} | {param.description} |")
                lines.append("")
            
            # 响应示例
            if doc.response_examples:
                lines.append("### 响应示例\n")
                for i, example in enumerate(doc.response_examples, 1):
                    if len(doc.response_examples) > 1:
                        lines.append(f"#### 示例 {i}: {example.title}\n")
                    lines.append(f"```{example.language}")
                    lines.append(example.code)
                    lines.append("```\n")
        
        # 通用参数（如果既不是请求也不是响应参数）
        if doc.parameters:
            lines.append("## 参数说明\n")
            lines.append("| 参数名 | 类型 | 必填 | 说明 |")
            lines.append("|--------|------|------|------|")
            for param in doc.parameters:
                required = "是" if param.required else "否"
                lines.append(f"| {param.name} | {param.type} | {required} | {param.description} |")
            lines.append("")
        
        # 其他章节
        if doc.sections:
            lines.append("## 其他说明\n")
            for section in doc.sections:
                lines.append(f"### {section.title}\n")
                lines.append(f"{section.content}\n")
        
        return "\n".join(lines)
    
    def _generate_markdown(self, doc: APIDoc) -> str:
        """生成单个 API 的 Markdown 文档"""
        lines = []
        
        # 标题
        lines.append(f"# {doc.title}\n")
        
        # 基本信息
        lines.append("## 基本信息\n")
        lines.append(f"- **文档地址**: [{doc.url}]({doc.url})")
        if doc.path:
            lines.append(f"- **文档 ID**: `{doc.path}`")
        if doc.method:
            lines.append(f"- **请求方法**: `{doc.method}`")
        if doc.api_url:
            lines.append(f"- **接口地址**: `{doc.api_url}`")
        lines.append("")
        
        # 描述
        if doc.description:
            lines.append(f"## 接口描述\n")
            lines.append(f"{doc.description}\n")
        
        # 请求信息
        has_request_info = (doc.request_params or doc.query_params or 
                           doc.body_params or doc.request_examples)
        
        if has_request_info:
            lines.append("## 请求信息\n")
            
            # HTTP 请求格式
            if doc.request:
                lines.append("### 请求格式\n")
                # 判断语言
                lang = 'http'
                if '<xml' in doc.request or '</xml>' in doc.request:
                    lang = 'xml'
                elif '{' in doc.request and '}' in doc.request:
                    lang = 'json'
                lines.append(f"```{lang}")
                lines.append(doc.request)
                lines.append("```\n")
            
            # Query 参数
            if doc.query_params:
                lines.append("### Query 参数\n")
                lines.append("| 参数名 | 类型 | 必填 | 说明 |")
                lines.append("|--------|------|------|------|")
                for param in doc.query_params:
                    required = "是" if param.required else "否"
                    lines.append(f"| {param.name} | {param.type} | {required} | {param.description} |")
                lines.append("")
            
            # Body 参数
            if doc.body_params:
                lines.append("### Body 参数\n")
                lines.append("| 参数名 | 类型 | 必填 | 说明 |")
                lines.append("|--------|------|------|------|")
                for param in doc.body_params:
                    required = "是" if param.required else "否"
                    lines.append(f"| {param.name} | {param.type} | {required} | {param.description} |")
                lines.append("")
            
            # 请求参数（通用）
            if doc.request_params:
                lines.append("### 请求参数\n")
                lines.append("| 参数名 | 类型 | 必填 | 说明 |")
                lines.append("|--------|------|------|------|")
                for param in doc.request_params:
                    required = "是" if param.required else "否"
                    lines.append(f"| {param.name} | {param.type} | {required} | {param.description} |")
                lines.append("")
            
            # 请求示例
            if doc.request_examples:
                lines.append("### 请求示例\n")
                for i, example in enumerate(doc.request_examples, 1):
                    if len(doc.request_examples) > 1:
                        lines.append(f"#### 示例 {i}: {example.title}\n")
                    lines.append(f"```{example.language}")
                    lines.append(example.code)
                    lines.append("```\n")
        
        # 响应信息
        has_response_info = doc.response_params or doc.response_examples
        
        if has_response_info:
            lines.append("## 响应信息\n")
            
            # 响应参数
            if doc.response_params:
                lines.append("### 响应参数\n")
                lines.append("| 参数名 | 类型 | 说明 |")
                lines.append("|--------|------|------|")
                for param in doc.response_params:
                    lines.append(f"| {param.name} | {param.type} | {param.description} |")
                lines.append("")
            
            # 响应示例
            if doc.response_examples:
                lines.append("### 响应示例\n")
                for i, example in enumerate(doc.response_examples, 1):
                    if len(doc.response_examples) > 1:
                        lines.append(f"#### 示例 {i}: {example.title}\n")
                    lines.append(f"```{example.language}")
                    lines.append(example.code)
                    lines.append("```\n")
        
        # 通用参数（如果既不是请求也不是响应参数）
        if doc.parameters:
            lines.append("## 参数说明\n")
            lines.append("| 参数名 | 类型 | 必填 | 说明 |")
            lines.append("|--------|------|------|------|")
            for param in doc.parameters:
                required = "是" if param.required else "否"
                lines.append(f"| {param.name} | {param.type} | {required} | {param.description} |")
            lines.append("")
        
        # 其他章节
        if doc.sections:
            lines.append("## 其他说明\n")
            for section in doc.sections:
                lines.append(f"### {section.title}\n")
                lines.append(f"{section.content}\n")
        
        return "\n".join(lines)
    
    def _generate_index(self):
        """生成最终索引文件"""
        output_file = self.output_dir / 'README.md'
        
        # 统计完整度分布
        score_stats = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for doc in self.api_docs:
            score = self._calculate_completeness_score(doc)
            score_stats[score] += 1
        
        lines = [
            "# 企业微信 API 文档索引\n",
            f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"共 {len(self.api_docs)} 个 API 接口\n",
            "## 完整度统计\n",
            f"- 🟢 完整（6分）: {score_stats[6]} 个",
            f"- 🟡 较完整（4-5分）: {score_stats[5] + score_stats[4]} 个",
            f"- 🔴 不完整（0-3分）: {score_stats[3] + score_stats[2] + score_stats[1] + score_stats[0]} 个\n",
            "## 说明\n",
            "文件名格式：`{id}-{score}.md`，其中 score 表示完整度（0-6分）\n",
            "**必选项（共6项）：**",
            "1. 请求方法 (GET/POST/PUT/DELETE)",
            "2. 接口地址 (API URL)",
            "3. 请求参数 (Query/Body 参数)",
            "4. 请求示例 (JSON/XML 示例)",
            "5. 响应参数 (返回字段说明)",
            "6. 响应示例 (返回数据示例)\n",
            "## API 列表\n"
        ]
        
        # 按完整度和 path 排序
        sorted_docs = sorted(self.api_docs, key=lambda x: (
            -self._calculate_completeness_score(x),  # 完整度降序
            x.path if x.path else x.title  # path 升序
        ))
        
        for doc in sorted_docs:
            score = self._calculate_completeness_score(doc)
            filename = doc.path if doc.path else self._sanitize_filename(doc.title)
            desc = doc.description[:50] + "..." if len(doc.description) > 50 else doc.description
            
            # 完整度标识
            score_badge = "🟢" if score == 6 else "🟡" if score >= 4 else "🔴"
            method_tag = f"`{doc.method}` " if doc.method else ""
            
            lines.append(f"- {score_badge} {method_tag}[{doc.title}]({filename}-{score}.md) `[{score}/6]` - {desc}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        
        print(f"\n已生成最终索引: {output_file}")
        print(f"  🟢 完整文档: {score_stats[6]} 个")
        print(f"  🟡 较完整: {score_stats[5] + score_stats[4]} 个")
        print(f"  🔴 需完善: {score_stats[3] + score_stats[2] + score_stats[1] + score_stats[0]} 个")
    
    def _extract_route_path(self, soup: BeautifulSoup) -> List[str]:
        """从页面中提取路由路径（面包屑导航）
        
        示例 HTML:
        <div class="ep-route-dir">
            <div class="ep-route-dir-item"><span>第三方应用开发</span>...</div>
            <div class="ep-route-dir-item"><span>服务端API</span>...</div>
            <div class="ep-route-dir-item"><span>推广二维码</span>...</div>
        </div>
        
        返回: ['第三方应用开发', '服务端API', '推广二维码']
        """
        route_path = []
        try:
            route_dir = soup.find('div', class_='ep-route-dir')
            if route_dir:
                route_items = route_dir.find_all('div', class_='ep-route-dir-item')
                for item in route_items:
                    span = item.find('span')
                    if span and span.text:
                        route_path.append(span.text.strip())
        except Exception as e:
            print(f"  ⚠️  解析路由失败: {e}")
        
        return route_path
    
    def _check_captcha_page(self, soup: BeautifulSoup) -> bool:
        """检测是否为验证码页面"""
        # 检查页面标题
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            if '企业微信-验证码' in title or '验证码' == title:
                return True
        
        # 检查常见的验证码元素
        captcha_indicators = [
            'captcha',
            'verify',
            'verification',
            '验证码',
            '人机验证'
        ]
        
        # 检查页面文本
        page_text = soup.get_text()
        for indicator in captcha_indicators:
            if indicator in page_text.lower() or indicator in page_text:
                # 进一步确认（避免误判）
                if '请完成验证' in page_text or '请输入验证码' in page_text:
                    return True
        
        return False
    
    def _load_visited_urls(self):
        """加载已访问的 URL 列表"""
        visited_file = self.output_dir / '.visited_urls.json'
        if visited_file.exists():
            try:
                with open(visited_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.visited = set(data.get('visited', []))
                    print(f"已加载 {len(self.visited)} 个已访问的 URL")
            except Exception as e:
                print(f"加载已访问 URL 失败: {e}")
    
    def _save_visited_urls(self):
        """保存已访问的 URL 列表"""
        visited_file = self.output_dir / '.visited_urls.json'
        try:
            with open(visited_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'visited': list(self.visited),
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存已访问 URL 失败: {e}")
    
    def _save_failed_docs(self):
        """保存失败的文档列表"""
        if not self.failed_docs:
            return
        
        failed_file = self.output_dir / '.failed_docs.json'
        try:
            with open(failed_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'failed_docs': self.failed_docs,
                    'total': len(self.failed_docs),
                    'last_update': time.strftime('%Y-%m-%d %H:%M:%S')
                }, f, ensure_ascii=False, indent=2)
            
            # 同时保存一个纯文本的文档 ID 列表，方便直接使用
            failed_ids_file = self.output_dir / '.failed_doc_ids.txt'
            with open(failed_ids_file, 'w', encoding='utf-8') as f:
                for item in self.failed_docs:
                    f.write(f"{item['doc_id']}\n")
            
        except Exception as e:
            print(f"⚠️  保存失败文档列表失败: {e}")
    
    def _load_queue(self):
        """加载待爬取的 URL 队列"""
        queue_file = self.output_dir / '.crawl_queue.json'
        if queue_file.exists():
            try:
                with open(queue_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.queue = data.get('queue', [])
                    print(f"已加载 {len(self.queue)} 个待爬取的 URL")
            except Exception as e:
                print(f"加载待爬取队列失败: {e}")
    
    def _save_queue(self):
        """保存待爬取的 URL 队列"""
        queue_file = self.output_dir / '.crawl_queue.json'
        try:
            with open(queue_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'queue': self.queue,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'queue_size': len(self.queue)
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存待爬取队列失败: {e}")
    
    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """清理文件名，移除非法字符"""
        # 替换非法字符为下划线
        filename = re.sub(r'[^\w\-\.]', '_', filename)
        # 移除多个连续下划线
        filename = re.sub(r'_+', '_', filename)
        # 去除首尾下划线
        filename = filename.strip('_')
        return filename


def main():
    """主函数"""
    import sys
    import argparse
    
    # 配置参数
    BASE_URL = "https://developer.work.weixin.qq.com"
    START_PATH = "/document/path/91201"
    OUTPUT_DIR = "../api_docs"
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='企业微信 API 文档爬虫')
    parser.add_argument('--no-resume', action='store_true', help='禁用断点续爬模式')
    parser.add_argument('--doc-ids', type=str, help='指定要爬取的文档 ID，多个用逗号分隔，例如: 90601,90602')
    parser.add_argument('--output-dir', type=str, default=OUTPUT_DIR, help=f'输出目录，默认: {OUTPUT_DIR}')
    parser.add_argument('--split-multi-api', action='store_true', 
                       help='分割多接口页面（实验性功能，可能导致参数混杂，默认禁用）')
    parser.add_argument('--route-filter', type=str, nargs='+', default=["第三方应用开发", "服务端API"],
                       help='路由过滤器（支持多个，AND逻辑），必须同时包含所有关键词（例如: "第三方应用开发" "服务端API"）')
    parser.add_argument('--route-exclude', type=str, nargs='+',
                       help='路由排除器（支持多个，OR逻辑），包含任意一个就排除（例如: "服务商代开发"）')
    
    args = parser.parse_args()
    
    resume = not args.no_resume
    if args.no_resume:
        print("已禁用断点续爬模式\n")
    
    # 解析文档 ID
    doc_ids = None
    if args.doc_ids:
        doc_ids = [doc_id.strip() for doc_id in args.doc_ids.split(',')]
        print(f"将爬取指定的 {len(doc_ids)} 个文档\n")
    
    if args.split_multi_api:
        print("⚠️  已启用多接口分割（实验性功能）\n")
    
    # 路由过滤器
    if args.route_filter:
        print(f"✓ 路由包含过滤 (AND): 必须同时包含 {args.route_filter} 中的所有关键词")
    if args.route_exclude:
        print(f"✓ 路由排除过滤 (OR): 排除包含 {args.route_exclude} 中任意一个的页面")
    if args.route_filter or args.route_exclude:
        print()
    
    # 创建爬虫实例
    crawler = WeChatWorkAPICrawler(
        BASE_URL, 
        START_PATH, 
        args.output_dir, 
        resume=resume,
        doc_ids=doc_ids,
        split_multi_api=args.split_multi_api,
        route_filter=args.route_filter,
        route_exclude=args.route_exclude
    )
    
    # 开始爬取
    crawler.crawl()


if __name__ == "__main__":
    main()
