#!/usr/bin/env python3
"""
企业微信 API 文档爬虫
用于爬取企业微信开发者文档中的 API 接口文档，并生成 Markdown 格式的文档
"""

import os
import json
import time
import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, asdict
from pathlib import Path

import requests
from bs4 import BeautifulSoup


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
    
    def __init__(self, base_url: str, start_path: str, output_dir: str, resume: bool = True):
        self.base_url = base_url
        self.start_url = urljoin(base_url, start_path)
        self.output_dir = Path(output_dir)
        self.visited = set()
        self.api_docs = []
        self.resume = resume
        self.queue = []  # 待爬取的 URL 队列

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
        
        # 如果队列为空，需要重新扫描已访问的页面来发现新链接
        if not self.queue:
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
            
            print("\n爬取完成！")
            
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
                api_doc = self._extract_api_doc(soup, url)
                if api_doc:
                    self.api_docs.append(api_doc)
                    print(f"  ✓ 提取文档: {api_doc.title}")
                    
                    # 立即保存 Markdown 文件
                    self._save_single_markdown(api_doc)
                    
                    # 更新索引文件
                    self._update_index()
            
            # 查找相关链接并加入队列（无论是否已访问都要扫描）
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
            
    def _extract_api_doc(self, soup: BeautifulSoup, url: str) -> Optional[APIDoc]:
        """从页面中提取 API 文档信息"""
        # 提取标题
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
        
        api_doc = APIDoc(title=title, url=url, path=path)
        
        # 提取描述（通常是第一个段落）
        first_p = soup.find('p')
        if first_p:
            api_doc.description = first_p.get_text(strip=True)
        
        # 提取 HTTP 方法和请求 URL
        self._extract_http_info(soup, api_doc)
        
        # 提取代码示例
        self._extract_code_examples(soup, api_doc)
        
        # 提取章节
        self._extract_sections(soup, api_doc)
        
        # 提取参数表格
        self._extract_parameters(soup, api_doc)
        
        return api_doc
    
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
    
    def _extract_parameters(self, soup: BeautifulSoup, api_doc: APIDoc):
        """提取参数表格"""
        for table in soup.find_all('table'):
            # 找到表格前最近的标题
            parent_heading = ""
            for sibling in table.find_all_previous(['h2', 'h3', 'h4', 'h5']):
                parent_heading = sibling.get_text(strip=True).lower()
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
                
                param = Parameter(
                    name=cell_texts[name_idx] if name_idx != -1 and name_idx < len(cell_texts) else cell_texts[0],
                    type=cell_texts[type_idx] if type_idx != -1 and type_idx < len(cell_texts) else "",
                    required=False,
                    description=cell_texts[desc_idx] if desc_idx != -1 and desc_idx < len(cell_texts) else ""
                )
                
                # 判断是否必填
                if required_idx != -1 and required_idx < len(cell_texts):
                    required_text = cell_texts[required_idx].lower()
                    param.required = any(keyword in required_text for keyword in ['是', 'yes', 'true', '必填', '必须'])
                
                params_list.append(param)
            
            # 智能分类参数
            self._classify_parameters(params_list, parent_heading, api_doc)
    
    def _classify_parameters(self, params_list: List[Parameter], parent_heading: str, api_doc: APIDoc):
        """智能分类参数到请求参数或响应参数"""
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
    
    # 配置参数
    BASE_URL = "https://developer.work.weixin.qq.com"
    START_PATH = "/document/path/91201"
    OUTPUT_DIR = "../api_docs"
    
    # 支持命令行参数控制是否断点续爬
    resume = True  # 默认启用断点续爬
    if len(sys.argv) > 1 and sys.argv[1] == '--no-resume':
        resume = False
        print("已禁用断点续爬模式\n")
    
    # 创建爬虫实例
    crawler = WeChatWorkAPICrawler(BASE_URL, START_PATH, OUTPUT_DIR, resume=resume)
    
    # 开始爬取
    crawler.crawl()


if __name__ == "__main__":
    main()
