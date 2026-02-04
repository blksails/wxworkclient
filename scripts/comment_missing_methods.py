#!/usr/bin/env python3
"""
自动注释掉 Client 接口中缺失实现的方法
"""

import subprocess
import re
from pathlib import Path

def get_missing_methods():
    """获取所有缺失的方法"""
    try:
        result = subprocess.run(
            ['go', 'build', '.'],
            capture_output=True,
            text=True,
            cwd='/Users/hysios/Projects/BlackSail/pkgs/wxwork-client'
        )
        
        # 提取 missing method MethodName
        pattern = r'missing method (\w+)'
        methods = set(re.findall(pattern, result.stderr))
        return sorted(methods)
    except Exception as e:
        print(f"Error: {e}")
        return []

def comment_methods_in_interface(methods):
    """在 Client 接口中注释掉缺失的方法"""
    client_file = Path('/Users/hysios/Projects/BlackSail/pkgs/wxwork-client/client.go')
    
    content = client_file.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    modified = False
    new_lines = []
    
    for line in lines:
        # 检查是否是要注释的方法
        should_comment = False
        for method in methods:
            # 匹配方法签名，格式: MethodName(req *...Request) (*...Response, error)
            pattern = rf'^\s*{method}\s*\('
            if re.match(pattern, line):
                should_comment = True
                break
        
        if should_comment and not line.strip().startswith('//'):
            # 注释掉这一行
            indent = len(line) - len(line.lstrip())
            new_lines.append(' ' * indent + '// ' + line.strip() + ' // TODO: 缺少实现或文档')
            modified = True
            print(f"  ✓ Commented: {method}")
        else:
            new_lines.append(line)
    
    if modified:
        client_file.write_text('\n'.join(new_lines), encoding='utf-8')
        return True
    return False

def main():
    print("🔍 扫描缺失的方法...")
    
    max_rounds = 10
    round_num = 1
    
    while round_num <= max_rounds:
        methods = get_missing_methods()
        
        if not methods:
            print("\n✅ 所有缺失的方法都已处理！")
            break
        
        print(f"\n=== Round {round_num} ===")
        print(f"发现 {len(methods)} 个缺失的方法:")
        for m in methods:
            print(f"  - {m}")
        
        # 注释掉方法
        if comment_methods_in_interface(methods):
            print(f"✅ 已注释 {len(methods)} 个方法")
        
        round_num += 1
    
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
        print("❌ 编译失败:")
        print(result.stderr[:500])

if __name__ == '__main__':
    main()
