# Agents.md - 企业微信 API Client 代码生成规范

## 核心原则

**禁止手动编写生成文件。** 不要使用 Write/Edit 工具直接修改以下文件：

- `types_generated.go`
- `client_generated.go`
- `impls_generated.go`

所有 API 接口代码必须通过 `gencode` 工具链生成。

## 代码生成流程

```
crawler.py → docs/api_docs/*_llm.json + *.md → go run ./cmd/gencode → Go 代码
```

### Step 1: 爬取 API 文档

使用 crawler.py 从企业微信开发者文档抓取接口定义：

```bash
cd docs/crawler
./venv/bin/python3 crawler.py \
  --doc-ids <文档ID> \
  --output-dir ../api_docs \
  --no-resume \
  --llm-model <模型名称>
```

常用参数：

| 参数 | 说明 |
|------|------|
| `--doc-ids` | 指定文档 ID，逗号分隔（如 `95724,90601`） |
| `--output-dir` | 输出目录，默认 `../api_docs` |
| `--no-resume` | 禁用断点续爬，强制重新抓取 |
| `--llm-model` | LLM 模型（默认 `gpt-3.5-turbo`，可用 OpenRouter 模型） |
| `--no-llm` | 禁用 LLM，仅用 BeautifulSoup 解析 |
| `--fallback` | LLM 失败时回退到 BeautifulSoup |

爬取后会在 `docs/api_docs/` 生成：
- `{ID}_llm.json` — LLM 提取的结构化 API 定义（gencode 的输入）
- `{ID}-{N}-{api_name}-{score}.md` — Markdown 文档

### Step 2: 生成 Go 代码

```bash
go run ./cmd/gencode -input docs/api_docs -output . -package wxwork
```

参数说明：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-input` | `docs/api_docs` | `*_llm.json` 文件所在目录 |
| `-output` | `generated` | 输出目录，用 `.` 直接生成到项目根目录 |
| `-package` | `wxwork` | Go 包名 |
| `-clean` | `true` | 生成前清理旧文件 |
| `-limit` | `0` | 限制生成数量，0 为全部 |

生成的文件：
- `types_generated.go` — Request/Response 类型定义
- `client_generated.go` — Client 接口和方法实现
- `impls_generated.go` — 泛型实现层

### Step 3: 验证编译

```bash
go build .
```

## 完整示例：添加新 API

以添加 `del_contact_way` 为例：

```bash
# 1. 爬取文档
cd docs/crawler
./venv/bin/python3 crawler.py --doc-ids 95724 --output-dir ../api_docs --no-resume --llm-model openai/gpt-4o

# 2. 生成代码（在项目根目录）
cd ../..
go run ./cmd/gencode -input docs/api_docs -output . -package wxwork

# 3. 验证
go build .
```

## 注意事项

- `gencode` 读取的是 `*_llm.json` 文件，不是 `apis.json`
- `build_apis_json.py` 生成的 `apis.json` 是独立的聚合文件，gencode 不依赖它
- 已在 `types.go` 中手动定义的类型会被 gencode 自动跳过，避免重复
- 如果 crawler 因区域限制无法调用 LLM，可手动编写 `*_llm.json` 文件后直接运行 gencode
