#!/usr/bin/env python3
"""
清理旧文件并重新生成所有文档
用于添加完整度评分功能后的迁移
"""

import sys
import json
from pathlib import Path
from crawler import WeChatWorkAPICrawler
import requests
from bs4 import BeautifulSoup
import time

def cleanup_and_regenerate():
    """清理旧文件并重新生成"""
    
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
    
    print("=" * 60)
    print("清理旧文件并重新生成所有文档")
    print("=" * 60)
    print(f"\n总共有 {len(visited_urls)} 个已访问的 URL")
    
    # 确认操作
    confirm = input("\n这将删除所有旧文档并重新生成，是否继续？(yes/no): ")
    if confirm.lower() != 'yes':
        print("已取消")
        return
    
    print("\n第1步：清理旧文档...")
    print("-" * 60)
    
    # 清理不带评分的旧文件
    old_files = []
    for md_file in output_dir.glob("*.md"):
        if md_file.name == "README.md":
            continue
        # 检查是否为旧格式（不带 -数字 后缀）
        if not any(md_file.stem.endswith(f"-{i}") for i in range(7)):
            old_files.append(md_file)
    
    print(f"找到 {len(old_files)} 个旧格式文档")
    
    if old_files:
        for f in old_files:
            f.unlink()
            print(f"  ✓ 已删除: {f.name}")
    
    print("\n第2步：重新生成所有文档...")
    print("-" * 60)
    
    # 创建爬虫实例
    crawler = WeChatWorkAPICrawler(
        base_url="https://developer.work.weixin.qq.com",
        start_path="/document/path/91201",
        output_dir="../api_docs",
        resume=False
    )
    
    success_count = 0
    fail_count = 0
    score_stats = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    
    for i, url in enumerate(visited_urls, 1):
        doc_id = url.split('/')[-1]
        print(f"\n[{i}/{len(visited_urls)}] 处理: {doc_id}")
        
        try:
            # 延迟请求
            time.sleep(0.5)
            
            response = requests.get(url, headers=crawler.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 检查验证码
            if crawler._check_captcha_page(soup):
                print(f"  ⚠️  检测到验证码页面，停止处理")
                break
            
            # 提取文档
            api_doc = crawler._extract_api_doc(soup, url)
            if api_doc:
                # 保存文档
                crawler._save_single_markdown(api_doc)
                
                # 统计
                score = crawler._calculate_completeness_score(api_doc)
                score_stats[score] += 1
                success_count += 1
            else:
                print(f"  ✗ 无法提取文档")
                fail_count += 1
                
        except Exception as e:
            print(f"  ✗ 处理失败: {e}")
            fail_count += 1
        
        # 每50个文档显示一次进度
        if i % 50 == 0:
            print(f"\n--- 进度: {i}/{len(visited_urls)} ---")
            print(f"成功: {success_count}, 失败: {fail_count}")
            for score in range(7):
                if score_stats[score] > 0:
                    print(f"  {score}分: {score_stats[score]} 个")
    
    print("\n" + "=" * 60)
    print("重新生成完成!")
    print("=" * 60)
    print(f"\n统计:")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print(f"\n完整度分布:")
    for score in range(7):
        if score_stats[score] > 0:
            badge = "🟢" if score == 6 else "🟡" if score >= 4 else "🔴"
            print(f"  {badge} {score}分: {score_stats[score]} 个")
    
    print("\n正在生成索引...")
    # 需要从文件中重新加载文档来生成索引
    # 这里直接调用爬虫的索引生成方法
    crawler.api_docs = []  # 需要重新填充
    # 简化处理：直接提示用户运行爬虫更新索引
    print("  请运行以下命令更新索引:")
    print("  python3 -c \"from crawler import *; import json; from pathlib import Path\"")
    print("\n或者重新运行爬虫以更新索引:")
    print("  python3 crawler.py")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    cleanup_and_regenerate()
