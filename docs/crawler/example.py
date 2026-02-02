#!/usr/bin/env python3
"""
使用示例：自定义爬虫配置
"""

from crawler import WeChatWorkAPICrawler


def example_basic():
    """基础用法示例"""
    print("=== 基础用法示例 ===\n")
    
    crawler = WeChatWorkAPICrawler(
        base_url="https://developer.work.weixin.qq.com",
        start_path="/document/path/91201",
        output_dir="../api_docs",
        resume=True  # 启用断点续爬
    )
    
    crawler.crawl()


def example_custom_path():
    """自定义起始路径示例"""
    print("=== 自定义起始路径示例 ===\n")
    
    # 例如：只爬取通讯录管理相关的 API
    crawler = WeChatWorkAPICrawler(
        base_url="https://developer.work.weixin.qq.com",
        start_path="/document/path/90194",  # 通讯录管理
        output_dir="../api_docs_contacts",
        resume=True
    )
    
    crawler.crawl()


def example_fresh_start():
    """从头开始爬取（禁用断点续爬）"""
    print("=== 从头开始爬取示例 ===\n")
    
    crawler = WeChatWorkAPICrawler(
        base_url="https://developer.work.weixin.qq.com",
        start_path="/document/path/91201",
        output_dir="../api_docs_fresh",
        resume=False  # 禁用断点续爬，从头开始
    )
    
    crawler.crawl()


def example_multiple_sections():
    """爬取多个章节示例"""
    print("=== 爬取多个章节示例 ===\n")
    
    sections = [
        ("/document/path/90194", "../api_docs_contacts"),     # 通讯录管理
        ("/document/path/90664", "../api_docs_messages"),     # 消息推送
        ("/document/path/90313", "../api_docs_auth"),         # 身份验证
    ]
    
    for start_path, output_dir in sections:
        print(f"\n正在爬取章节: {start_path}")
        crawler = WeChatWorkAPICrawler(
            base_url="https://developer.work.weixin.qq.com",
            start_path=start_path,
            output_dir=output_dir,
            resume=True
        )
        crawler.crawl()
        print(f"章节 {start_path} 爬取完成\n")


if __name__ == "__main__":
    # 运行基础示例
    example_basic()
    
    # 取消注释以运行其他示例：
    # example_custom_path()
    # example_fresh_start()
    # example_multiple_sections()
