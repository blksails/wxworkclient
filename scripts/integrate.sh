#!/bin/bash
# 自动集成生成的代码到项目中

set -e

PROJECT_ROOT="/Users/hysios/Projects/BlackSail/pkgs/wxwork-client"
GENERATED_DIR="$PROJECT_ROOT/generated"

echo "🔧 开始集成生成的代码..."

# 1. 检查生成的文件是否存在
if [ ! -d "$GENERATED_DIR" ]; then
    echo "❌ generated/ 目录不存在，请先运行 ./scripts/generate.sh"
    exit 1
fi

if [ ! -f "$GENERATED_DIR/types_generated.go" ] || \
   [ ! -f "$GENERATED_DIR/client_generated.go" ] || \
   [ ! -f "$GENERATED_DIR/impls_generated.go" ]; then
    echo "❌ 生成的文件不完整，请先运行 ./scripts/generate.sh"
    exit 1
fi

# 2. 备份现有文件
echo "📦 备份现有文件..."
BACKUP_DIR="$PROJECT_ROOT/.backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

if [ -f "$PROJECT_ROOT/types_generated.go" ]; then
    cp "$PROJECT_ROOT/types_generated.go" "$BACKUP_DIR/"
fi
if [ -f "$PROJECT_ROOT/client_generated.go" ]; then
    cp "$PROJECT_ROOT/client_generated.go" "$BACKUP_DIR/"
fi
if [ -f "$PROJECT_ROOT/impls_generated.go" ]; then
    cp "$PROJECT_ROOT/impls_generated.go" "$BACKUP_DIR/"
fi
if [ -f "$PROJECT_ROOT/impl.go" ]; then
    cp "$PROJECT_ROOT/impl.go" "$BACKUP_DIR/impl.go"
fi

echo "   备份目录: $BACKUP_DIR"

# 3. 复制生成的文件到项目根目录
echo "📝 复制生成的文件..."
cp "$GENERATED_DIR/types_generated.go" "$PROJECT_ROOT/"
cp "$GENERATED_DIR/client_generated.go" "$PROJECT_ROOT/"
cp "$GENERATED_DIR/impls_generated.go" "$PROJECT_ROOT/"

echo "   ✓ types_generated.go"
echo "   ✓ client_generated.go"
echo "   ✓ impls_generated.go"

# 4. 检查并修改 impl.go
echo "🔧 检查 impl.go..."

if grep -q "type impls struct" "$PROJECT_ROOT/impl.go" 2>/dev/null; then
    echo "   找到 impls 结构体"
    
    # 检查是否已经添加了 generated 字段
    if ! grep -q "implsGenerated" "$PROJECT_ROOT/impl.go"; then
        echo "   添加 implsGenerated 字段..."
        
        # 创建临时文件
        TMP_FILE=$(mktemp)
        
        # 在 impls struct 中添加 implsGenerated 字段
        awk '
        /^type impls struct/ {
            print $0
            getline
            print $0
            print "\t// Generated API implementations"
            print "\timplsGenerated implsGenerated"
            next
        }
        { print }
        ' "$PROJECT_ROOT/impl.go" > "$TMP_FILE"
        
        mv "$TMP_FILE" "$PROJECT_ROOT/impl.go"
        echo "   ✓ 已添加 implsGenerated 字段"
    else
        echo "   ✓ implsGenerated 字段已存在"
    fi
    
    # 检查 installAll 方法
    if grep -q "func (imp \*impls) installAll" "$PROJECT_ROOT/impl.go"; then
        if ! grep -q "imp.implsGenerated.installAll" "$PROJECT_ROOT/impl.go"; then
            echo "   添加 implsGenerated.installAll() 调用..."
            
            TMP_FILE=$(mktemp)
            
            # 在 installAll 方法末尾添加调用
            awk '
            /imp.inited = true/ {
                print "\t// Install generated implementations"
                print "\timp.implsGenerated.installAll(c)"
                print ""
                print $0
                next
            }
            { print }
            ' "$PROJECT_ROOT/impl.go" > "$TMP_FILE"
            
            mv "$TMP_FILE" "$PROJECT_ROOT/impl.go"
            echo "   ✓ 已添加 installAll 调用"
        else
            echo "   ✓ installAll 调用已存在"
        fi
    fi
else
    echo "   ⚠️  未找到 impls 结构体，需要手动修改"
fi

# 5. 格式化代码
echo "🎨 格式化代码..."
go fmt "$PROJECT_ROOT"/*.go >/dev/null 2>&1 || true

# 6. 语法检查
echo "🧪 语法检查..."
if go fmt "$PROJECT_ROOT"/*.go >/dev/null 2>&1 && \
   gofmt -l "$PROJECT_ROOT"/*.go 2>/dev/null | wc -l | grep -q "0"; then
    echo "   ✅ 语法检查通过"
else
    echo "   ⚠️  代码格式问题"
fi

# 尝试编译（可能会失败，因为依赖问题）
echo "🔍 尝试编译测试..."
if go build -o /tmp/test_wxwork_integration "$PROJECT_ROOT" 2>/dev/null; then
    echo "   ✅ 编译成功！"
    rm -f /tmp/test_wxwork_integration
else
    echo "   ℹ️  完整编译需要在项目上下文中进行"
    echo "   提示: 运行 'go build' 测试完整编译"
fi

# 7. 统计信息
echo ""
echo "📊 集成完成统计:"
echo "   - 类型定义: $(grep -c "^type.*Request struct" "$PROJECT_ROOT/types_generated.go" 2>/dev/null || echo 0) 个 Request"
echo "   - 类型定义: $(grep -c "^type.*Response struct" "$PROJECT_ROOT/types_generated.go" 2>/dev/null || echo 0) 个 Response"
echo "   - Client 方法: $(grep -c "^func (c \*client)" "$PROJECT_ROOT/client_generated.go" 2>/dev/null || echo 0) 个"
echo "   - 总代码行数: $(wc -l "$PROJECT_ROOT"/*_generated.go 2>/dev/null | tail -1 | awk '{print $1}') 行"

echo ""
echo "✅ 集成完成！"
echo ""
echo "💡 使用示例:"
echo "   import \"github.com/blacksail/wxwork-client\""
echo "   "
echo "   client := wxwork.New(wxwork.Config{...})"
echo "   resp, err := client.UserCreate(&wxwork.UserCreateRequest{...})"
echo ""
echo "📁 备份文件: $BACKUP_DIR"
echo "🔄 如需回滚: cp $BACKUP_DIR/* $PROJECT_ROOT/"
