# 企业微信 API 文档爬虫使用指南

## 功能特性

### 1. 🤖 AI 驱动的文档提取（新功能）

**LLM 提取模式**（推荐）：使用 OpenAI GPT-4 Turbo 进行语义理解和结构化提取

**优势**：
- ✅ **更高准确性**：通过语义理解而非规则匹配
- ✅ **自动识别多 API**：一个页面包含多个接口时自动分离，无需手动切分
- ✅ **智能内容归属**：准确判断每段描述、参数属于哪个 API
- ✅ **处理不规范格式**：能理解文档语义，适应格式变化
- ✅ **自动提取 API 名称**：从 URL 中提取 API 名称（如 `add_field_group`）
- ✅ **自动 fallback**：LLM 失败时自动回退到传统解析方式

**配置方法**：
```bash
# 设置 OpenAI API Key
export OPENAI_API_KEY="your-api-key-here"

# 如果需要使用代理（可选）
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890

# 运行爬虫（自动使用 LLM 模式）
python3 crawler.py
```

**代理说明**：
- 爬虫会自动检测 `https_proxy`、`http_proxy` 环境变量
- 支持 HTTP 和 SOCKS5 代理
- 如果设置了代理，启动时会显示：`✓ LLM 提取模式已启用 (模型: gpt-4-turbo, 代理: http://127.0.0.1:7890)`

**传统 BeautifulSoup 模式**：
如果未配置 API Key，自动使用传统的规则匹配方式。

### 2. 多接口识别和分组

**LLM 模式**：
- 🎯 一次性理解整个页面，自动识别所有 API
- 🎯 智能判断内容归属，避免参数混杂
- 🎯 处理共享的说明和参数

**传统模式**：
- 检测"请求方式：POST（HTTPS）请求地址:"模式
- 自动将一个页面拆分为多个独立的 API 文档
- 文件命名格式：`{doc_id}-{index}-{api_name}-{score}.md`
  - `doc_id`: 文档 ID
  - `index`: 接口序号（1、2、3...）
  - `api_name`: API 名称（从 URL 提取，如 `get_sheet_priv`）
  - `score`: 完整度分数（0-6）

### 3. 指定文档 ID 爬取
支持只爬取指定的文档 ID，而不是爬取整个网站。

### 4. 智能参数提取
- 从请求地址中提取 Query 参数（如 `access_token`）
- 从请求包体 JSON 中推测参数类型
- 从响应示例 JSON 中推测返回值类型
- 自动合并表格和 JSON 中的参数信息
- **LLM 模式**：通过语义理解自动分类参数（query/body/response）

## 命令行用法

### 基本用法
```bash
# 爬取所有文档（从起始页面开始）
python3 crawler.py

# 禁用断点续爬（重新开始）
python3 crawler.py --no-resume

# 爬取指定的文档 ID
python3 crawler.py --doc-ids 99935

# 爬取多个指定的文档 ID（用逗号分隔）
python3 crawler.py --doc-ids 99935,90601,90350

# 指定输出目录
python3 crawler.py --doc-ids 99935 --output-dir ./my_docs

# 组合使用
python3 crawler.py --doc-ids 99935,90601 --output-dir ./my_docs --no-resume

# 只处理包含特定路由的页面（单个关键词）
python3 crawler.py --route-filter "第三方应用开发"

# 必须同时包含多个关键词（AND逻辑，空格分隔）
python3 crawler.py --route-filter "第三方应用开发" "服务端API"

# 排除特定路由的页面（支持多个，OR逻辑）
python3 crawler.py --route-exclude "服务商代开发" "已废弃"

# 组合使用：必须同时包含"第三方应用开发"和"服务端API"，但排除"服务商代开发"
python3 crawler.py --route-filter "第三方应用开发" "服务端API" --route-exclude "服务商代开发"
```

### 路由过滤器说明

`--route-filter` 和 `--route-exclude` 参数支持多个值（数组匹配），允许你精确控制要处理的页面。路由信息从页面的面包屑导航中提取。

**示例路由路径**：
```
第三方应用开发 > 服务端API > 推广二维码 > 调用接口 > 获取注册码
第三方应用开发 > 客户端API > 账号授权
企业内部开发 > 服务端API > 通讯录管理 > 成员管理
服务商代开发 > 服务端API > 应用管理
```

**匹配逻辑**：
- `--route-filter`: **AND 逻辑** - 路由必须同时包含数组中的**所有**关键词才处理
- `--route-exclude`: **OR 逻辑** - 只要路由包含数组中的**任意一个**关键词就排除

