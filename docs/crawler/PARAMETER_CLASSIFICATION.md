# 参数分类说明

## 智能参数分类机制

爬虫使用多层次的智能分类算法，自动区分请求参数和响应参数。

## 分类优先级

### 1. 结构判断（最高优先级）

**规则：** 包含点号（`.`）的参数名 → 响应参数

**示例：**
- `order_list.order_id` ✓ 响应参数
- `user.name` ✓ 响应参数  
- `data.list` ✓ 响应参数

**原理：** 嵌套结构通常出现在响应数据中。

### 2. 明确名称判断

使用预定义的参数名字典进行精确匹配。

#### 响应专属参数

```python
response_only_names = {
    'errcode', 'errmsg', 'error_code', 'error_msg',
    'result', 'data', 'info', 'detail',
    'next_cursor', 'has_more', 'total', 'count',
    'expires_in', 'refresh_token', 'openid', 'unionid'
}
```

**示例：**
- `errcode` ✓ 响应参数（总是）
- `errmsg` ✓ 响应参数（总是）
- `next_cursor` ✓ 响应参数
- `has_more` ✓ 响应参数

#### 请求专属参数

```python
request_only_names = {
    'provider_access_token', 'suite_access_token',
    'corpid', 'userid', 'agentid', 'suite_id',
    'cursor', 'limit', 'offset', 'size',
    'start_time', 'end_time', 'begin_time',
    'filter', 'sort', 'order'
}
```

**示例：**
- `provider_access_token` ✓ 请求参数
- `corpid` ✓ 请求参数
- `limit` ✓ 请求参数
- `cursor` ✓ 请求参数

### 3. 特殊描述判断

**规则：** 描述中包含特定关键词

#### "由上次调用返回"

```
参数: next_cursor
描述: 分页游标，由上一次调用返回，再下次请求时填写以获取之后分页的记录
→ 响应参数（虽然用于下次请求，但它来自上次响应）
```

### 4. 必填标记判断

**规则：** 标记为"必填"的参数 → 请求参数

**原理：** 响应参数很少标记为必填，必填的通常是请求参数。

**示例：**
```
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | ...  ← 请求参数
| corpid | string | 是 | ...       ← 请求参数
| errcode | int | 否 | ...          ← 可能是响应参数
```

### 5. 关键词匹配

#### 响应关键词

- 中文：`返回`、`输出`、`结果`
- 英文：`return`、`output`

**示例：**
```
描述: 返回的订单列表
→ 响应参数
```

#### 请求关键词

- 中文：`传入`、`输入`、`填写`、`指定`、`查询`
- 英文：`input`、`specify`、`query`

**示例：**
```
描述: 需要查询的企业ID
→ 请求参数
```

### 6. 位置规则（最低优先级）

**规则：** 遇到明确的响应参数（如 `errcode`）后，后续参数默认为响应参数

**示例：**
```
| 参数名 | 说明 |
|--------|------|
| corpid | 企业ID            ← 请求参数
| limit | 返回记录数         ← 请求参数
| errcode | 错误码           ← 响应参数（明确）
| errmsg | 错误说明          ← 响应参数（位置规则）
| order_list | 订单列表      ← 响应参数（位置规则）
```

## 实际案例

### 案例 1：混合参数表格

**原始表格：**
```
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | | 是 | 应用服务商的接口调用凭证 |
| corpid | | 否 | 企业id |
| start_time | | 否 | 开始时间 |
| end_time | | 否 | 结束时间 |
| cursor | | 否 | 用于分页查询的游标 |
| limit | | 否 | 返回的最大记录数 |
| errcode | | 否 | 错误码 |
| errmsg | | 否 | 错误码说明 |
| order_list | | 否 | 订单列表 |
| order_list.order_id | | 否 | 订单id |
| next_cursor | | 否 | 分页游标，由上一次调用返回 |
| has_more | | 否 | 是否有更多 |
```

**分类结果：**

**请求参数：**
1. `provider_access_token` - 必填 + 在请求专属列表中
2. `corpid` - 在请求专属列表中
3. `start_time` - 在请求专属列表中
4. `end_time` - 在请求专属列表中
5. `cursor` - 在请求专属列表中
6. `limit` - 在请求专属列表中

**响应参数：**
1. `errcode` - 在响应专属列表中（明确）
2. `errmsg` - 在响应专属列表中（明确）
3. `order_list` - 位置规则（errcode 之后）
4. `order_list.order_id` - 包含点号
5. `next_cursor` - 在响应专属列表中 + "由上次调用返回"
6. `has_more` - 在响应专属列表中

### 案例 2：模糊参数

**问题：** `access_token` 既可能在请求中（作为凭证），也可能在响应中（返回的令牌）

**解决：**
1. 检查是否必填 → 必填则为请求参数
2. 检查描述关键词 → "调用接口凭证" → 请求参数
3. 检查描述关键词 → "返回的访问令牌" → 响应参数

### 案例 3：特殊情况

**`next_cursor` 的分类：**

```
描述: 分页游标，由上一次调用返回，再下次请求时填写以获取之后分页的记录
```

**分析：**
- "由上一次调用返回" → 说明它来自上次的**响应**
- "再下次请求时填写" → 说明它用于下次的**请求**

**结论：** 响应参数（因为它的来源是响应，虽然用途是下次请求）

## 重新生成文档

如果发现分类不准确，可以重新生成：

### 方法 1：使用 regenerate.py

```bash
# 重新生成单个文档
cd docs/crawler
python3 regenerate.py 95647

# 重新生成多个文档
python3 regenerate.py 95647 90335 90332
```

### 方法 2：清除缓存重新爬取

```bash
# 删除访问记录
rm ../api_docs/.visited_urls.json

# 重新运行爬虫
python3 crawler.py
```

## 优化建议

### 如果发现分类错误

1. **检查参数名** - 是否需要添加到专属列表？
2. **检查描述** - 描述是否清晰表明参数用途？
3. **提交反馈** - 报告分类错误的案例，帮助改进算法

### 改进分类算法

编辑 `crawler.py` 中的参数名列表：

```python
# 添加新的响应专属参数
response_only_names = {
    'errcode', 'errmsg', ...
    'your_new_param',  # 添加你的参数
}

# 添加新的请求专属参数  
request_only_names = {
    'corpid', 'userid', ...
    'your_new_param',  # 添加你的参数
}
```

## 验证分类结果

### 检查生成的文档

```bash
cat ../api_docs/95647.md
```

查看是否有：
- `## 请求信息` 章节
- `## 响应信息` 章节
- 参数是否正确分类

### 检查 JSON 数据

```python
import json

with open('../api_docs/api_docs.json', 'r') as f:
    apis = json.load(f)

for api in apis:
    print(f"API: {api['title']}")
    print(f"  请求参数: {len(api['request_params'])}")
    print(f"  响应参数: {len(api['response_params'])}")
```

## 总结

智能参数分类使用多层次判断，确保高准确率：

1. **结构判断** - 最明确（点号）
2. **名称判断** - 高可信度（预定义列表）
3. **描述判断** - 中可信度（关键词）
4. **标记判断** - 中可信度（必填）
5. **位置判断** - 低可信度（默认规则）

通过这个分层机制，即使是混合的参数表格也能准确分类！ 🎯
