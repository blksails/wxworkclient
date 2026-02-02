# 企业微信 API 文档爬虫

这个工具用于爬取企业微信开发者文档中的 API 接口文档，并生成 Markdown 格式的文档。

## 🆕 最新功能 (v2.3.0)

### 📊 文档完整度评分系统 (v2.2.0)
- ⭐ **自动评估文档质量**（0-6分）：请求方法、接口地址、请求参数、请求示例、响应参数、响应示例
- 📁 **文件名包含评分**：`95647-6.md`（完整度 6/6）🟢
- 📈 **索引显示统计**：完整/较完整/需完善一目了然
- 🎯 **快速筛选**：`ls api_docs/*-6.md` 查找完整文档

### 🔄 断点续传功能修复 (v2.3.0)
- ✅ **真正的断点续传**：中断后无缝继续爬取
- 🔍 **智能重新扫描**：自动发现遗漏的链接（测试：发现542个新链接）
- 💾 **队列持久化**：保存待爬取的 URL 列表 (`.crawl_queue.json`)
- ⚡ **BFS + 队列机制**：替代DFS，更可靠高效

## 目录结构

```
docs/
├── crawler/          # 爬虫源代码
│   ├── crawler.py   # 爬虫主程序
│   ├── requirements.txt # Python 依赖
│   ├── .envrc       # direnv 自动激活配置
│   ├── activate.sh  # 手动激活脚本
│   ├── run.sh       # 快速启动脚本
│   ├── example.py   # 使用示例
│   ├── test_crawler.py # 功能测试
│   ├── env.example  # 环境变量示例
│   └── venv/        # Python 虚拟环境（自动生成）
├── api_docs/        # 生成的 API 文档（将在运行后生成）
│   ├── README.md    # API 索引
│   ├── *.md         # 各个 API 的详细文档
│   └── api_docs.json # JSON 格式的完整数据
└── README.md        # 本文件
```

## 使用方法

### 方式零：自动激活虚拟环境（最便捷）

#### 选项 A：使用 direnv（推荐）

安装 direnv 后自动激活虚拟环境：

```bash
# macOS
brew install direnv

# 配置 shell（添加到 ~/.zshrc 或 ~/.bashrc）
eval "$(direnv hook zsh)"  # 或 eval "$(direnv hook bash)"

# 进入目录并允许 direnv
cd crawler
direnv allow
```

之后每次进入 `crawler` 目录，虚拟环境会自动激活！

#### 选项 B：使用 activate.sh 脚本

```bash
cd crawler
source activate.sh
```

这会激活虚拟环境并显示可用命令。

### 方式一：使用快速启动脚本

```bash
cd crawler
./run.sh
```

脚本会自动：
- 创建 Python 虚拟环境
- 安装所需依赖
- 运行爬虫程序

### 方式二：手动安装和运行

#### 1. 安装依赖

```bash
cd crawler
pip install -r requirements.txt
```

或使用虚拟环境（推荐）：

```bash
cd crawler
python3 -m venv venv
source venv/bin/activate  # Windows 上使用: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. 运行爬虫

```bash
cd crawler
python3 crawler.py
```

### 方式三：使用示例脚本

查看 `example.py` 了解更多自定义配置：

```bash
cd crawler
python3 example.py
```

爬虫将会：
- 从 https://developer.work.weixin.qq.com/document/path/91201 开始爬取
- 自动跟随相关的 API 文档链接
- 提取 API 的标题、描述、请求方法、参数等信息
- **每提取一个接口立即保存 Markdown 文件**
- **实时更新索引文件，可随时查看进度**
- 生成 JSON 格式的完整数据
- 支持断点续爬（中断后重新运行会跳过已爬取的页面）

### 断点续爬

默认启用断点续爬。如果爬取过程中中断，只需重新运行命令即可继续：

```bash
# 继续上次的爬取（默认）
python3 crawler.py

# 从头开始爬取（忽略之前的进度）
python3 crawler.py --no-resume
```

### 3. 查看结果

生成的文档会实时保存在 `api_docs/` 目录下：
- `README.md` - API 接口索引（实时更新）
- `<api_path>.md` - 各个 API 的详细文档（立即保存，包含完整的请求/响应信息）
- `api_docs.json` - JSON 格式的完整数据（最后生成，结构化的 API 信息）
- `.visited_urls.json` - 已访问的 URL 记录（用于断点续爬）

你可以在爬取过程中随时打开 `api_docs/README.md` 查看已爬取的接口列表！

### 文档格式示例

生成的 Markdown 文档格式清晰：

```markdown
# API 标题