**使用场景**：
```bash
# 单个过滤器：只爬取"第三方应用开发"
python3 crawler.py --route-filter "第三方应用开发"

# AND逻辑：必须同时包含"第三方应用开发"和"服务端API"
python3 crawler.py --route-filter "第三方应用开发" "服务端API"

# 排除多个（OR逻辑）：排除"服务商代开发"或"已废弃"
python3 crawler.py --route-exclude "服务商代开发" "已废弃"

# 组合使用：必须同时包含("第三方应用开发"和"服务端API")，但不要"服务商代开发"
python3 crawler.py --route-filter "第三方应用开发" "服务端API" --route-exclude "服务商代开发"

# 结合其他参数
python3 crawler.py --route-filter "第三方应用开发" "服务端API" --route-exclude "服务商代开发" --no-resume
```

**工作原理**：
- 爬虫会从页面的 `<div class="ep-route-dir">` 元素中提取路由路径
- `--route-filter`: **AND 匹配** - 如果路由路径中不包含数组中的**所有**关键词，则跳过该页面
- `--route-exclude`: **OR 匹配** - 如果路由路径中包含数组中的**任意一个**关键词，则跳过该页面
- 两个过滤器可以同时使用，形成"包含(A且B且C) 但排除(X或Y或Z)"的逻辑
- 输出示例：
  ```
  启动信息：
  ✓ 路由包含过滤 (AND): 必须同时包含 ['第三方应用开发', '服务端API'] 中的所有关键词
  ✓ 路由排除过滤 (OR): 排除包含 ['服务商代开发'] 中任意一个的页面
  
  正在爬取: https://developer.work.weixin.qq.com/document/path/90341
    → 路由: 第三方应用开发 > 服务端API > 推广二维码
    ✓ 提取文档: 获取注册码
  
  正在爬取: https://developer.work.weixin.qq.com/document/path/90350
    → 路由: 第三方应用开发 > 客户端API > 账号授权
    ⊗ 跳过: 缺少必需的路由关键词 ['服务端API']
  
  正在爬取: https://developer.work.weixin.qq.com/document/path/90329
    → 路由: 服务商代开发 > 服务端API > 应用管理
    ⊗ 跳过: 缺少必需的路由关键词 ['第三方应用开发']
  
  正在爬取: https://developer.work.weixin.qq.com/document/path/90330
    → 路由: 企业内部开发 > 服务端API > 通讯录管理
    ⊗ 跳过: 缺少必需的路由关键词 ['第三方应用开发']
  ```

### 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--no-resume` | 禁用断点续爬模式，重新开始爬取 | `--no-resume` |
| `--doc-ids` | 指定要爬取的文档 ID，多个用逗号分隔 | `--doc-ids 99935,90601` |
| `--output-dir` | 指定输出目录，默认为 `../api_docs` | `--output-dir ./docs` |
| `--route-filter` | 路由包含过滤器（支持多个，AND逻辑），必须同时包含所有关键词 | `--route-filter "第三方应用开发" "服务端API"` |
| `--route-exclude` | 路由排除过滤器（支持多个，OR逻辑），包含任意一个就排除 | `--route-exclude "服务商代开发" "已废弃"` |
| `--split-multi-api` | 分割多接口页面（实验性，默认禁用，可能导致参数混杂） | `--split-multi-api` |

## 输出文件格式

### 单接口文档
```
90601-5.md
```
- `90601`: 文档 ID
- `5`: 完整度分数

### 多接口文档（同一页面包含多个接口）
```
99935-1-get_sheet_priv-6.md
99935-2-update_sheet_priv-6.md
99935-3-create_rule-5.md
99935-4-mod_rule_member-6.md
99935-5-delete_rule-6.md
```
- `99935`: 文档 ID
- `1`, `2`, `3`, `4`, `5`: 接口序号
- `get_sheet_priv` 等: API 名称
- `6`, `6`, `5`, `6`, `6`: 完整度分数

## 完整度评分规则

评分标准（0-6分）：
1. ✅ 请求方法（GET/POST/PUT/DELETE）
2. ✅ 接口地址（API URL）
3. ✅ 请求参数（Query/Body 参数）
4. ✅ 请求示例（JSON/XML 示例）
5. ✅ 响应参数（返回字段说明）
6. ✅ 响应示例（返回数据示例）

## Markdown 文档结构

