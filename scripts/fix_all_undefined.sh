#!/bin/bash
# 一次性修复所有未定义的类型

set -e

PROJECT_ROOT="/Users/hysios/Projects/BlackSail/pkgs/wxwork-client"
PLACEHOLDER_FILE="$PROJECT_ROOT/types_placeholder.go"

cd "$PROJECT_ROOT"

echo "🔍 扫描所有未定义的类型..."

# 初始化占位符文件
if [ ! -f "$PLACEHOLDER_FILE" ]; then
    cat > "$PLACEHOLDER_FILE" << 'EOF'
// Code generated to fix undefined types. DO NOT EDIT manually.
// Run ./scripts/generate.sh to regenerate properly.
package wxwork

// Placeholder types for missing API definitions
// These need to be properly generated or implemented

EOF
fi

# 循环直到没有未定义的类型
MAX_ROUNDS=10
round=1

while [ $round -le $MAX_ROUNDS ]; do
    echo ""
    echo "=== Round $round ==="
    
    # 获取未定义的类型
    UNDEFINED_TYPES=$(go build . 2>&1 | grep "undefined:" | awk '{print $2}' | grep -v ":" | sort -u || true)
    
    if [ -z "$UNDEFINED_TYPES" ]; then
        echo "✅ 没有未定义的类型了！"
        break
    fi
    
    COUNT=$(echo "$UNDEFINED_TYPES" | wc -l | tr -d ' ')
    echo "发现 $COUNT 个未定义的类型，正在添加..."
    
    # 添加每个类型
    while read -r TYPE; do
        # 检查是否已存在
        if grep -q "^type $TYPE struct" "$PLACEHOLDER_FILE" 2>/dev/null; then
            continue
        fi
        
        echo "  ➕ $TYPE"
        
        if [[ $TYPE == *Request ]]; then
            cat >> "$PLACEHOLDER_FILE" << EOF
// $TYPE - Placeholder, needs proper implementation
type $TYPE struct {
	// TODO: Add proper fields
}

EOF
        elif [[ $TYPE == *Response ]]; then
            cat >> "$PLACEHOLDER_FILE" << EOF
// $TYPE - Placeholder, needs proper implementation
type $TYPE struct {
	CommonResponse
	// TODO: Add proper fields
}

EOF
        else
            # 其他类型
            cat >> "$PLACEHOLDER_FILE" << EOF
// $TYPE - Placeholder, needs proper implementation
type $TYPE struct {
	// TODO: Add proper fields
}

EOF
        fi
    done <<< "$UNDEFINED_TYPES"
    
    round=$((round + 1))
done

if [ $round -gt $MAX_ROUNDS ]; then
    echo "⚠️  达到最大轮数限制，可能还有错误"
fi

echo ""
echo "🧪 最终编译测试..."
if go build . >/dev/null 2>&1; then
    echo "✅ 编译成功！"
    echo ""
    echo "📊 占位符统计:"
    echo "   - 占位符类型数: $(grep -c "^type.*struct" "$PLACEHOLDER_FILE")"
    echo "   - 文件行数: $(wc -l < "$PLACEHOLDER_FILE")"
else
    echo "❌ 编译仍有错误:"
    go build . 2>&1 | head -20
fi
