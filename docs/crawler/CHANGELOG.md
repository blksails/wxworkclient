# 更新日志

## v2.0.0 - 2024-12-10

### 🎉 重大改进：完善的 HTTP 信息提取

#### 新增功能

1. **完整的 HTTP 信息提取**
   - ✅ 自动提取 API URL（`api_url` 字段）
   - ✅ 识别 HTTP 方法（GET/POST/PUT/DELETE）
   - ✅ 区分 Query 参数和 Body 参数
   - ✅ 单独提取请求参数和响应参数

2. **代码示例提取**
   - ✅ 自动提取请求示例（`request_examples`）
   - ✅ 自动提取响应示例（`response_examples`）
   - ✅ 识别代码语言（JSON/XML/HTTP/Bash）
   - ✅ 保留原始格式和缩进

3. **改进的文档格式**
   - ✅ 清晰的章节结构
   - ✅ 基本信息独立展示
   - ✅ 请求信息和响应信息明确分开
   - ✅ 支持多个代码示例

4. **反爬虫检测**
   - ✅ 自动检测验证码页面
   - ✅ 检测到验证码后保存进度并停止
   - ✅ 提供恢复建议

5. **实时保存和断点续爬**
   - ✅ 每个接口提取后立即保存
   - ✅ 实时更新索引文件
   - ✅ 记录已访问的 URL
   - ✅ 支持中断后继续爬取

#### 数据结构变化

新增字段：
- `api_url`: API 接口地址
- `query_params`: Query 参数列表
- `body_params`: Body 参数列表
- `request_params`: 通用请求参数列表
- `response_params`: 响应参数列表
- `request_examples`: 请求示例列表
- `response_examples`: 响应示例列表

每个 CodeExample 包含：
- `title`: 示例标题
- `language`: 代码语言（json/xml/http/bash）
- `code`: 代码内容

#### Markdown 格式变化

**旧格式：**
```markdown
# API 标题

## 描述
...

## 请求方法
POST

## 参数
| 参数名 | 类型 | 必填 | 说明 |
```

**新格式：**
```markdown
# API 标题

## 基本信息
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/xxx`
- **请求方法**: `POST`

## 请求信息

### Query 参数
...

### Body 参数
...

### 请求示例
​```json
...
​```

## 响应信息

### 响应参数
...

### 响应示例
​```json
...
​```
```

#### 改进点

1. **信息更完整**
   - 之前：只有参数名称和说明
   - 现在：完整的 API URL、HTTP 方法、参数分类、代码示例

2. **结构更清晰**
   - 之前：请求和响应参数混在一起
   - 现在：明确分为"请求信息"和"响应信息"两大章节

3. **参数更细分**
   - 之前：所有参数混在一起
   - 现在：Query 参数、Body 参数、响应参数分别展示

4. **示例更完善**
   - 之前：可能没有代码示例
   - 现在：自动提取请求和响应的代码示例，带语法高亮

5. **数据可用性**
   - 之前：难以程序化处理
   - 现在：结构化的 JSON 数据，便于生成客户端代码

#### 使用示例

**查看生成的文档：**
```bash
cat api_docs/90195.md
```

**程序化处理：**
```python
import json

with open('api_docs/api_docs.json', 'r') as f:
    apis = json.load(f)

for api in apis:
    if api['method'] == 'POST':
        print(f"{api['title']}: {api['api_url']}")
        print(f"  Query 参数: {len(api['query_params'])}")
        print(f"  Body 参数: {len(api['body_params'])}")