```markdown
# {接口标题}

## 基本信息
- **文档地址**: {原始文档链接}
- **文档 ID**: {文档 ID}
- **API 名称**: {API 名称}
- **请求方法**: {GET/POST/PUT/DELETE}
- **接口地址**: {完整 API URL}
- **分组信息**: 第 X 个接口，共 Y 个（仅多接口页面）

## 接口描述
{接口描述文本}

## 请求信息

### Query 参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ... | ... | ... | ... |

### Body 参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ... | ... | ... | ... |

### 请求示例
```json
{...}
```

## 响应信息

### 响应参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| ... | ... | ... |

### 响应示例
```json
{...}
```

## 其他说明
{其他章节内容}
```

## 示例：爬取特定文档

假设你想重新爬取文档 ID 99935（这个文档包含多个接口）：

```bash
# 1. 爬取该文档
python3 crawler.py --doc-ids 99935

# 2. 查看输出
ls -la ../api_docs/99935-*.md

# 输出示例：
# 99935-1-get_sheet_priv-6.md
# 99935-2-update_sheet_priv-6.md
# 99935-3-create_rule-5.md
# 99935-4-mod_rule_member-6.md
# 99935-5-delete_rule-6.md
```

## 多接口页面处理

### 🤖 LLM 模式（推荐）

使用 LLM 提取时，会**自动智能处理多接口页面**：

```bash
# 配置 API Key 后运行
export OPENAI_API_KEY="your-api-key-here"
python3 crawler.py --doc-ids 99935
```

**工作原理**：
1. MarkItDown 将整个页面转换为 Markdown
2. GPT-3.5 一次性理解整个页面，自动识别所有 API
3. 智能判断每段描述、参数属于哪个 API
4. 生成独立的文档文件

输出示例：
```
99935-1-get_sheet_priv-6.md       # ✅ 只包含该接口的参数
99935-2-update_sheet_priv-6.md    # ✅ 只包含该接口的参数
99935-3-create_rule-6.md          # ✅ 只包含该接口的参数
```

**优势**：
- ✅ 参数归属准确，不会混杂
- ✅ 自动处理共享说明
- ✅ 不依赖固定的 HTML 结构
- ✅ 适应文档格式变化

### 传统模式

#### 默认行为（保持完整性）

**默认禁用自动分割**，保持文档完整性：
```bash
python3 crawler.py --doc-ids 99935
```

输出：
```
99935-6.md  # 完整文档，包含所有接口
```

**优点**：
- ✅ 保持原始页面完整性
- ✅ 参数表格完整可用
- ✅ 不会丢失信息

#### 实验性功能（不推荐）

启用自动分割（可能导致参数混杂）：
```bash
python3 crawler.py --doc-ids 99935 --split-multi-api
```

输出：
```
99935-1-get_sheet_priv-6.md       # ⚠️ 包含所有接口的参数
99935-2-update_sheet_priv-6.md    # ⚠️ 包含所有接口的参数
...
```

**缺点**：
- ❌ 参数会重复和混杂
- ❌ 每个接口都包含所有接口的参数

**建议**：使用 LLM 模式而非 `--split-multi-api` 标志。

详细说明请参考 [MULTI_API_ISSUE.md](./MULTI_API_ISSUE.md)

## 注意事项

1. **LLM 模式**：需要配置 `OPENAI_API_KEY` 环境变量，会产生 API 调用费用（每个页面约 0.01-0.02 美元）
2. **Token 使用**：爬虫会记录每次 LLM 调用的 token 使用量，方便成本控制
3. **自动 fallback**：LLM 失败时自动回退到传统解析方式，确保爬取不中断
4. **反爬虫限制**：爬取时会自动延迟（2秒），如果触发验证码会自动停止并保存进度
5. **断点续爬**：默认启用，会保存已访问的 URL 和待爬取队列
6. **多接口页面**：
   - **LLM 模式**：自动智能分离（推荐）
   - **传统模式**：默认不分割（使用 `--split-multi-api` 启用分割，但不推荐）
7. **参数推测**：从 JSON 示例中自动推测参数类型
8. **Query 参数**：从请求 URL 中自动提取 Query 参数

## 高级技巧

### 批量爬取多个文档
```bash
# 创建一个包含文档 ID 的列表
DOC_IDS="99935,93798,90195,90350,100776"
python3 crawler.py --doc-ids $DOC_IDS
```

### 查看爬取进度
爬虫会生成以下文件来保存进度：
- `.visited_urls.json`: 已访问的 URL 列表
- `.crawl_queue.json`: 待爬取的 URL 队列
- `api_docs.json`: 完整的 API 数据（JSON 格式）
- `README.md`: API 索引文件

### 重新爬取某个文档
```bash
# 使用 --no-resume 确保重新爬取
python3 crawler.py --doc-ids 99935 --no-resume
```
