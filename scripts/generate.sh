#!/bin/bash
# 生成企业微信 API Client 代码

set -e

echo "🚀 开始生成企业微信 API Client 代码..."

# 确保 APIs JSON 是最新的
echo "📝 检查 APIs JSON..."
if [ ! -f "docs/apis/apis.json" ]; then
    echo "⚠️  APIs JSON 不存在，正在生成..."
    python3 docs/apis/build_apis_json.py
fi

# 生成代码
echo "🔨 生成 Go 代码..."
go run cmd/gencode/main.go \
    -input docs/apis/apis.json \
    -output generated \
    -package wxwork

echo "✅ 代码生成完成！"
echo "📁 生成的文件："
echo "   - generated/types_generated.go"
echo "   - generated/client_generated.go"
echo ""
echo "💡 使用提示："
echo "   1. 查看生成的类型定义：generated/types_generated.go"
echo "   2. 查看生成的 Client 方法：generated/client_generated.go"
echo "   3. 手动集成到项目中或进一步修改"
