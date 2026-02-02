# 企业微信 Client 代码生成器

根据企业微信官方文档自动生成完整的 Go Client 代码。

## 项目结构

```
wxwork-client/
├── cmd/gencode/          # 代码生成器
│   ├── main.go          # 生成器主程序
│   └── README.md        # 生成器文档
├── docs/
│   ├── api_docs/        # 原始 API 文档（Markdown）
│   └── apis/
│       ├── apis.json    # 解析后的 API 规范
│       └── build_apis_json.py  # JSON 生成脚本
├── generated/           # 生成的代码输出目录
│   ├── types_generated.go      # 类型定义
│   └── client_generated.go     # Client 方法
├── scripts/
│   └── generate.sh      # 一键生成脚本
└── examples/
    └── generated_client/
        └── main.go      # 使用示例
```

## 快速开始

### 1. 生成 APIs JSON

```bash
# 从 Markdown 文档生成 APIs JSON
python3 docs/apis/build_apis_json.py --pretty
```

这会生成 `docs/apis/apis.json`，包含所有 API 的结构化数据。

### 2. 生成 Go Client 代码

```bash
# 使用一键脚本
./scripts/generate.sh

# 或者手动运行
go run cmd/gencode/main.go
```

### 3. 查看生成的代码

```bash
# 查看类型定义
cat generated/types_generated.go

# 查看 Client 方法
cat generated/client_generated.go
```

## 生成器特性

### 1. 智能类型推断

根据字段名和类型描述自动推断 Go 类型：

- `userid`, `openid` → `string`
- `count`, `limit` → `int`
- `timestamp`, `expire_time` → `int64`
- `xxx_list`, `xxx_ids` → `[]string`
- `is_xxx`, `has_xxx` → `bool`

### 2. 命名规范

自动转换为符合 Go 规范的命名：

- `user/create` → `UserCreate`
- `user_id` → `UserID`
- `jsapi_ticket` → `JSAPITicket`
- `kf_account` → `KFAccount`

### 3. 自动过滤

- 过滤纯中文字段名
- 过滤应用类型描述字段（如"自建应用"、"第三方应用"）
- 自动去除 `errcode` 和 `errmsg`（已在 `CommonResponse` 中）

### 4. 完整注释

保留原始 API 文档的描述信息：

```go
// UserCreateRequest - 创建成员
type UserCreateRequest struct {
    UserID     string `json:"userid"`     // 成员UserID
    Name       string `json:"name"`       // 成员名称
    Department []int  `json:"department"` // 成员所属部门id列表
}
```

## 使用示例

### 基本用法

```go
package main

import "github.com/blacksail/wxwork-client"

func main() {
    // 创建 Client
    client := wxwork.NewClient(
        wxwork.WithCorpID("your_corp_id"),
        wxwork.WithCorpSecret("your_corp_secret"),
    )

    // 调用生成的方法
    req := &wxwork.UserCreateRequest{
        UserID: "zhangsan",
        Name:   "张三",
    }
    
    resp, err := client.UserCreate(req)
    if err != nil {
        panic(err)
    }
    
    println("Created user:", resp)
}
```

### 高级配置

```bash
# 只生成前 50 个 API（用于快速测试）
go run cmd/gencode/main.go -limit 50

# 自定义输出目录和包名
go run cmd/gencode/main.go \
    -output ./internal/wxwork \
    -package wxwork

# 指定不同的输入文件
go run cmd/gencode/main.go \
    -input ./custom_apis.json
```

## 生成统计

根据 `apis.json`：

- **总 API 数**: 2504
- **有效 API 数**: ~1279（有 api_name 和 method）
- **生成类型数**: ~2558（每个 API 生成 Request 和 Response）
- **生成方法数**: ~1279

## 已知限制

1. **复杂类型**: 嵌套对象和数组类型需要手动调整
2. **特殊字段**: 某些字段类型推断可能不准确，需要人工检查
3. **文档质量**: 依赖原始文档的准确性

## 后续集成

生成的代码可以：

1. **直接使用**: 复制到项目中使用
2. **作为参考**: 了解 API 结构后手动实现
3. **增量更新**: 只生成新增的 API

## 维护

### 更新 API 文档

```bash
# 1. 更新 Markdown 文档
# 将新的 API 文档放到 docs/api_docs/

# 2. 重新生成 JSON
python3 docs/apis/build_apis_json.py --pretty

# 3. 重新生成代码
./scripts/generate.sh
```

### 自定义生成器

编辑 `cmd/gencode/main.go` 可以：

- 修改类型推断规则
- 调整命名转换逻辑
- 添加自定义模板
- 扩展过滤规则

## 相关文档

- [代码生成器详细说明](cmd/gencode/README.md)
- [APIs JSON 格式说明](docs/apis/README.md)
- [使用示例](examples/generated_client/main.go)

## 问题反馈

如果生成的代码有问题，可以：

1. 检查原始 `apis.json` 数据
2. 调整生成器参数
3. 手动修正生成的代码
4. 提交 Issue 或 PR