```

#### 向后兼容

保留了以下字段以保持兼容性：
- `parameters`: 通用参数列表（当无法区分类型时使用）
- `request`: 原始请求文本
- `response`: 原始响应文本
- `sections`: 其他文档章节

#### 文档

- [DOCUMENT_FORMAT.md](DOCUMENT_FORMAT.md) - 详细的文档格式说明
- [ANTI_CAPTCHA.md](ANTI_CAPTCHA.md) - 反爬虫检测说明
- [FEATURES.md](FEATURES.md) - 实时保存和断点续爬功能说明
- [USAGE.md](USAGE.md) - 完整使用指南

---

## v1.0.0 - 2024-12-10

### 初始版本

- ✅ 基本爬虫功能
- ✅ 提取标题、描述
- ✅ 解析参数表格
- ✅ 生成 Markdown 文档
- ✅ 生成 JSON 数据

## v2.1.0 - 2024-12-10

### 🎯 改进：智能参数分类

#### 问题
之前的版本虽然能区分请求和响应参数，但在某些情况下分类不准确：
- 混合参数表格（请求和响应参数在同一个表格）分类错误
- `corpid`, `limit` 等明确的请求参数被误判为响应参数
- `next_cursor` 等响应参数被误判为请求参数

#### 解决方案

实现了更智能的参数分类算法，按优先级判断：

1. **结构判断** - 包含点号（如 `order_list.order_id`）→ 响应参数
2. **明确名称** - 使用预定义的参数名字典
   - 响应专属：`errcode`, `errmsg`, `next_cursor`, `has_more` 等
   - 请求专属：`provider_access_token`, `corpid`, `limit`, `cursor` 等
3. **特殊描述** - "由上次调用返回" → 响应参数
4. **必填标记** - 必填参数 → 请求参数（响应参数很少标记为必填）
5. **关键词匹配** - 描述中的 "返回"、"输出" → 响应；"传入"、"指定" → 请求
6. **位置规则** - 遇到明确的响应参数后，后续参数默认为响应参数

#### 改进效果

**改进前：**
```markdown
## 参数说明
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | | 是 | ... |
| corpid | | 否 | ... |
| errcode | | 否 | ... |
| errmsg | | 否 | ... |
```
所有参数混在一起，无法区分请求和响应。

**改进后：**
```markdown
## 请求信息

### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | | 是 | ... |
| corpid | | 否 | ... |

## 响应信息

### 响应参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | | ... |
| errmsg | | ... |
```
请求和响应参数明确分开！

#### 工具

新增 `regenerate.py` 工具，用于重新生成已爬取的文档：

```bash
# 重新生成单个文档
python3 regenerate.py 95647

# 重新生成多个文档
python3 regenerate.py 95647 90335 90332
```

#### 使用建议

如果发现已爬取的文档参数分类不准确：

1. 使用 `regenerate.py` 重新生成指定文档
2. 或删除 `.visited_urls.json` 并重新运行爬虫


## v2.1.1 - 2024-12-10

### 🔧 修复：HTTP 信息提取增强

#### 问题
某些 API 文档的请求方式和请求地址没有被正确提取，例如：
```
请求方式： POST（HTTPS）
请求地址： https://qyapi.weixin.qq.com/cgi-bin/license/list_order?provider_access_token=ACCESS_TOKEN
```

这种格式的信息在 `<strong>` 标签中，之前的提取逻辑只查找 `<code>` 和 `<pre>` 标签。

#### 解决方案

改进 `_extract_http_info` 方法，使用三层提取策略：

1. **从 strong 标签提取**（新增）
   - 查找 "请求方式：" 后的 HTTP 方法
   - 查找 "请求地址：" 后的 API URL
   - 这是企业微信文档的常用格式

2. **从 code/pre 标签提取**（原有）
   - 查找代码块中的 HTTP 信息
   - 适用于代码示例中的请求

3. **从整个页面文本提取**（增强）
   - 使用正则表达式匹配
   - 兜底方案，确保不遗漏

#### 提取示例

**网页源码：**
```html
<p>
  <strong>请求方式：</strong> POST（HTTPS）
</p>
<p>
  <strong>请求地址：</strong> 
  https://qyapi.weixin.qq.com/cgi-bin/license/list_order?provider_access_token=ACCESS_TOKEN
</p>
```

**提取结果：**
```markdown
## 基本信息

- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/license/list_order?provider_access_token=ACCESS_TOKEN`
```

#### 影响范围

- ✅ 现在能正确提取所有格式的 HTTP 信息
- ✅ 向后兼容，不影响已正确提取的文档
- ✅ 适用于企业微信文档的多种格式变体

#### 使用建议

如果之前的文档缺少请求方法或接口地址，使用 `regenerate.py` 重新生成：

```bash
python3 regenerate.py 95647
```


## v2.1.2 - 2024-12-10

### 🎨 改进：代码示例提取增强

#### 问题
请求包体（Request Body）和返回结果（Response）的 JSON 示例没有被提取，例如：

**请求包体：**
```json
{
    "corpid":"xxxxx",
    "start_time":1500000000,
    "end_time":1600000000,
    "cursor":"xxx",
    "limit":10
}
```

**返回结果：**
```json
{
    "errcode": 0,
    "errmsg": "ok",
    "next_cursor":"xxx",
    "has_more":1,
    "order_list":[...]
}
```

原因：这些示例前的标题使用 `<strong>` 标签而不是 `<h2>` 等标题标签。

