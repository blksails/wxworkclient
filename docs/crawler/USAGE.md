# 企业微信 API 文档爬虫使用指南

## 功能特性

### 1. 多接口识别和分组
爬虫现在可以自动识别一个页面中的多个 API 接口，并为每个接口生成独立的 Markdown 文档。

**识别规则**：
- 检测"请求方式：POST（HTTPS）请求地址:"模式
- 自动将一个页面拆分为多个独立的 API 文档
- 文件命名格式：`{doc_id}-{index}-{api_name}-{score}.md`
  - `doc_id`: 文档 ID
  - `index`: 接口序号（1、2、3...）
  - `api_name`: API 名称（从 URL 提取，如 `get_sheet_priv`）
  - `score`: 完整度分数（0-6）

### 2. 指定文档 ID 爬取
支持只爬取指定的文档 ID，而不是爬取整个网站。

### 3. 智能参数提取
- 从请求地址中提取 Query 参数（如 `access_token`）
- 从请求包体 JSON 中推测参数类型
- 从响应示例 JSON 中推测返回值类型
- 自动合并表格和 JSON 中的参数信息

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
```

### 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--no-resume` | 禁用断点续爬模式，重新开始爬取 | `--no-resume` |
| `--doc-ids` | 指定要爬取的文档 ID，多个用逗号分隔 | `--doc-ids 99935,90601` |
| `--output-dir` | 指定输出目录，默认为 `../api_docs` | `--output-dir ./docs` |
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

### 问题说明

某些文档页面（如 99935）在一个页面中包含多个 API 接口，但参数表格是混杂在一起的。

### 默认行为（推荐）

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

### 实验性功能（不推荐）

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

详细说明请参考 [MULTI_API_ISSUE.md](./MULTI_API_ISSUE.md)

## 注意事项

1. **反爬虫限制**：爬取时会自动延迟（2秒），如果触发验证码会自动停止并保存进度
2. **断点续爬**：默认启用，会保存已访问的 URL 和待爬取队列
3. **多接口页面**：默认不分割，保持完整性（使用 `--split-multi-api` 启用分割，但不推荐）
4. **参数推测**：从 JSON 示例中自动推测参数类型
5. **Query 参数**：从请求 URL 中自动提取 Query 参数

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
