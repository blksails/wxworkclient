# 企业微信 Client SDK

基于 Golang 的企业微信 API Client，支持自动代码生成。

## 🚀 快速开始

```bash
# 1. 生成代码
./scripts/generate.sh

# 2. 集成到项目
./scripts/integrate.sh

# 3. 使用
```

```go
import "github.com/blacksail/wxwork-client"

client := wxwork.New(wxwork.Config{
    SuiteId:     "your_suite_id",
    SuiteSecret: "your_suite_secret",
})

// 使用 608 个自动生成的 API
resp, err := client.UserCreate(&wxwork.UserCreateRequest{
    UserID: "test001",
    Name:   "测试用户",
})
```

## ✨ 特性

- ✅ **608 个 API** - 自动生成企业微信 API Client
- ✅ **类型安全** - 完整的 Request/Response 类型定义
- ✅ **智能推断** - 自动推断 Go 类型
- ✅ **一键集成** - 自动备份和修改代码
- ✅ **持续更新** - 基于官方文档自动生成

## 📚 文档

- **[QUICKSTART.md](QUICKSTART.md)** - ⭐ 快速入门（推荐从这里开始）
- **[CODEGEN.md](CODEGEN.md)** - 完整开发文档
- **[scripts/README.md](scripts/README.md)** - 脚本使用说明
- **[cmd/gencode/README.md](cmd/gencode/README.md)** - 生成器文档
- **[generated/COMPLETION_REPORT.md](generated/COMPLETION_REPORT.md)** - 完成报告

## 🔧 代码生成器

### 生成统计

- **API 数量**: 608 个（去重后）
- **类型定义**: ~1,200 个（Request + Response）
- **代码行数**: ~24,000 行

### 一键生成

```bash
# 生成 + 集成
./scripts/generate.sh && ./scripts/integrate.sh
```

详细说明见 [QUICKSTART.md](QUICKSTART.md)

## 🛠️ 项目结构

```
wxwork-client/
├── cmd/gencode/           # 代码生成器
├── docs/
│   ├── api_docs/         # API 文档（Markdown）
│   └── apis/
│       └── apis.json     # 解析后的 API 规范
├── generated/            # 生成的代码
│   ├── types_generated.go
│   ├── client_generated.go
│   └── impls_generated.go
├── scripts/              # 自动化脚本
│   ├── generate.sh       # 生成代码
│   └── integrate.sh      # 集成代码
├── examples/             # 使用示例
├── client.go             # Client 实现
├── impl.go               # 实现基础
└── types.go              # 类型定义
```

## 🔄 更新流程

当有新的 API 时：

```bash
# 1. 更新文档（将新 .md 文件放到 docs/api_docs/）

# 2. 重新生成
python3 docs/apis/build_apis_json.py --pretty

# 3. 重新生成和集成
./scripts/generate.sh && ./scripts/integrate.sh
```

## 📝 使用示例

```go
package main

import (
    "fmt"
    "log"
    
    "github.com/blacksail/wxwork-client"
)

func main() {
    client := wxwork.New(wxwork.Config{
        SuiteId:     "your_suite_id",
        SuiteSecret: "your_suite_secret",
    })
    
    // 获取用户信息
    user, err := client.UserGet(&wxwork.UserGetRequest{
        Userid: "zhangsan",
    })
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("用户: %+v\n", user)
    
    // 创建部门
    dept, err := client.DepartmentCreate(&wxwork.DepartmentCreateRequest{
        Name:     "研发部",
        ParentID: 1,
    })
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("部门 ID: %d\n", dept.ID)
    
    // 发送消息
    msg, err := client.MessageSend(&wxwork.MessageSendRequest{
        ToUser:  "zhangsan",
        MsgType: "text",
        AgentID: 1000001,
        Text: map[string]string{
            "content": "Hello from WxWork Client!",
        },
    })
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("消息已发送: %s\n", msg.MsgID)
}
```

更多示例见 [examples/](examples/) 目录。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 基于企业微信官方 API 文档
- 感谢所有贡献者

---

**Happy Coding! 🚀**

如有问题，请参阅 [QUICKSTART.md](QUICKSTART.md) 或提交 Issue。
