# 脚本使用说明

本目录包含用于生成和集成企业微信 API Client 代码的脚本。

## 脚本列表

### 1. `generate.sh` - 生成代码

生成完整的企业微信 API Client 代码。

**用法：**
```bash
./scripts/generate.sh
```

**功能：**
- 检查 `docs/apis/apis.json` 是否存在
- 如果不存在，自动运行 `build_apis_json.py` 生成
- 运行代码生成器生成 Go 代码
- 输出生成统计信息

**输出：**
- `generated/types_generated.go` - 类型定义
- `generated/client_generated.go` - Client 方法
- `generated/impls_generated.go` - impl 结构体

---

### 2. `integrate.sh` - 集成代码（⭐ 推荐）

自动将生成的代码集成到项目中。

**用法：**
```bash
./scripts/integrate.sh
```

**功能：**
1. ✅ **自动备份** - 备份现有的生成文件到 `.backup_YYYYMMDD_HHMMSS/`
2. ✅ **复制文件** - 将 `generated/` 中的文件复制到项目根目录
3. ✅ **修改 impl.go** - 自动添加 `implsGenerated` 字段和初始化代码
4. ✅ **格式化** - 运行 `go fmt` 格式化代码
5. ✅ **编译测试** - 测试代码是否能编译通过

**修改内容：**

在 `impl.go` 中自动添加：

```go
// impls 结构体中添加
type impls struct {
    inited bool
    // ... 现有字段
    
    // Generated API implementations
    implsGenerated implsGenerated  // 👈 新增
}

// installAll 方法中添加
func (imp *impls) installAll(c *client) {
    if imp.inited {
        return
    }
    
    // ... 现有代码
    
    // Install generated implementations
    imp.implsGenerated.installAll(c)  // 👈 新增
    
    imp.inited = true
}
```

**输出示例：**
```
🔧 开始集成生成的代码...
📦 备份现有文件...
   备份目录: .backup_20260201_183000
📝 复制生成的文件...
   ✓ types_generated.go
   ✓ client_generated.go
   ✓ impls_generated.go
🔧 检查 impl.go...
   找到 impls 结构体
   ✓ implsGenerated 字段已存在
   ✓ installAll 调用已存在
🎨 格式化代码...
🧪 编译测试...
   ✅ 编译成功！

📊 集成完成统计:
   - 类型定义: 608 个 Request
   - 类型定义: 608 个 Response
   - Client 方法: 608 个
   - 总代码行数: 23953 行

✅ 集成完成！
```

**回滚：**
```bash
# 如果集成后有问题，可以回滚
cp .backup_YYYYMMDD_HHMMSS/* ./
```

---

## 完整工作流

### 首次生成和集成

```bash
# 1. 生成代码
./scripts/generate.sh

# 2. 集成到项目
./scripts/integrate.sh

# 3. 测试
go test ./...
```

### 更新 API

当有新的 API 文档时：

```bash
# 1. 更新 Markdown 文档
# 将新文档放到 docs/api_docs/

# 2. 重新生成 JSON
python3 docs/apis/build_apis_json.py --pretty

# 3. 重新生成代码
./scripts/generate.sh

# 4. 重新集成
./scripts/integrate.sh
```

### 只测试生成（不集成）

```bash
# 只生成前 10 个 API 测试
go run cmd/gencode/main.go -limit 10 -output test_generated

# 检查生成的代码
ls -lh test_generated/
```

---

## 故障排除

### 问题 1: "generated/ 目录不存在"

**解决：** 先运行 `./scripts/generate.sh`

### 问题 2: "编译出现问题"

**原因：** 可能是代码生成器有 bug 或项目结构有变化

**解决：**
1. 检查备份目录中的文件
2. 查看编译错误信息
3. 手动修复或回滚: `cp .backup_*/* ./`

### 问题 3: "权限不足"

**解决：**
```bash
chmod +x scripts/*.sh
```

### 问题 4: 想手动集成

如果不想使用自动脚本，查看 [CODEGEN.md](../CODEGEN.md) 获取手动集成步骤。

---

## 脚本维护

### 修改生成器

编辑 `cmd/gencode/main.go` 可以：
- 调整类型推断规则
- 修改命名转换逻辑
- 添加新的过滤规则

修改后重新运行生成即可。

### 自定义集成

如果项目结构不同，可以修改 `integrate.sh`：
- 调整文件路径
- 修改 `impl.go` 的查找和修改逻辑
- 添加额外的检查步骤

---

## 相关文档

- [完整文档](../CODEGEN.md)
- [生成器说明](../cmd/gencode/README.md)
- [完成报告](../generated/COMPLETION_REPORT.md)