## 基本信息
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/xxx`
- **请求方法**: `POST`

## 请求信息

### Query 参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userid | string | 是 | 用户ID |

### 请求示例
​```json
{"userid": "zhangsan"}
​```

## 响应信息

### 响应参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int | 返回码 |

### 响应示例
​```json
{"errcode": 0, "errmsg": "ok"}
​```
```

查看完整的文档格式说明：[crawler/DOCUMENT_FORMAT.md](crawler/DOCUMENT_FORMAT.md)

## 功能特性

- ✅ 自动爬取企业微信 API 文档
- ✅ **完整提取 HTTP 信息** - API URL、请求方法、Query/Body 参数
- ✅ **区分请求/响应** - 请求参数和响应参数明确分开
- ✅ **代码示例提取** - 自动提取请求和响应的代码示例
- ✅ 解析参数表格（支持多种表格格式）
- ✅ 提取各个章节内容
- ✅ **实时保存** - 每提取一个接口立即保存，避免数据丢失
- ✅ **断点续爬** - 支持中断后继续爬取，不会重复已爬取的内容
- ✅ **实时索引** - 爬取过程中实时更新索引文件
- ✅ **反爬虫检测** - 自动检测验证码页面，保存进度并停止
- ✅ **结构化文档** - 清晰的 Markdown 格式和 JSON 数据
- ✅ 防止重复爬取
- ✅ 请求间隔延迟（避免给服务器造成压力）

## 配置选项

你可以在 `crawler.py` 的 `main()` 函数中修改以下配置：

```python
BASE_URL = "https://developer.work.weixin.qq.com"
START_PATH = "/document/path/91201"  # 起始页面
OUTPUT_DIR = "../api_docs"            # 输出目录
```

## 数据结构

每个 API 文档包含以下信息：

```json
{
  "title": "API 标题",
  "url": "文档 URL",
  "path": "路径 ID",
  "description": "API 描述",
  "method": "请求方法（GET/POST）",
  "api_url": "API 接口地址",
  "request": "完整请求示例",
  "response": "响应示例",
  "query_params": [
    {
      "name": "参数名",
      "type": "参数类型",
      "required": true,
      "description": "Query 参数说明"
    }
  ],
  "body_params": [
    {
      "name": "参数名",
      "type": "参数类型",
      "required": true,
      "description": "Body 参数说明"
    }
  ],
  "request_params": [
    {
      "name": "参数名",
      "type": "参数类型",
      "required": true,
      "description": "请求参数说明"
    }
  ],
  "response_params": [
    {
      "name": "参数名",
      "type": "参数类型",
      "required": false,
      "description": "响应参数说明"
    }
  ],
  "request_examples": [
    {
      "title": "示例标题",
      "language": "json",
      "code": "请求代码示例"
    }
  ],
  "response_examples": [
    {
      "title": "示例标题",
      "language": "json",
      "code": "响应代码示例"
    }
  ],
  "sections": [
    {
      "title": "章节标题",
      "content": "章节内容"
    }
  ]
}
```

详细的文档格式说明请查看 [DOCUMENT_FORMAT.md](crawler/DOCUMENT_FORMAT.md)

## 注意事项

1. 爬虫会在每次请求之间等待 2 秒，以避免对服务器造成过大压力
2. 请遵守企业微信开发者文档的使用条款
3. 爬取的文档仅供学习和开发参考使用

## 反爬虫检测

爬虫会自动检测验证码页面（标题为"企业微信-验证码"）：

- ⚠️ **检测到验证码** - 自动保存当前进度并停止
- 💾 **进度已保存** - 所有已爬取的文档都已安全保存
- ⏰ **等待后重试** - 建议等待 30 分钟以上再重新运行

如果遇到验证码：

```bash
# 等待一段时间后重新运行（会自动跳过已爬取的）
python3 crawler.py

# 或增加请求延迟（编辑 crawler.py，修改 time.sleep(2) 为更大的值）
```

## 实时保存机制

爬虫采用实时保存策略：

1. **立即保存文件** - 每提取一个 API 文档，立即保存为 Markdown 文件
2. **实时更新索引** - 每爬取一个接口，立即更新 README.md 索引
3. **保存访问记录** - 记录所有已访问的 URL，支持断点续爬
4. **最后生成汇总** - 爬取完成后生成完整的 JSON 数据

优势：
- ✅ 不怕中断，已爬取的内容都已保存
- ✅ 可以随时查看进度
- ✅ 重启后自动跳过已爬取的内容
- ✅ 失败重试不会重复劳动

## 后续改进

- [x] 支持断点续爬
- [x] 实时保存文件
- [ ] 支持多线程爬取
- [ ] 支持更详细的参数解析
- [ ] 支持代码示例提取
- [ ] 支持错误码文档提取
- [ ] 支持自定义爬取范围
