# 跳过生成的 API 方法

## 概述

有些 API 在 `Client` 接口中被引用，但没有对应的文档或实现。本文档说明如何跳过这些方法的生成。

## 已跳过的方法

以下方法已在 `client.go` 中被注释掉（缺少文档）:

1. **ChatdataExportGetJobStatus** - 会话内容导出任务状态查询
2. **ChatdataGetagreestatusRoom** - 获取同意状态（房间）
3. **ChatdataGroupchatGet** - 获取群聊信息
4. **ChatdataKeywordDeleteRule** - 删除关键词规则
5. **ChatdataKeywordGetHitMsgList** - 获取关键词命中消息列表
6. **ChatdataSearchChat** - 搜索会话
7. **ChatdataSearchMsg** - 搜索消息
8. **ChatdataSyncMsg** - 同步消息

## 方法 1: 在生成器中跳过

修改 `cmd/gencode/main.go`，添加到跳过列表：

```go
// skipAPIs 跳过生成的 API 列表（api_name）
var skipAPIs = map[string]bool{
	"chatdata/export/get_job_status": true,
	"chatdata/groupchat/get": true,
	// 添加更多需要跳过的 API
}
```

## 方法 2: 自动注释掉缺失的方法

使用脚本自动注释掉所有缺失实现的方法：

```bash
python3 scripts/comment_missing_methods.py
```

脚本会：
1. 扫描编译错误中的 "missing method"
2. 在 `client.go` 的 `Client` 接口中注释掉这些方法
3. 自动添加 `// TODO: 缺少实现或文档` 注释
4. 循环直到编译成功

## 方法 3: 手动注释

在 `client.go` 中找到对应的方法签名，添加 `//` 注释：

```go
// 原来
ChatdataExportGetJobStatus(req *ChatdataExportGetJobStatusRequest) (*ChatdataExportGetJobStatusResponse, error)

// 修改后
// ChatdataExportGetJobStatus(req *ChatdataExportGetJobStatusRequest) (*ChatdataExportGetJobStatusResponse, error) // TODO: 缺少文档
```

## 恢复方法

如果后续添加了对应的 API 文档，可以：

1. **添加 API 文档** 到 `docs/api_docs/`
2. **重新生成 JSON**:
   ```bash
   python3 docs/apis/build_apis_json.py --pretty
   ```
3. **从跳过列表中移除**（如果在生成器中跳过）
4. **取消注释**（如果在接口中注释）
5. **重新生成代码**:
   ```bash
   ./scripts/generate.sh
   ./scripts/integrate.sh
   ```

## 脚本说明

### comment_missing_methods.py

- 📍 位置: `scripts/comment_missing_methods.py`
- 🎯 功能: 自动注释掉缺失的 Client 接口方法
- 🔧 用法: `python3 scripts/comment_missing_methods.py`
- ⚙️ 工作原理:
  1. 运行 `go build` 捕获编译错误
  2. 提取 "missing method" 的方法名
  3. 在 `client.go` 中查找并注释对应的方法签名
  4. 循环执行直到编译成功

## 完整流程

```bash
# 1. 生成代码（会自动跳过 skipAPIs 中的 API）
./scripts/generate.sh

# 2. 集成代码
./scripts/integrate.sh

# 3. 注释掉缺失的方法（如果编译失败）
python3 scripts/comment_missing_methods.py

# 4. 测试编译
go build .
```

## 注意事项

1. **不要删除占位符类型**: 即使方法被注释掉，`types_placeholder.go` 中的类型定义也应该保留，以便将来恢复使用

2. **版本控制**: 被注释掉的方法应该提交到版本控制，以便团队成员知道哪些方法需要文档

3. **TODO 标记**: 所有注释掉的方法都应该有 `// TODO` 标记，方便后续搜索和处理

## 检查已注释的方法

```bash
# 查看所有被注释的方法
grep "// TODO: 缺少实现或文档" client.go

# 统计数量
grep -c "// TODO: 缺少实现或文档" client.go
```

## 总结

- ✅ 使用 `skipAPIs` 在生成器中跳过特定 API
- ✅ 使用 `comment_missing_methods.py` 自动注释缺失的方法
- ✅ 手动添加 `// TODO` 标记便于追踪
- ✅ 编译成功，项目可以正常使用
