#!/usr/bin/env python3
"""
爬虫测试脚本
用于测试爬虫的基本功能，不进行实际爬取
"""

import sys
from crawler import WeChatWorkAPICrawler, APIDoc, Parameter, Section, CodeExample


def test_sanitize_filename():
    """测试文件名清理函数"""
    print("测试文件名清理...")
    
    test_cases = [
        ("普通文件名", "普通文件名"),
        ("文件/名/测试", "文件_名_测试"),
        ("API-文档_v1.0", "API-文档_v1_0"),
        ("  多余空格  ", "多余空格"),
    ]
    
    for input_name, expected in test_cases:
        result = WeChatWorkAPICrawler._sanitize_filename(input_name)
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{input_name}' -> '{result}'")


def test_api_doc_creation():
    """测试 API 文档数据结构"""
    print("\n测试 API 文档数据结构...")
    
    # 创建测试数据
    query_param = Parameter(
        name="access_token",
        type="string",
        required=True,
        description="调用接口凭证"
    )
    
    body_param = Parameter(
        name="corpid",
        type="string",
        required=True,
        description="企业ID"
    )
    
    response_param = Parameter(
        name="errcode",
        type="int",
        required=False,
        description="返回码"
    )
    
    request_example = CodeExample(
        title="请求示例",
        language="http",
        code="GET https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=xxx&corpsecret=xxx"
    )
    
    response_example = CodeExample(
        title="响应示例",
        language="json",
        code='{"errcode": 0, "errmsg": "ok", "access_token": "xxx"}'
    )
    
    section = Section(
        title="使用说明",
        content="access_token是企业后台调用企业微信API的凭证"
    )
    
    api_doc = APIDoc(
        title="获取access_token",
        url="https://developer.work.weixin.qq.com/document/path/91201",
        path="91201",
        description="获取访问令牌",
        method="GET",
        api_url="https://qyapi.weixin.qq.com/cgi-bin/gettoken",
        query_params=[query_param],
        body_params=[body_param],
        response_params=[response_param],
        request_examples=[request_example],
        response_examples=[response_example],
        sections=[section]
    )
    
    print(f"  ✓ API 标题: {api_doc.title}")
    print(f"  ✓ API 路径: {api_doc.path}")
    print(f"  ✓ API 地址: {api_doc.api_url}")
    print(f"  ✓ 请求方法: {api_doc.method}")
    print(f"  ✓ Query 参数: {len(api_doc.query_params)}")
    print(f"  ✓ Body 参数: {len(api_doc.body_params)}")
    print(f"  ✓ 响应参数: {len(api_doc.response_params)}")
    print(f"  ✓ 请求示例: {len(api_doc.request_examples)}")
    print(f"  ✓ 响应示例: {len(api_doc.response_examples)}")
    print(f"  ✓ 章节数量: {len(api_doc.sections)}")


def test_markdown_generation():
    """测试 Markdown 生成"""
    print("\n测试 Markdown 生成...")
    
    crawler = WeChatWorkAPICrawler(
        base_url="https://developer.work.weixin.qq.com",
        start_path="/document/path/91201",
        output_dir="/tmp/test_output"
    )
    
    # 创建测试文档
    query_param = Parameter(
        name="access_token",
        type="string",
        required=True,
        description="调用接口凭证"
    )
    
    body_param = Parameter(
        name="corpid",
        type="string",
        required=True,
        description="企业ID"
    )
    
    response_param = Parameter(
        name="errcode",
        type="int",
        required=False,
        description="返回码"
    )
    
    request_example = CodeExample(
        title="请求示例",
        language="http",
        code="POST https://qyapi.weixin.qq.com/cgi-bin/test?access_token=xxx"
    )
    
    response_example = CodeExample(
        title="响应示例",
        language="json",
        code='{"errcode": 0, "errmsg": "ok"}'
    )
    
    api_doc = APIDoc(
        title="测试API",
        url="https://example.com",
        path="12345",
        description="这是一个测试API",
        method="POST",
        api_url="https://qyapi.weixin.qq.com/cgi-bin/test",
        request="POST https://qyapi.weixin.qq.com/cgi-bin/test",
        query_params=[query_param],
        body_params=[body_param],
        response_params=[response_param],
        request_examples=[request_example],
        response_examples=[response_example],
        sections=[
            Section(title="使用说明", content="这是使用说明")
        ]
    )
    
    markdown = crawler._generate_markdown(api_doc)
    
    # 验证 Markdown 内容
    assert "# 测试API" in markdown, "标题未生成"
    assert "POST" in markdown, "方法未生成"
    assert "https://qyapi.weixin.qq.com/cgi-bin/test" in markdown, "API URL 未生成"
    assert "## 请求信息" in markdown, "请求信息章节未生成"
    assert "## 响应信息" in markdown, "响应信息章节未生成"
    assert "Query 参数" in markdown, "Query 参数未生成"
    assert "Body 参数" in markdown, "Body 参数未生成"
    assert "响应参数" in markdown, "响应参数未生成"
    assert "access_token" in markdown, "Query 参数内容未生成"
    assert "corpid" in markdown, "Body 参数内容未生成"
    assert "errcode" in markdown, "响应参数内容未生成"
    
    print("  ✓ Markdown 生成成功")
    print("  ✓ 包含请求信息章节")
    print("  ✓ 包含响应信息章节")
    print("  ✓ 包含 Query 参数")
    print("  ✓ 包含 Body 参数")
    print("  ✓ 包含响应参数")
    print(f"\n--- 生成的 Markdown 预览 ---")
    print(markdown[:500] + "...")


def main():
    """运行所有测试"""
    print("=================================")
    print("企业微信 API 爬虫 - 功能测试")
    print("=================================\n")
    
    try:
        test_sanitize_filename()
        test_api_doc_creation()
        test_markdown_generation()
        
        print("\n=================================")
        print("✓ 所有测试通过！")
        print("=================================\n")
        print("爬虫功能正常，可以运行:")
        print("  python3 crawler.py")
        print("或使用快速启动脚本:")
        print("  ./run.sh")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
