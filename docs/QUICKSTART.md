# 企业微信 API 代码生成器 - 快速入门

## 🚀 一键生成和集成

### 完整流程（推荐）

```bash
# 1. 生成代码（首次或更新时）
./scripts/generate.sh

# 2. 集成到项目（自动备份和修改）
./scripts/integrate.sh

# 完成！现在可以使用 608 个生成的 API 了
```

就这么简单！🎉

---

## 📝 详细步骤

### 步骤 1: 生成代码

```bash
./scripts/generate.sh
```

**输出:**
```
🚀 开始生成企业微信 API Client 代码...
📝 检查 APIs JSON...
🔨 生成 Go 代码...
✅ 代码生成完成！
📁 生成的文件：
   - generated/types_generated.go
   - generated/client_generated.go
   - generated/impls_generated.go
```

**生成内容:**
- 608 个 API 方法
- ~1,200 个类型定义（Request/Response）
- ~24,000 行代码

---

### 步骤 2: 集成代码

```bash
./scripts/integrate.sh
```

**输出:**
```
🔧 开始集成生成的代码...
📦 备份现有文件...
   备份目录: .backup_20260202_193139
📝 复制生成的文件...
   ✓ types_generated.go
   ✓ client_generated.go
   ✓ impls_generated.go
🔧 检查 impl.go...
   ✓ implsGenerated 字段已存在
   ✓ installAll 调用已存在
🎨 格式化代码...
🧪 语法检查...
   ✅ 语法检查通过
✅ 集成完成！
```

**脚本自动完成:**
1. ✅ 备份现有文件
2. ✅ 复制生成的代码到项目根目录
3. ✅ 修改 `impl.go` 添加必要字段
4. ✅ 添加初始化调用
5. ✅ 格式化和检查代码

---

## 💡 使用生成的 API

集成后，可以直接使用所有生成的 API：

```go
package main

import (
    "fmt"
    "log"
    
    "github.com/blacksail/wxwork-client"
)

func main() {
    // 创建 client
    client := wxwork.New(wxwork.Config{
        SuiteId:     "your_suite_id",
        SuiteSecret: "your_suite_secret",
    })
    
    // 示例 1: 获取用户信息
    userResp, err := client.UserGet(&wxwork.UserGetRequest{
        Userid: "zhangsan",
    })
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("用户: %+v\n", userResp)
    
    // 示例 2: 创建部门
    deptResp, err := client.DepartmentCreate(&wxwork.DepartmentCreateRequest{
        Name:     "研发部",
        ParentID: 1,
    })
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("部门 ID: %d\n", deptResp.ID)
    
    // 示例 3: 发送消息
    msgResp, err := client.MessageSend(&wxwork.MessageSendRequest{
        ToUser:  "zhangsan|lisi",
        MsgType: "text",
        AgentID: 1000001,
        Text: map[string]string{
            "content": "测试消息",
        },
    })
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("消息 ID: %s\n", msgResp.MsgID)
}
```

---

## 🔄 更新 API

当有新的 API 文档时：

```bash
# 1. 更新文档（将新的 .md 文件放到 docs/api_docs/）

# 2. 重新生成 JSON
python3 docs/apis/build_apis_json.py --pretty

# 3. 重新生成和集成
./scripts/generate.sh && ./scripts/integrate.sh
```

---

## 🛠️ 高级用法

### 只生成部分 API（测试）

```bash
go run cmd/gencode/main.go -limit 10 -output test_gen
```

### 自定义输出目录

```bash
go run cmd/gencode/main.go -output ./custom_dir -package mypackage
```

### 查看生成统计

```bash
# Request 类型数量
grep -c "^type.*Request struct" types_generated.go

# Response 类型数量  
grep -c "^type.*Response struct" types_generated.go

# Client 方法数量
grep -c "^func (c \*client)" client_generated.go
```

---

## 🔍 故障排除

### 问题 1: "权限不足"

```bash
chmod +x scripts/*.sh
```

### 问题 2: 想回滚更改

```bash
# 查看备份
ls -la .backup_*

# 恢复
cp .backup_YYYYMMDD_HHMMSS/* ./
```

### 问题 3: 手动集成

如果不想用自动脚本，参考 [CODEGEN.md](CODEGEN.md) 的手动集成步骤。

---

## 📚 完整文档

- **[CODEGEN.md](CODEGEN.md)** - 完整开发文档
- **[scripts/README.md](scripts/README.md)** - 脚本详细说明
- **[cmd/gencode/README.md](cmd/gencode/README.md)** - 生成器文档
- **[generated/COMPLETION_REPORT.md](generated/COMPLETION_REPORT.md)** - 完成报告

---

## 🎯 核心特性

- ✅ **608 个 API** - 覆盖企业微信主要功能
- ✅ **自动类型推断** - 智能推断 Go 类型
- ✅ **智能命名** - 自动转换为 Go 风格命名
- ✅ **自动过滤** - 过滤无效字段和重复 API
- ✅ **完整注释** - 保留原始文档描述
- ✅ **一键集成** - 自动备份和修改代码
- ✅ **可定制** - 支持自定义生成规则

---

## 🙏 反馈

有问题或建议？
1. 查看 [故障排除](#-故障排除)
2. 阅读 [完整文档](CODEGEN.md)
3. 提交 Issue 或 PR

---

**Happy Coding! 🚀**
