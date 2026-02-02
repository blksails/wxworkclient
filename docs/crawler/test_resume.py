#!/usr/bin/env python3
"""测试断点续传功能"""

from crawler import WeChatWorkAPICrawler
import time

def test_resume():
    """测试队列和断点续传"""
    
    # 创建爬虫实例（不自动加载）
    crawler = WeChatWorkAPICrawler(
        base_url="https://developer.work.weixin.qq.com",
        start_path="/document/path/91201",
        output_dir="../api_docs",
        resume=True
    )
    
    print("=" * 60)
    print("断点续传状态检查")
    print("=" * 60)
    print(f"已访问 URL 数量: {len(crawler.visited)}")
    print(f"待爬取队列大小: {len(crawler.queue)}")
    print()
    
    if crawler.queue:
        print("队列前5个 URL:")
        for i, url in enumerate(crawler.queue[:5], 1):
            print(f"  {i}. {url}")
    else:
        print("队列为空，将从起始 URL 开始")
    
    print()
    print("=" * 60)
    
    # 显示统计
    if crawler.visited:
        print("\n✓ 断点续传功能正常")
        print(f"  可以继续爬取剩余的 {len(crawler.queue)} 个 URL")
    else:
        print("\n✓ 首次运行，将从头开始爬取")

if __name__ == "__main__":
    test_resume()
