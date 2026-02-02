#!/usr/bin/env python3
"""
重新生成指定文档
用于修复参数分类问题
"""

import sys
import json
from pathlib import Path
from crawler import WeChatWorkAPICrawler

def regenerate_docs(doc_ids: list = None):
    """重新生成指定的文档"""
    
    output_dir = Path("../api_docs")
    visited_file = output_dir / '.visited_urls.json'
    
    if not visited_file.exists():
        print("错误: 找不到已访问的 URL 记录")
        print("请先运行爬虫: python3 crawler.py")
        return
    
    # 加载已访问的 URL
    with open(visited_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        visited_urls = data.get('visited', [])
    
    print(f"总共有 {len(visited_urls)} 个已访问的 URL")
    
    # 如果指定了文档 ID，只重新生成这些文档
    if doc_ids:
        urls_to_regenerate = []
        for doc_id in doc_ids:
            url = f"https://developer.work.weixin.qq.com/document/path/{doc_id}"
            if url in visited_urls:
                urls_to_regenerate.append(url)
            else:
                print(f"警告: 文档 {doc_id} 未找到在访问记录中")
        
        print(f"\n将重新生成 {len(urls_to_regenerate)} 个文档:")
        for url in urls_to_regenerate:
            doc_id = url.split('/')[-1]
            print(f"  - {doc_id}")
    else:
        # 重新生成所有文档
        urls_to_regenerate = visited_urls
        print(f"\n将重新生成所有 {len(urls_to_regenerate)} 个文档")
    
    if not urls_to_regenerate:
        print("没有需要重新生成的文档")
        return
    
    print("\n开始重新生成...")
    print("=" * 60)
    
    # 创建爬虫实例（禁用断点续爬，因为我们要重新处理）
    crawler = WeChatWorkAPICrawler(
        base_url="https://developer.work.weixin.qq.com",
        start_path="/document/path/91201",
        output_dir="../api_docs",
        resume=False
    )
    
    # 重新访问并提取每个页面
    import requests
    from bs4 import BeautifulSoup
    import time
    
    success_count = 0
    fail_count = 0
    
    for i, url in enumerate(urls_to_regenerate, 1):
        doc_id = url.split('/')[-1]
        print(f"\n[{i}/{len(urls_to_regenerate)}] 正在处理: {doc_id}")
        
        try:
            # 延迟请求
            time.sleep(1)
            
            response = requests.get(url, headers=crawler.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 检查是否为验证码页面
            if crawler._check_captcha_page(soup):
                print(f"  ⚠️  检测到验证码页面，停止处理")
                break
            
            # 提取文档
            api_doc = crawler._extract_api_doc(soup, url)
            if api_doc:
                # 保存文档
                crawler._save_single_markdown(api_doc)
                
                # 统计信息
                req_params = len(api_doc.request_params) + len(api_doc.query_params) + len(api_doc.body_params)
                resp_params = len(api_doc.response_params)
                
                print(f"  ✓ 成功")
                print(f"    请求参数: {req_params}, 响应参数: {resp_params}")
                success_count += 1
            else:
                print(f"  ✗ 无法提取文档")
                fail_count += 1
                
        except Exception as e:
            print(f"  ✗ 处理失败: {e}")
            fail_count += 1
    
    print("\n" + "=" * 60)
    print(f"重新生成完成!")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print("=" * 60)


def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 从命令行参数获取文档 ID
        doc_ids = sys.argv[1:]
        print(f"重新生成指定文档: {', '.join(doc_ids)}")
        regenerate_docs(doc_ids)
    else:
        print("用法:")
        print("  python3 regenerate.py [doc_id1] [doc_id2] ...")
        print()
        print("示例:")
        print("  # 重新生成单个文档")
        print("  python3 regenerate.py 95647")
        print()
        print("  # 重新生成多个文档")
        print("  python3 regenerate.py 95647 90335 90332")
        print()
        print("  # 重新生成所有文档（慎用！）")
        print("  python3 regenerate.py --all")
        print()
        
        if '--all' in sys.argv:
            confirm = input("确定要重新生成所有文档吗？(yes/no): ")
            if confirm.lower() == 'yes':
                regenerate_docs()
            else:
                print("已取消")


if __name__ == "__main__":
    main()
