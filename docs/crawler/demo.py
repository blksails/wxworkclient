#!/usr/bin/env python3
"""
演示脚本：展示实时保存和断点续爬功能
仅爬取几个页面作为演示
"""

import sys
from crawler import WeChatWorkAPICrawler


def demo_realtime_save():
    """演示实时保存功能"""
    print("=" * 60)
    print("演示：实时保存和断点续爬功能")
    print("=" * 60)
    print()
    print("这个演示将：")
    print("1. 从企业微信 API 文档开始爬取")
    print("2. 每提取一个接口立即保存 Markdown 文件")
    print("3. 实时更新索引文件")
    print("4. 记录访问过的 URL")
    print()
    print("提示：你可以随时按 Ctrl+C 中断，重新运行会继续爬取！")
    print("=" * 60)
    print()
    
    # 创建爬虫实例
    crawler = WeChatWorkAPICrawler(
        base_url="https://developer.work.weixin.qq.com",
        start_path="/document/path/91201",
        output_dir="../api_docs_demo",
        resume=True  # 启用断点续爬
    )
    
    try:
        # 开始爬取
        crawler.crawl()
        
        print("\n" + "=" * 60)
        print("演示完成！")
        print("=" * 60)
        print()
        print("查看结果：")
        print(f"  索引文件: {crawler.output_dir}/README.md")
        print(f"  API 文档: {crawler.output_dir}/*.md")
        print(f"  完整数据: {crawler.output_dir}/api_docs.json")
        print(f"  访问记录: {crawler.output_dir}/.visited_urls.json")
        print()
        print("💡 提示：你可以重新运行此演示脚本，它会跳过已爬取的内容！")
        
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("爬取已中断！")
        print("=" * 60)
        print()
        print(f"已爬取 {len(crawler.api_docs)} 个 API 文档")
        print("所有已提取的文档都已保存 ✓")
        print()
        print("💡 重新运行此脚本将从中断处继续爬取：")
        print("  python3 demo.py")
        print()
        print("或者从头开始：")
        print("  python3 demo.py --no-resume")
        
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(demo_realtime_save())
