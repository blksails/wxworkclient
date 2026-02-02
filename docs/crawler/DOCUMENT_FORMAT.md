# API 文档格式说明

## 新版文档格式

改进后的 API 文档格式更加清晰、结构化，明确区分了请求和响应信息。

## 文档结构

### 1. 基本信息

显示 API 的基本元信息：

```markdown
## 基本信息

- **文档地址**: [链接](URL)
- **文档 ID**: `91201`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/xxx`
```

### 2. 接口描述

简要说明 API 的功能和用途：

```markdown
## 接口描述

这个接口用于获取访问令牌，用于后续调用企业微信 API。
```

### 3. 请求信息

**完整的请求相关信息，包括：**

#### 3.1 请求格式

显示完整的 HTTP 请求示例：

```markdown
### 请求格式

​```http
POST https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=xxx&corpsecret=xxx
​```
```

#### 3.2 Query 参数

URL 查询参数：

```markdown
### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |
| corpid | string | 是 | 企业ID |
```

#### 3.3 Body 参数

请求体参数（POST/PUT 请求）：

```markdown
### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 用户名称 |
| mobile | string | 否 | 手机号码 |
```

#### 3.4 请求参数

通用请求参数（当无法区分 Query/Body 时）：

```markdown
### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userid | string | 是 | 用户ID |
```

#### 3.5 请求示例

实际的请求代码示例：

```markdown
### 请求示例

​```http
POST https://qyapi.weixin.qq.com/cgi-bin/user/create?access_token=xxx
Content-Type: application/json

{
   "userid": "zhangsan",
   "name": "张三",
   "mobile": "13800000000"
}
​```
```

支持多种语言：
- `http` - HTTP 请求
- `json` - JSON 数据
- `xml` - XML 数据
- `bash` - curl 命令

### 4. 响应信息

**完整的响应相关信息，包括：**

#### 4.1 响应参数

返回数据的字段说明：

```markdown
### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int | 返回码，0 表示成功 |
| errmsg | string | 错误信息 |
| access_token | string | 访问令牌 |
| expires_in | int | 过期时间（秒） |
```

#### 4.2 响应示例

实际的响应数据示例：

```markdown
### 响应示例

​```json
{
   "errcode": 0,
   "errmsg": "ok",
   "access_token": "accesstoken000001",
   "expires_in": 7200
}
​```
```

### 5. 参数说明

如果有需要特别说明的参数：

```markdown
## 参数说明

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ...
```

### 6. 其他说明

额外的文档章节：

```markdown
## 其他说明

### 权限要求

需要企业管理员权限。

### 调用频率

每分钟最多调用 100 次。
```

## 完整示例

````markdown
# 创建成员

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/90195](https://developer.work.weixin.qq.com/document/path/90195)
- **文档 ID**: `90195`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/user/create`

## 接口描述

创建企业成员。

## 请求信息

### 请求格式

```http
POST https://qyapi.weixin.qq.com/cgi-bin/user/create?access_token=ACCESS_TOKEN
Content-Type: application/json
```

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userid | string | 是 | 成员UserID |
| name | string | 是 | 成员名称 |
| mobile | string | 否 | 手机号码 |
| department | int[] | 是 | 成员所属部门 |
| position | string | 否 | 职务信息 |

### 请求示例

```json
{
   "userid": "zhangsan",
   "name": "张三",
   "mobile": "13800000000",
   "department": [1, 2],
   "position": "产品经理"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "created"
}
```

## 其他说明

### 权限说明

仅通讯录同步助手或第三方通讯录应用可调用。

### 注意事项

1. 手机号码必须为有效的中国大陆手机号
2. userid 不能与现有成员重复
````

## 对比：旧版 vs 新版

### 旧版格式（问题）

```markdown
# API 标题

## 描述

一些描述...

## 请求方法

**POST**

## 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| xxx | string | 是 | ... |
| yyy | int | 否 | ... |

## 其他章节
...
```

**问题：**
- ❌ 没有明确的 API URL
- ❌ 请求参数和响应参数混在一起
- ❌ 无法区分 Query 参数和 Body 参数
- ❌ 缺少代码示例
- ❌ 结构不清晰

### 新版格式（改进）

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
```json
...
```

## 响应信息

### 响应参数
...

### 响应示例
```json
...
```
```

**优势：**
- ✅ 清晰显示 API URL
- ✅ 请求和响应明确分开
- ✅ Query 和 Body 参数分开
- ✅ 包含完整的代码示例
- ✅ 结构清晰易读

## JSON 数据格式

生成的 `api_docs.json` 也包含完整的结构化数据：

```json
{
  "title": "创建成员",
  "url": "https://developer.work.weixin.qq.com/document/path/90195",
  "path": "90195",
  "method": "POST",
  "api_url": "https://qyapi.weixin.qq.com/cgi-bin/user/create",
  "description": "创建企业成员",
  "query_params": [
    {
      "name": "access_token",
      "type": "string",
      "required": true,
      "description": "调用接口凭证"
    }
  ],
  "body_params": [
    {
      "name": "userid",
      "type": "string",
      "required": true,
      "description": "成员UserID"
    }
  ],
  "response_params": [
    {
      "name": "errcode",
      "type": "int",
      "required": false,
      "description": "返回码"
    }
  ],
  "request_examples": [
    {
      "title": "请求示例",
      "language": "json",
      "code": "..."
    }
  ],
  "response_examples": [
    {
      "title": "响应示例",
      "language": "json",
      "code": "..."
    }
  ]
}
```

## 使用建议

### 1. 查看 API 文档

打开 Markdown 文件，直接查看格式化的文档：

```bash
cat api_docs/90195.md
# 或使用 Markdown 预览工具
```

### 2. 程序化处理

使用 JSON 数据进行程序化处理：

```python
import json

with open('api_docs/api_docs.json', 'r', encoding='utf-8') as f:
    apis = json.load(f)

for api in apis:
    print(f"API: {api['title']}")
    print(f"URL: {api['api_url']}")
    print(f"Method: {api['method']}")
    print(f"Query Params: {len(api['query_params'])}")
    print(f"Body Params: {len(api['body_params'])}")
    print()
```

### 3. 生成客户端代码

基于结构化的 JSON 数据，可以生成各种语言的客户端代码：

```python
# 伪代码
def generate_client_method(api):
    method_name = api['title'].lower().replace(' ', '_')
    params = api['query_params'] + api['body_params']
    
    code = f"def {method_name}(self"
    for param in params:
        code += f", {param['name']}"
    code += "):\n"
    code += f"    url = '{api['api_url']}'\n"
    code += "    ...\n"
    
    return code
```

## 总结

新版文档格式的核心改进：

1. **✅ 明确的接口地址** - 清楚知道要调用哪个 URL
2. **✅ 分离的请求/响应** - 不再混淆输入和输出
3. **✅ 细分的参数类型** - Query、Body、响应参数各司其职
4. **✅ 完整的代码示例** - 直接可用的请求和响应样例
5. **✅ 结构化的数据** - JSON 格式便于程序处理

这样的文档格式既适合人类阅读，也适合程序处理！🎯
