# Crawler 快速参考

## 命令速查

```bash
# 爬取所有文档
python3 crawler.py

# 爬取指定文档
python3 crawler.py --doc-ids 99935

# 爬取多个文档
python3 crawler.py --doc-ids 99935,90601,90350

# 指定输出目录
python3 crawler.py --output-dir ./my_docs

# 重新开始爬取（不使用缓存）
python3 crawler.py --no-resume

# 组合使用
python3 crawler.py --doc-ids 99935 --output-dir ./docs --no-resume
```

## 文件命名规则

### 单接口文档
```
{doc_id}-{score}.md
```
示例：`90601-5.md`

### 多接口文档（新功能）
```
{doc_id}-{index}-{api_name}-{score}.md
```
示例：
- `99935-1-get_sheet_priv-6.md`
- `99935-2-update_sheet_priv-6.md`
- `99935-3-create_rule-5.md`

## 新功能速览

### 1️⃣ 多接口识别（默认禁用）
- ⚠️ 默认不分割多接口页面（避免参数混杂）
- ✅ 可选启用 `--split-multi-api`（实验性）
- ✅ 从 URL 提取 API 名称
- 📖 详见：[MULTI_API_ISSUE.md](./MULTI_API_ISSUE.md)

### 2️⃣ 指定文档爬取
- ✅ `--doc-ids` 参数指定文档 ID
- ✅ 支持多个文档（逗号分隔）
- ✅ 不爬取其他链接

### 3️⃣ Query 参数提取
- ✅ 从请求地址提取 Query 参数
- ✅ 智能推测参数类型
- ✅ 示例：`?access_token=TOKEN` → `access_token: string`

### 4️⃣ JSON 类型推测
- ✅ 从请求包体推测参数类型
- ✅ 从响应示例推测返回值类型
- ✅ 支持嵌套对象和数组

### 5️⃣ 智能参数合并
- ✅ 表格 + JSON + Query 参数自动合并
- ✅ 表格信息优先级最高
- ✅ 避免参数重复

## 参数类型推测规则

### Query 参数
| 参数名模式 | 推测类型 |
|-----------|---------|
| `*token`, `*key`, `*secret` | `string` |
| `*id` | `string` |
| `limit`, `offset`, `page`, `size`, `count` | `int` |
| 纯数字值 | `int` |
| `true`, `false`, `0`, `1` | `bool` |
| 其他 | `string` |

### JSON 值类型
| JSON 值 | 推测类型 |
|---------|---------|
| `123` | `int` |
| `123.45` | `float` |
| `"text"` | `string` |
| `true`, `false` | `bool` |
| `[1, 2, 3]` | `array[int]` |
| `["a", "b"]` | `array[string]` |
| `[{...}]` | `array[object]` |
| `{...}` | `object` |
| `null` | `string` |

## 完整度评分

| 分数 | 说明 | 包含内容 |
|-----|------|---------|
| 6 | 🟢 完整 | 方法 + URL + 请求参数 + 请求示例 + 响应参数 + 响应示例 |
| 5 | 🟡 较完整 | 缺少 1 项 |
| 4 | 🟡 较完整 | 缺少 2 项 |
| 3 | 🔴 不完整 | 缺少 3 项 |
| 2 | 🔴 不完整 | 缺少 4 项 |
| 1 | 🔴 不完整 | 缺少 5 项 |
| 0 | 🔴 不完整 | 缺少全部 |

## Markdown 文档结构

```
# {接口标题}

## 基本信息
- 文档地址、ID、API 名称、请求方法、接口地址

## 接口描述
{描述文本}

## 请求信息
### Query 参数
### Body 参数
### 请求示例

## 响应信息
### 响应参数
### 响应示例

## 其他说明
{其他章节}
```

## 常见使用场景

### 场景 1：完整爬取所有文档
```bash
python3 crawler.py
```
**说明**：从起始页面开始，递归爬取所有文档链接

### 场景 2：爬取单个指定文档
```bash
python3 crawler.py --doc-ids 99935
```
**说明**：只爬取文档 ID 99935，如果包含多个接口会自动分组

### 场景 3：批量爬取多个指定文档
```bash
python3 crawler.py --doc-ids 99935,93798,90195
```
**说明**：爬取 3 个指定的文档

### 场景 4：重新爬取某个文档（强制刷新）
```bash
python3 crawler.py --doc-ids 99935 --no-resume
```
**说明**：忽略缓存，重新爬取并覆盖现有文档

### 场景 5：自定义输出目录
```bash
python3 crawler.py --doc-ids 99935 --output-dir ./custom_docs
```
**说明**：将文档保存到 `./custom_docs` 目录

## 输出文件

### 主要输出
- `{doc_id}-{score}.md` - 单接口文档
- `{doc_id}-{index}-{api_name}-{score}.md` - 多接口文档
- `README.md` - API 索引
- `api_docs.json` - 完整 JSON 数据

### 状态文件
- `.visited_urls.json` - 已访问的 URL
- `.crawl_queue.json` - 待爬取队列

## 参数信息来源优先级

```
表格信息 > Query 参数 > JSON 推测
    ↓           ↓            ↓
  描述        示例值      类型推测
  类型        类型推测
  必填状态
```

**合并规则**：
1. 优先使用表格中的完整信息
2. 表格中缺少类型时，使用 JSON 推测
3. Query 参数会自动合并到表格参数中
4. JSON 中独有的参数会被标注"(从示例中推测)"

## 故障排除

### 问题：触发验证码
**解决**：等待 30 分钟后重新运行，或增加延迟时间

### 问题：文档不完整
**解决**：检查原始页面格式，可能需要调整识别规则

### 问题：多接口识别失败
**解决**：确认页面是否包含"请求方式：POST（HTTPS）"模式

### 问题：参数类型推测不准确
**解决**：优先以表格信息为准，JSON 推测仅作为补充