#### 解决方案

1. **改进 `_find_parent_heading` 方法**
   - 现在同时查找 `h2/h3/h4/h5` 和 `strong` 标签
   - 企业微信文档常用 `strong` 作为小标题
   - 过滤掉非标题的 strong 标签（文本长度判断）

2. **增强 `_extract_code_examples` 方法**
   - 跳过空代码块或过短的代码块
   - 更精确的分类判断：
     - "请求包体" / "请求体" / "请求示例" → 请求示例
     - "返回结果" / "响应" / "返回" → 响应示例
   - 智能默认分类：
     - 包含 `errcode` 的 JSON → 响应示例
     - 其他 JSON → 请求示例

#### 提取结果

现在生成的文档包含完整的代码示例：

```markdown
## 请求信息

### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
...

### 请求示例

​```json
{
    "corpid":"xxxxx",
    "start_time":1500000000,
    "end_time":1600000000,
    "cursor":"xxx",
    "limit":10
}
​```

## 响应信息

### 响应参数
| 参数名 | 类型 | 说明 |
...

### 响应示例

​```json
{
    "errcode": 0,
    "errmsg": "ok",
    "next_cursor":"xxx",
    "has_more":1,
    "order_list":[...]
}
​```
```

#### 改进效果

- ✅ 正确提取请求包体的 JSON 示例
- ✅ 正确提取返回结果的 JSON 示例
- ✅ 自动识别 JSON/XML/HTTP/Bash 等代码语言
- ✅ 智能分类请求示例和响应示例
- ✅ 支持多个代码示例

#### 使用建议

重新生成文档以获取完整的代码示例：

```bash
# 重新生成单个文档
python3 regenerate.py 95647

# 重新生成所有文档（谨慎！）
python3 regenerate.py --all
```


## v2.2.0 - 2024-12-10

### 🎯 新功能：文档完整度评分

#### 功能说明

文档保存时自动评估完整度，并在文件名中添加评分后缀。

**必选项（共6项）：**
1. ✅ 请求方法 (GET/POST/PUT/DELETE)
2. ✅ 接口地址 (API URL)
3. ✅ 请求参数 (Query/Body 参数)
4. ✅ 请求示例 (JSON/XML 示例)
5. ✅ 响应参数 (返回字段说明)
6. ✅ 响应示例 (返回数据示例)

#### 文件命名规则

**格式：** `{id}-{score}.md`

**示例：**
- `95647-6.md` - 完整度 6/6（完美）🟢
- `90335-5.md` - 完整度 5/6（缺1项）🟡
- `90332-4.md` - 完整度 4/6（缺2项）🟡
- `91144-3.md` - 完整度 3/6（缺3项）🔴

#### 完整度标识

- 🟢 **6分** - 完整，包含所有必选信息
- 🟡 **4-5分** - 较完整，缺少1-2项信息
- 🔴 **0-3分** - 不完整，缺少3项以上信息

#### 保存输出

```
[1/1] 正在处理: 95647
    → 已保存: 95647-6.md (完整度: 6/6)
  ✓ 成功
    请求参数: 6, 响应参数: 7
```

#### 索引文件增强

**README.md 现在包含：**

1. **完整度统计**
   ```markdown
   ## 完整度统计
   
   - 🟢 完整（6分）: 45 个
   - 🟡 较完整（4-5分）: 78 个
   - 🔴 不完整（0-3分）: 41 个
   ```

2. **API 列表带评分**
   ```markdown
   ## API 列表
   
   - 🟢 `POST` [获取订单列表](95647-6.md) `[6/6]` - 服务商查询...
   - 🟡 `GET` [获取企业信息](90335-5.md) `[5/6]` - 获取企业基本信息
   - 🔴 [通知事件](90332-3.md) `[3/6]` - 推送事件说明
   ```

3. **按完整度排序**
   - 完整的文档排在前面
   - 方便优先查看和使用高质量文档

#### 评分计算逻辑

```python
def _calculate_completeness_score(doc):
    score = 0
    if doc.method: score += 1              # 请求方法
    if doc.api_url: score += 1             # 接口地址
    if doc.request_params: score += 1      # 请求参数
    if doc.request_examples: score += 1    # 请求示例
    if doc.response_params: score += 1     # 响应参数
    if doc.response_examples: score += 1   # 响应示例
    return score
```

#### 工具支持

**regenerate.py** 现在也支持评分：

```bash
# 重新生成带评分的文档
python3 regenerate.py 95647
# 输出：已保存: 95647-6.md (完整度: 6/6)
```

