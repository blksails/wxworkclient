#!/usr/bin/env python3
"""从已访问的 URL 中重建队列"""

import json
from pathlib import Path

def create_queue_from_visited():
    """从已访问的 URL 中找出所有链接，创建待爬取队列"""
    
    output_dir = Path("../api_docs")
    visited_file = output_dir / '.visited_urls.json'
    queue_file = output_dir / '.crawl_queue.json'
    
    if not visited_file.exists():
        print("错误: 找不到已访问的 URL 文件")
        return
    
    # 加载已访问的 URL
    with open(visited_file, 'r') as f:
        data = json.load(f)
        visited = set(data.get('visited', []))
    
    print(f"已加载 {len(visited)} 个已访问的 URL")
    
    # 创建一个空队列
    # 因为我们不知道还有哪些 URL 未访问，所以需要从某个页面重新扫描
    # 这里我们创建一个空队列，让爬虫从起始 URL 重新扫描链接
    queue = []
    
    # 保存队列
    with open(queue_file, 'w') as f:
        json.dump({
            'queue': queue,
            'timestamp': '2024-12-10',
            'queue_size': len(queue),
            'note': '空队列，爬虫将从已访问页面中查找新链接'
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 已创建队列文件: {queue_file}")
    print(f"  队列大小: {len(queue)}")
    print("\n说明: 由于无法从已访问 URL 推断出未访问的 URL，")
    print("      爬虫将在运行时动态发现新链接")

if __name__ == "__main__":
    create_queue_from_visited()
