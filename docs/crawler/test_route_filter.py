#!/usr/bin/env python3
"""测试路由过滤功能"""

from bs4 import BeautifulSoup

# 模拟企业微信文档的路由导航 HTML
html_sample = """
<div class="ep-route-dir">
    <div class="ep-route-dir-item">
        <span>第三方应用开发</span>
        <svg width="7" height="10" viewBox="0 0 7 10" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M1.24264 1.00004L5.48528 5.24268L1.24264 9.48532" stroke="var(--ww_base_gray_060)" stroke-opacity="0.5"></path>
        </svg>
    </div>
    <div class="ep-route-dir-item">
        <span>服务端API</span>
        <svg width="7" height="10" viewBox="0 0 7 10" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M1.24264 1.00004L5.48528 5.24268L1.24264 9.48532" stroke="var(--ww_base_gray_060)" stroke-opacity="0.5"></path>
        </svg>
    </div>
    <div class="ep-route-dir-item">
        <span>推广二维码</span>
        <svg width="7" height="10" viewBox="0 0 7 10" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M1.24264 1.00004L5.48528 5.24268L1.24264 9.48532" stroke="var(--ww_base_gray_060)" stroke-opacity="0.5"></path>
        </svg>
    </div>
    <div class="ep-route-dir-item">
        <span>调用接口</span>
        <svg width="7" height="10" viewBox="0 0 7 10" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M1.24264 1.00004L5.48528 5.24268L1.24264 9.48532" stroke="var(--ww_base_gray_060)" stroke-opacity="0.5"></path>
        </svg>
    </div>
    <div class="ep-route-dir-item">
        <span>获取注册码</span>
    </div>
</div>
"""

def extract_route_path(soup: BeautifulSoup):
    """提取路由路径"""
    route_path = []
    try:
        route_dir = soup.find('div', class_='ep-route-dir')
        if route_dir:
            route_items = route_dir.find_all('div', class_='ep-route-dir-item')
            for item in route_items:
                span = item.find('span')
                if span and span.text:
                    route_path.append(span.text.strip())
    except Exception as e:
        print(f"解析路由失败: {e}")
    
    return route_path