**cleanup_and_regenerate.py** - 批量迁移工具：

```bash
# 清理旧文档并重新生成（带评分）
python3 cleanup_and_regenerate.py
```

会自动：
1. 删除所有旧格式文档（无评分后缀）
2. 重新生成所有文档（带评分后缀）
3. 显示完整度统计

#### 使用建议

**查找完整文档：**
```bash
# 查找所有完整文档（6分）
ls ../api_docs/*-6.md

# 查找需要完善的文档（< 4分）
ls ../api_docs/*-[0-3].md
```

**优先使用完整文档：**
```python
import json
from pathlib import Path

# 读取索引
with open('../api_docs/README.md', 'r') as f:
    content = f.read()
    # 查找 🟢 标记的完整文档
    complete_docs = [line for line in content.split('\n') 
                     if '🟢' in line and '.md' in line]
```

#### 优势

1. **一目了然** - 从文件名就知道文档质量
2. **快速筛选** - 轻松找到完整或需要完善的文档
3. **质量追踪** - 随时了解文档库的整体质量
4. **优先级明确** - 优先使用高分文档

#### 示例对比

**改进前：**
```
95647.md
90335.md
90332.md
```
无法判断哪个文档更完整

**改进后：**
```
95647-6.md  🟢 完整
90335-5.md  🟡 较完整
90332-3.md  🔴 需完善
```
立即知道文档质量！


## v2.3.0 - 2024-12-10

### 🐛 重大修复：断点续传功能

#### 问题描述

之前的断点续传功能存在严重缺陷：
- 爬虫中断后重启，无法继续爬取
- 原因：使用深度优先搜索（DFS），从起始 URL 开始递归
- 起始 URL 已在 visited 集合中，直接被跳过
- 导致无法发现和爬取其他页面

#### 解决方案

**重新设计为 BFS（广度优先搜索）+ 队列机制：**

1. **维护待爬取队列**
   - 新增 `queue` 属性，存储待爬取的 URL 列表
   - 使用 BFS 而非 DFS，避免递归深度问题

2. **队列持久化**
   - 新增 `.crawl_queue.json` 文件
   - 保存待爬取的 URL 队列
   - 每10个页面自动保存，中断时也会保存

3. **智能重新扫描**
   - 当队列为空但有已访问页面时，自动进入重新扫描模式
   - 重新扫描已访问页面的链接，发现未爬取的 URL
   - 发现新链接后自动关闭重新扫描模式

4. **优化链接发现**
   - 已访问的页面不重新提取内容（避免重复）
   - 但会扫描页面链接（发现遗漏的 URL）
   - 重新扫描时使用更短的延迟（0.5秒 vs 2秒）

#### 技术细节

**新增文件：**
- `.crawl_queue.json` - 待爬取队列持久化文件

**新增方法：**
```python
def _load_queue(self):
    """加载待爬取的 URL 队列"""

def _save_queue(self):
    """保存待爬取的 URL 队列"""
```

**修改的核心逻辑：**

```python
# 原来（DFS）
def crawl(self):
    self._crawl_page(self.start_url)  # 递归爬取

def _crawl_page(self, url):
    if url in self.visited:
        return  # 已访问直接返回，无法继续
    # ...
    for link in links:
        self._crawl_page(link)  # 递归调用

# 现在（BFS + 队列）
def crawl(self):
    while self.queue:  # 从队列中取出URL
        url = self.queue.pop(0)
        self._crawl_page(url)

def _crawl_page(self, url):
    already_visited = url in self.visited
    
    if already_visited and not self.need_rescan:
        return  # 正常模式下跳过已访问页面
    
    if already_visited:
        print(f"重新扫描链接: {url}")  # 重新扫描模式
    
    # 扫描链接并加入队列（而非递归调用）
    for link in links:
        if link not in visited and link not in queue:
            self.queue.append(link)  # 加入队列
```

#### 测试结果

```bash
$ python3 test_crawl_resume.py

已加载 282 个已访问的 URL
已加载 0 个待爬取的 URL
队列为空但有 282 个已访问页面
将重新扫描部分页面来发现未爬取的链接...

重新扫描链接: https://developer.work.weixin.qq.com/document/path/91201
  ✓ 发现 542 个新链接

爬取后状态:
  已访问: 282 个 URL
  队列: 543 个待爬取
  已提取文档: 0 个

✓ 测试完成！
```

#### 使用示例

