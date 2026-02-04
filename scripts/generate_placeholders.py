#!/usr/bin/env python3
"""
从编译错误中提取所有未定义的类型并生成占位符
"""

import subprocess
import re
from pathlib import Path

def get_undefined_types():
    """获取所有未定义的类型"""
    try:
        result = subprocess.run(
            ['go', 'build', '.'],
            capture_output=True,
            text=True,
            cwd='/Users/hysios/Projects/BlackSail/pkgs/wxwork-client'
        )
        
        # 提取 undefined: TypeName
        pattern = r'undefined:\s+(\w+)'
        types = set(re.findall(pattern, result.stderr))
        return sorted(types)
    except Exception as e:
        print(f"Error: {e}")
        return []

def generate_placeholder(typename):
    """生成占位符类型定义"""
    if typename.endswith('Request'):
        return f"""// {typename} - Placeholder, needs proper implementation
type {typename} struct {{
	// TODO: Add proper fields from docs/api_docs/
}}

"""
    elif typename.endswith('Response'):
        return f"""// {typename} - Placeholder, needs proper implementation
type {typename} struct {{
	CommonResponse
	// TODO: Add proper fields from docs/api_docs/
}}

"""
    else:
        return f"""// {typename} - Placeholder
type {typename} struct {{
	// TODO: Define proper structure
}}

"""

def main():
    print("🔍 扫描未定义的类型...")
    
    types = get_undefined_types()
    
    if not types:
        print("✅ 没有未定义的类型！")
        return
    
    print(f"发现 {len(types)} 个未定义的类型:")
    for t in types:
        print(f"  - {t}")
    
    # 生成占位符文件
    placeholder_file = Path('/Users/hysios/Projects/BlackSail/pkgs/wxwork-client/types_placeholder.go')
    
    # 读取已存在的类型
    existing_types = set()
    if placeholder_file.exists():
        content = placeholder_file.read_text(encoding='utf-8')
        existing_types = set(re.findall(r'^type\s+(\w+)\s+struct', content, re.MULTILINE))
    
    # 过滤掉已存在的类型
    new_types = [t for t in types if t not in existing_types]
    
    if not new_types:
        print("✅ 所有类型都已存在占位符！")
        return
    
    print(f"\n新增 {len(new_types)} 个占位符:")
    for t in new_types:
        print(f"  + {t}")
    
    # 追加新类型
    if not placeholder_file.exists():
        with open(placeholder_file, 'w', encoding='utf-8') as f:
            f.write("""// Code generated to fix undefined types. DO NOT EDIT manually.
// Run ./scripts/generate.sh to regenerate properly.
package wxwork

// ⚠️ WARNING: These are placeholder types
// They need to be properly implemented by:
//   1. Adding corresponding API docs to docs/api_docs/
//   2. Running: python3 docs/apis/build_apis_json.py
//   3. Running: ./scripts/generate.sh

""")
    
    with open(placeholder_file, 'a', encoding='utf-8') as f:
        for typename in new_types:
            f.write(generate_placeholder(typename))
    
    print(f"\n✅ 生成了 {len(types)} 个占位符类型")
    print(f"📁 文件: {placeholder_file}")
    
    # 测试编译
    print("\n🧪 测试编译...")
    result = subprocess.run(
        ['go', 'build', '.'],
        capture_output=True,
        text=True,
        cwd='/Users/hysios/Projects/BlackSail/pkgs/wxwork-client'
    )
    
    if result.returncode == 0:
        print("✅ 编译成功！")
    else:
        remaining = len(re.findall(r'undefined:', result.stderr))
        if remaining > 0:
            print(f"⚠️  还有 {remaining} 个未定义的类型，重新运行脚本")
        else:
            print("❌ 编译失败:")
            print(result.stderr[:500])

if __name__ == '__main__':
    main()
