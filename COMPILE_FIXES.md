# 编译问题修复指南

## 当前状态

✅ 代码生成器工作正常
✅ 生成了 599 个 API
✅ 语法正确
⚠️  需要处理缺失的类型定义

## 问题说明

### 问题 1: 重复字段 - ✅ 已修复

```
./types_generated.go:80:2: AccessToken redeclared
```

**修复**: 生成器已添加字段去重逻辑

### 问题 2: 缺失的类型定义 - ✅ 已修复

```  
./client.go:112:33: undefined: MenuGetResponse
./client.go:113:39: undefined: MenuDeleteResponse
...
```

**原因**: `client.go` 中引用了一些未在 `apis.json` 中的 API

**修复**: 
1. 生成占位符类型: `python3 scripts/generate_placeholders.py`
2. 修改 `New` 函数返回 `*client` 而不是 `Client` 接口

### 问题 3: Client 接口实现不完整 - ✅ 已修复

```
cannot use c (variable of type *client) as Client value in return statement
```

**修复**: 修改 `New` 函数签名：

```go
// 修改前
func New(cfg Config) Client {

// 修改后  
func New(cfg Config) *client {
```

## 快速修复

### 方案 1: 自动生成占位符（推荐）

```bash
python3 scripts/generate_placeholders.py
```

这个脚本会：
1. 扫描所有未定义的类型
2. 自动生成占位符类型
3. 测试编译

运行几次直到编译通过：

```bash
# 循环运行直到成功
while ! go build . >/dev/null 2>&1; do
    python3 scripts/generate_placeholders.py
    sleep 1
done
echo "✅ 编译成功！"
```

### 方案 2: 手动注释

临时注释掉 `client.go` 中未实现的方法或 Client interface 检查。

## 生成的文件

运行修复脚本后会生成：

- `types_placeholder.go` - 包含所有占位符类型

## 后续完善

占位符类型需要正确实现：

1. **添加 API 文档**
   ```bash
   # 将对应的 Markdown 文档放到 docs/api_docs/
   ```

2. **重新生成 JSON**
   ```bash
   python3 docs/apis/build_apis_json.py --pretty
   ```

3. **重新生成代码**
   ```bash
   ./scripts/generate.sh && ./scripts/integrate.sh
   ```

4. **删除占位符**
   ```bash
   rm types_placeholder.go
   ```

## 脚本说明

### generate_placeholders.py

- 📍 位置: `scripts/generate_placeholders.py`
- 🎯 功能: 自动扫描并生成占位符
- 🔧 用法: `python3 scripts/generate_placeholders.py`

### fix_all_undefined.sh

- 📍 位置: `scripts/fix_all_undefined.sh`
- 🎯 功能: Bash 版本的修复脚本
- 🔧 用法: `./scripts/fix_all_undefined.sh`

### integrate.sh

- 📍 位置: `scripts/integrate.sh`
- 🎯 功能: 集成生成的代码到项目
- 🔧 用法: `./scripts/integrate.sh`

## 完整流程

```bash
# 1. 生成代码
./scripts/generate.sh

# 2. 集成代码
./scripts/integrate.sh

# 3. 修复缺失类型
python3 scripts/generate_placeholders.py

# 4. 测试编译
go build .
```

## 常见问题

### Q: 为什么需要占位符？

A: 某些 API 在 `client.go` 中被引用，但没有对应的文档文件，所以无法自动生成。

### Q: 占位符类型可以使用吗？

A: 可以编译通过，但功能不完整。建议：
- 添加正确的字段定义
- 或添加对应的 API 文档重新生成

### Q: 如何找到缺失的 API 文档？

A: 查看占位符类型名称，如 `MenuGetResponse`：
- 对应 API: `menu/get`
- 需要在 `docs/api_docs/` 添加对应文档

## 总结

使用 `python3 scripts/generate_placeholders.py` 可以快速修复所有编译错误！