**场景1：首次运行**
```bash
$ python3 crawler.py
开始爬取企业微信 API 文档...
输出目录: ../api_docs

正在爬取: https://developer.work.weixin.qq.com/document/path/91201
  ✓ 提取文档: 获取 access_token
  → 已保存: 91201-6.md (完整度: 6/6)
...
```

**场景2：中断后重启（有队列）**
```bash
$ python3 crawler.py
开始爬取企业微信 API 文档...
输出目录: ../api_docs
断点续爬模式: 已访问 150 个页面，队列中还有 243 个待爬取

正在爬取: https://developer.work.weixin.qq.com/document/path/90332
  ✓ 提取文档: 成员管理
  → 已保存: 90332-5.md (完整度: 5/6)
...
```

**场景3：中断后重启（队列为空）**
```bash
$ python3 crawler.py
开始爬取企业微信 API 文档...
输出目录: ../api_docs
已加载 282 个已访问的 URL
已加载 0 个待爬取的 URL
队列为空但有 282 个已访问页面
将重新扫描部分页面来发现未爬取的链接...

重新扫描链接: https://developer.work.weixin.qq.com/document/path/91201
  ✓ 发现 542 个新链接

正在爬取: https://developer.work.weixin.qq.com/document/path/93010
  ✓ 提取文档: 通讯录回调通知
  → 已保存: 93010-4.md (完整度: 4/6)
...
```

#### 优势

1. **可靠性** ⭐
   - 真正的断点续传，中断后可以无缝继续
   - 不会丢失未爬取的 URL

2. **效率** ⚡
   - BFS 避免深度递归和栈溢出
   - 智能重新扫描，只在必要时才重新请求页面

3. **可观察性** 👀
   - 实时显示队列大小和进度
   - 清楚知道还有多少页面待爬取

4. **容错性** 🛡️
   - 定期自动保存队列（每10个页面）
   - 中断时也会保存队列
   - 验证码触发时保存队列

#### 文件说明

**新增的持久化文件：**
```
api_docs/
├── .visited_urls.json      # 已访问的 URL 列表
├── .crawl_queue.json       # 待爬取的 URL 队列（新增）
├── api_docs.json           # 所有 API 文档的 JSON
└── README.md               # 索引文件
```

**.crawl_queue.json 格式：**
```json
{
  "queue": [
    "https://developer.work.weixin.qq.com/document/path/90332",
    "https://developer.work.weixin.qq.com/document/path/90333",
    ...
  ],
  "timestamp": "2024-12-10 16:45:00",
  "queue_size": 243
}
```

#### 相关工具

**test_resume.py** - 测试断点续传状态：
```bash
python3 test_resume.py
# 显示：已访问 URL 数量、队列大小、队列内容预览
```

**test_crawl_resume.py** - 测试完整流程：
```bash
python3 test_crawl_resume.py
# 模拟中断后重启，验证队列是否正常工作
```

**create_queue.py** - 创建空队列文件（如果需要）：
```bash
python3 create_queue.py
# 在首次运行时创建队列文件
```

#### 注意事项

1. **首次运行后中断**
   - 如果首次运行就中断，队列可能为空
   - 重启时会自动重新扫描起始页面
   - 这是正常行为，会自动恢复

2. **队列文件丢失**
   - 如果 `.crawl_queue.json` 丢失，但 `.visited_urls.json` 存在
   - 爬虫会自动重新扫描来重建队列
   - 不会重新爬取已访问的页面

3. **性能优化**
   - 队列每10个页面自动保存一次
   - 如果频繁中断，可以减少保存间隔
   - 修改 `crawl()` 方法中的 `len(self.visited) % 10 == 0`

#### 升级指南

如果你已经在使用旧版本的爬虫：

1. **无需手动操作**
   - 旧的 `.visited_urls.json` 仍然有效
   - 爬虫会自动创建 `.crawl_queue.json`

2. **首次运行新版本**
   - 会自动重新扫描起始页面
   - 发现并爬取遗漏的 URL

3. **清理旧文件（可选）**
   ```bash
   # 如果想从头开始
   rm ../api_docs/.visited_urls.json
   rm ../api_docs/.crawl_queue.json
   ```

#### 总结

这次修复彻底解决了断点续传的问题：
- ✅ 中断后可以无缝继续爬取
- ✅ 不会丢失任何未爬取的页面
- ✅ 智能重新扫描机制
- ✅ 更可靠、更高效

从 DFS 到 BFS + 队列，这是一个架构级的改进！🎉

