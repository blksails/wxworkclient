#!/bin/bash
# 一次性添加所有缺失的类型

PLACEHOLDER_FILE="/Users/hysios/Projects/BlackSail/pkgs/wxwork-client/types_placeholder.go"

# 缺失的类型列表
MISSING_TYPES=(
    "ChatdataKeywordDeleteRuleRequest"
    "ChatdataKeywordDeleteRuleResponse"
    "ChatdataKeywordGetHitMsgListRequest"
    "ChatdataKeywordGetHitMsgListResponse"
    "ChatdataSyncMsgRequest"
    "ChatdataSyncMsgResponse"
    "CorpgroupCorpRemoveCorpResponse"
    "GettokenRequest"
    "GettokenResponse"
    "SyncContactSyncSuccessResponse"
)

echo "📝 添加缺失的类型到 types_placeholder.go..."

for TYPE in "${MISSING_TYPES[@]}"; do
    # 检查类型是否已存在
    if grep -q "type $TYPE struct" "$PLACEHOLDER_FILE" 2>/dev/null; then
        echo "  ⏭️  $TYPE 已存在"
        continue
    fi
    
    echo "  ➕ 添加 $TYPE"
    
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
    fi
done

echo "✅ 完成！"
echo ""
echo "🧪 测试编译..."
cd /Users/hysios/Projects/BlackSail/pkgs/wxwork-client && go build . && echo "✅ 编译成功！" || echo "❌ 编译仍有错误"
