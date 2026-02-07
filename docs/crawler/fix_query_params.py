#!/usr/bin/env python3
"""
从 MD 文件中提取 query 参数并更新对应的 JSON 文件

用于修复爬虫因 LLM API 限制而遗漏的 URL query 参数
"""

import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse


class QueryParamFixer:
    """Query 参数修复工具"""
    
    def __init__(self, api_docs_dir: str, dry_run: bool = False, verbose: bool = False):
        self.api_docs_dir = Path(api_docs_dir)
        self.dry_run = dry_run
        self.verbose = verbose
        
        # 统计信息
        self.stats = {
            'total': 0,
            'updated': 0,
            'skipped': 0,
            'failed': 0,
            'no_json': 0
        }
        self.failed_files = []
    
    def process_all(self, files: Optional[List[str]] = None):
        """处理所有 MD 文件或指定的文件"""
        print(f"开始处理 MD 文件...")
        print(f"输入目录: {self.api_docs_dir}")
        if self.dry_run:
            print("⚠️  预览模式 (不会实际修改文件)")
        print()
        
        # 获取文件列表
        if files:
            md_files = [self.api_docs_dir / f for f in files if f.endswith('.md')]
        else:
            md_files = list(self.api_docs_dir.glob('*.md'))
            # 排除 README.md
            md_files = [f for f in md_files if f.name != 'README.md']
        
        md_files.sort()
        self.stats['total'] = len(md_files)
        
        # 处理每个文件
        for idx, md_file in enumerate(md_files, 1):
            print(f"[{idx}/{self.stats['total']}] {md_file.name}")
            try:
                self._process_file(md_file)
            except Exception as e:
                print(f"  ✗ 处理失败: {e}")
                self.stats['failed'] += 1
                self.failed_files.append({
                    'file': md_file.name,
                    'error': str(e)
                })
            print()
        
        # 显示统计
        self._print_summary()
    
    def _process_file(self, md_file: Path):
        """处理单个 MD 文件"""
        # 读取 MD 文件
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 提取文档 ID
        doc_id = self._extract_doc_id(md_file.name)
        if not doc_id:
            print(f"  ⚠️  无法从文件名提取文档 ID")
            self.stats['skipped'] += 1
            return
        
        # 查找对应的 JSON 文件
        json_file = self.api_docs_dir / f"{doc_id}_llm.json"
        if not json_file.exists():
            print(f"  ⚠️  未找到对应的 JSON 文件: {json_file.name}")
            self.stats['no_json'] += 1
            return
        
        # 提取 API URL
        api_url = self._extract_api_url(md_content)
        if not api_url:
            print(f"  ⚠️  未找到接口地址")
            self.stats['skipped'] += 1
            return
        
        if self.verbose:
            print(f"  → 提取到接口地址: {api_url}")
        
        # 提取 query 参数
        query_params = self._extract_query_params_from_table(md_content)
        
        if query_params:
            if self.verbose:
                print(f"  → 从 Query 参数表格提取到 {len(query_params)} 个参数: {', '.join([p['name'] for p in query_params])}")
        else:
            # 从 URL 提取
            query_params = self._extract_query_params_from_url(api_url)
            if query_params:
                print(f"  ⚠️  没有 Query 参数表格")
                if self.verbose:
                    print(f"  → 从 URL 提取到 {len(query_params)} 个参数: {', '.join([p['name'] for p in query_params])}")
            else:
                print(f"  ⚠️  URL 中没有 query 参数")
                self.stats['skipped'] += 1
                return
        
        # 更新 JSON 文件
        if self._update_json_file(json_file, query_params):
            print(f"  ✓ 成功更新 JSON: {json_file.name}")
            self.stats['updated'] += 1
        else:
            print(f"  → 跳过（query_params 已存在且相同）")
            self.stats['skipped'] += 1
    
    def _extract_doc_id(self, filename: str) -> Optional[str]:
        """从文件名提取文档 ID
        
        支持格式：
        - 100779-6.md -> 100779
        - 100779-1-get_auth_info-6.md -> 100779
        """
        # 匹配数字开头
        match = re.match(r'^(\d+)', filename)
        if match:
            return match.group(1)
        return None
    
    def _extract_api_url(self, md_content: str) -> Optional[str]:
        """从 MD 文件中提取 API URL"""
        # 查找 "- **接口地址**: `URL`" 格式
        pattern = r'-\s*\*\*接口地址\*\*:\s*`([^`]+)`'
        match = re.search(pattern, md_content)
        if match:
            return match.group(1)
        return None
    
    def _extract_query_params_from_table(self, md_content: str) -> List[Dict]:
        """从 MD 的 Query 参数表格中提取参数"""
        params = []
        in_query_section = False
        
        lines = md_content.split('\n')
        for i, line in enumerate(lines):
            # 检测进入 Query 参数章节
            if '### Query 参数' in line:
                in_query_section = True
                continue
            
            # 检测离开 Query 参数章节
            if in_query_section and line.startswith('###') and 'Query 参数' not in line:
                break
            
            # 解析表格行
            if in_query_section and line.startswith('|') and '---' not in line:
                parts = [p.strip() for p in line.split('|')[1:-1]]
                
                # 跳过表头
                if len(parts) >= 4 and parts[0] not in ['参数名', 'name', '']:
                    params.append({
                        'name': parts[0],
                        'type': parts[1],
                        'required': parts[2] in ['是', 'yes', 'true', '必填', 'Yes', 'True'],
                        'description': parts[3]
                    })
        
        return params
    
    def _extract_query_params_from_url(self, api_url: str) -> List[Dict]:
        """从 URL 中提取 query 参数"""
        params = []
        
        try:
            parsed_url = urlparse(api_url)
            
            if parsed_url.query:
                # 手动解析 query 参数
                query_parts = parsed_url.query.split('&')
                
                for part in query_parts:
                    if '=' in part:
                        key, value = part.split('=', 1)
                        
                        # 推测参数类型和描述
                        param_type = self._infer_query_param_type(key, value)
                        description = self._infer_query_param_description(key, value)
                        
                        params.append({
                            'name': key,
                            'type': param_type,
                            'required': True,
                            'description': description
                        })
        except Exception as e:
            if self.verbose:
                print(f"  ⚠️  解析 URL query 参数时出错: {e}")
        
        return params
    
    def _infer_query_param_type(self, key: str, value: str) -> str:
        """推测 query 参数的类型"""
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
    
    def _update_json_file(self, json_file: Path, query_params: List[Dict]) -> bool:
        """更新 JSON 文件中的 query_params
        
        返回 True 表示文件被更新，False 表示跳过（已存在相同内容）
        """
        # 读取现有的 JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查是否需要更新
        updated = False
        for api in data.get('apis', []):
            existing_params = api.get('query_params', [])
            
            # 比较参数是否相同
            if self._are_params_equal(existing_params, query_params):
                continue
            
            # 更新参数
            api['query_params'] = query_params
            updated = True
        
        if not updated:
            return False
        
        # 保存回 JSON（仅在非预览模式下）
        if not self.dry_run:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    
    def _are_params_equal(self, params1: List[Dict], params2: List[Dict]) -> bool:
        """比较两个参数列表是否相同"""
        if len(params1) != len(params2):
            return False
        
        # 按名称排序后比较
        p1_sorted = sorted(params1, key=lambda x: x.get('name', ''))
        p2_sorted = sorted(params2, key=lambda x: x.get('name', ''))
        
        for p1, p2 in zip(p1_sorted, p2_sorted):
            if p1.get('name') != p2.get('name'):
                return False
            if p1.get('type') != p2.get('type'):
                return False
            if p1.get('required') != p2.get('required'):
                return False
        
        return True
    
    def _print_summary(self):
        """打印处理统计"""
        print("=" * 60)
        print("处理完成！")
        print(f"  - 总文件数: {self.stats['total']}")
        print(f"  - 成功更新: {self.stats['updated']}")
        print(f"  - 跳过（无需更新）: {self.stats['skipped']}")
        print(f"  - 未找到 JSON: {self.stats['no_json']}")
        print(f"  - 失败: {self.stats['failed']}")
        
        if self.failed_files:
            print(f"\n失败的文件:")
            for item in self.failed_files:
                print(f"  - {item['file']}: {item['error']}")
        
        print("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='从 MD 文件中提取 query 参数并更新对应的 JSON 文件'
    )
    parser.add_argument(
        '--api-docs-dir',
        type=str,
        default='../api_docs',
        help='API 文档目录，默认: ../api_docs'
    )
    parser.add_argument(
        '--files',
        type=str,
        nargs='+',
        help='指定要处理的 MD 文件（文件名），例如: 100779-6.md 100764-6.md'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式，不实际修改文件'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='详细输出'
    )
    
    args = parser.parse_args()
    
    # 创建修复工具
    fixer = QueryParamFixer(
        api_docs_dir=args.api_docs_dir,
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    
    # 处理文件
    fixer.process_all(files=args.files)


if __name__ == '__main__':
    main()
