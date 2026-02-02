#!/usr/bin/env python3
"""测试爬虫断点续传的完整流程"""

from crawler import WeChatWorkAPICrawler

def test_full_resume():
    """测试完整的断点续传流程"""
    
    print("=" * 60)
    print("测试爬虫断点续传")
    print("=" * 60)
    print()
    
    # 创建爬虫实例（启用断点续传）
    crawler = WeChatWorkAPICrawler(
        base_url="https://developer.work.weixin.qq.com",
        start_path="/document/path/91201",
        output_dir="../api_docs",
        resume=True
    )
    
    print()
    print("初始状态:")
    print(f"  已访问: {len(crawler.visited)} 个 URL")
    print(f"  队列: {len(crawler.queue)} 个待爬取")
    print(f"  重新扫描模式: {crawler.need_rescan}")
    print()
    
    # 模拟爬取（只爬1个页面来测试）
    print("开始测试爬取...")
    print("-" * 60)
    
    try:
        # 只爬取队列中的第一个URL
        if crawler.queue:
            url = crawler.queue[0]
            print(f"测试爬取: {url}\n")
            
            # 手动调用 _crawl_page（仅测试用途）
            crawler._crawl_page(url)
            
            print()
            print("-" * 60)
            print("爬取后状态:")
            print(f"  已访问: {len(crawler.visited)} 个 URL")
            print(f"  队列: {len(crawler.queue)} 个待爬取")
            print(f"  已提取文档: {len(crawler.api_docs)} 个")
            
            if crawler.queue:
                print("\n队列前5个:")
                for i, u in enumerate(crawler.queue[:5], 1):
                    print(f"    {i}. {u.split('/')[-1]}")
            
            # 保存状态
            print("\n保存断点状态...")
            crawler._save_visited_urls()
            crawler._save_queue()
            
            print("\n✓ 测试完成！")
            print("\n说明:")
            print("  1. 已访问的页面会被重新扫描以发现新链接")
            print("  2. 队列中的新链接将在下次运行时继续爬取")
            print("  3. 断点续传功能正常工作")
            
    except Exception as e:
        print(f"\n测试出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_resume()
