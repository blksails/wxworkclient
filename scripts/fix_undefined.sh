#!/bin/bash
# 修复未定义类型的引用

set -e

PROJECT_ROOT="/Users/hysios/Projects/BlackSail/pkgs/wxwork-client"

echo "🔧 检查未定义的类型引用..."

# 编译并捕获错误
ERRORS=$(cd "$PROJECT_ROOT" && go build . 2>&1 | grep "undefined:" || true)

if [ -z "$ERRORS" ]; then
    echo "✅ 没有未定义的类型！"
    exit 0
fi

echo "发现以下未定义的类型:"
echo "$ERRORS"

echo ""
echo "📝 生成缺失类型的占位符..."

# 提取未定义的类型名
TYPES=$(echo "$ERRORS" | grep -o "undefined: \w\+" | awk '{print $2}' | sort -u)

# 创建占位符文件
PLACEHOLDER_FILE="$PROJECT_ROOT/types_placeholder.go"

cat > "$PLACEHOLDER_FILE" << 'EOF'
// Code generated to fix undefined types. DO NOT EDIT manually.
// Run ./scripts/generate.sh to regenerate properly.
package wxwork

// Placeholder types for missing API definitions
// These need to be properly generated or implemented

EOF

for TYPE in $TYPES; do
    if [[ $TYPE == *Request ]]; then
        echo "// $TYPE - Placeholder, needs proper implementation" >> "$PLACEHOLDER_FILE"
        echo "type $TYPE struct {" >> "$PLACEHOLDER_FILE"
        echo "	// TODO: Add proper fields" >> "$PLACEHOLDER_FILE"
        echo "}" >> "$PLACEHOLDER_FILE"
        echo "" >> "$PLACEHOLDER_FILE"
    elif [[ $TYPE == *Response ]]; then
        echo "// $TYPE - Placeholder, needs proper implementation" >> "$PLACEHOLDER_FILE"
        echo "type $TYPE struct {" >> "$PLACEHOLDER_FILE"
        echo "	CommonResponse" >> "$PLACEHOLDER_FILE"
        echo "	// TODO: Add proper fields" >> "$PLACEHOLDER_FILE"
        echo "}" >> "$PLACEHOLDER_FILE"
        echo "" >> "$PLACEHOLDER_FILE"
    fi
done

echo "✅ 创建了占位符文件: $PLACEHOLDER_FILE"
echo ""
echo "⚠️  警告: 这些是占位符类型，需要:"
echo "   1. 在 docs/api_docs/ 添加对应的 API 文档"
echo "   2. 重新运行 python3 docs/apis/build_apis_json.py"
echo "   3. 重新运行 ./scripts/generate.sh"
echo ""
echo "🧪 测试编译..."
cd "$PROJECT_ROOT" && go build . && echo "✅ 编译成功！" || echo "❌ 编译失败，请检查错误"