def test_route_extraction():
    """测试路由提取"""
    print("=" * 60)
    print("测试路由提取功能")
    print("=" * 60)
    
    soup = BeautifulSoup(html_sample, 'html.parser')
    route_path = extract_route_path(soup)
    
    print(f"\n提取的路由路径: {route_path}")
    print(f"路由字符串: {' > '.join(route_path)}")
    
    # 测试包含过滤器
    print("\n" + "=" * 60)
    print("测试路由包含过滤器 (--route-filter)")
    print("=" * 60)
    
    test_filters = [
        ("服务端API", True),
        ("客户端API", False),
        ("推广二维码", True),
        ("第三方应用开发", True),
    ]
    
    for filter_keyword, expected in test_filters:
        result = filter_keyword in route_path
        status = "✓" if result == expected else "✗"
        result_text = "匹配" if result else "不匹配"
        print(f"{status} 包含过滤 '{filter_keyword}': {result_text} (预期: {'匹配' if expected else '不匹配'})")
    
    # 测试排除过滤器
    print("\n" + "=" * 60)
    print("测试路由排除过滤器 (--route-exclude)")
    print("=" * 60)
    
    test_excludes = [
        ("服务商代开发", False),  # 不包含，所以不应该被排除
        ("第三方应用开发", True),  # 包含，应该被排除
        ("服务端API", True),       # 包含，应该被排除
    ]
    
    for exclude_keyword, should_exclude in test_excludes:
        result = exclude_keyword in route_path
        status = "✓" if result == should_exclude else "✗"
        result_text = "会被排除" if result else "不会被排除"
        print(f"{status} 排除过滤 '{exclude_keyword}': {result_text} (预期: {'会被排除' if should_exclude else '不会被排除'})")
    
    # 测试 AND 逻辑匹配
    print("\n" + "=" * 60)
    print("测试 AND 逻辑匹配 (--route-filter)")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "AND逻辑 - 同时包含所有关键词",
            "route": ['第三方应用开发', '服务端API', '推广二维码'],
            "filters": ["第三方应用开发", "服务端API"],
            "excludes": ["服务商代开发"],
            "expected": True,
        },
        {
            "name": "AND逻辑 - 只包含第一个关键词",
            "route": ['第三方应用开发', '客户端API', '账号授权'],
            "filters": ["第三方应用开发", "服务端API"],
            "excludes": ["服务商代开发"],
            "expected": False,
        },
        {
            "name": "AND逻辑 - 只包含第二个关键词",
            "route": ['企业内部开发', '服务端API', '通讯录管理'],
            "filters": ["第三方应用开发", "服务端API"],
            "excludes": ["服务商代开发"],
            "expected": False,
        },
        {
            "name": "AND逻辑 - 都不包含",
            "route": ['企业内部开发', '客户端API', '账号授权'],
            "filters": ["第三方应用开发", "服务端API"],
            "excludes": ["服务商代开发"],
            "expected": False,
        },
        {
            "name": "AND逻辑 - 同时包含但命中排除",
            "route": ['第三方应用开发', '服务端API', '服务商代开发'],
            "filters": ["第三方应用开发", "服务端API"],
            "excludes": ["服务商代开发"],
            "expected": False,
        },
        {
            "name": "三个关键词 - 全部匹配",
            "route": ['第三方应用开发', '服务端API', '推广二维码', '调用接口'],
            "filters": ["第三方应用开发", "服务端API", "推广二维码"],
            "excludes": [],
            "expected": True,
        },
        {
            "name": "三个关键词 - 缺少一个",
            "route": ['第三方应用开发', '服务端API', '通讯录管理'],
            "filters": ["第三方应用开发", "服务端API", "推广二维码"],
            "excludes": [],
            "expected": False,
        },
        {
            "name": "多个排除过滤器 - 命中第一个",
            "route": ['第三方应用开发', '服务端API', '服务商代开发'],
            "filters": ["第三方应用开发", "服务端API"],
            "excludes": ["服务商代开发", "已废弃"],
            "expected": False,
        },
        {
            "name": "多个排除过滤器 - 命中第二个",
            "route": ['第三方应用开发', '服务端API', '已废弃'],
            "filters": ["第三方应用开发", "服务端API"],
            "excludes": ["服务商代开发", "已废弃"],
            "expected": False,
        },
        {
            "name": "多个排除过滤器 - 都不命中",
            "route": ['第三方应用开发', '服务端API', '推广二维码'],
            "filters": ["第三方应用开发", "服务端API"],
            "excludes": ["服务商代开发", "已废弃"],
            "expected": True,
        },
    ]
    
    for case in test_cases:
        route = case['route']
        filters = case['filters']
        excludes = case['excludes']
        
        # 逻辑：必须包含filters中的所有关键词(AND)，且不能包含excludes中的任意一个(OR)
        filter_match = all(f in route for f in filters)
        exclude_match = any(e in route for e in excludes) if excludes else False
        should_pass = filter_match and not exclude_match
        
        status = "✓" if should_pass == case['expected'] else "✗"
        result_text = "通过" if should_pass else "被过滤"
        missing = [f for f in filters if f not in route]
        
        print(f"\n{status} {case['name']}")
        print(f"   路由: {' > '.join(route)}")
        print(f"   包含过滤 (AND): {filters} → {'全部匹配' if filter_match else f'缺少 {missing}'}")
        if excludes:
            print(f"   排除过滤 (OR): {excludes} → {'命中' if exclude_match else '不命中'}")
        print(f"   结果: {result_text} (预期: {'通过' if case['expected'] else '被过滤'})")

if __name__ == '__main__':
    test_route_extraction()
