# 编辑文档内容

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98027](https://developer.work.weixin.qq.com/document/path/98027)
- **文档 ID**: `98027`
- **API 名称**: `batch_update`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/wedoc/document/batch_update`
- **分组信息**: 第 1 个接口，共 13 个

## 接口描述

该接口可以对一个在线文档批量执行多个更新操作。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 访问令牌 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| docid | string | 是 | 文档的docid |
| version | uint32 | 否 | 操作的文档版本, 该参数可以通过获取文档内容接口获得。操作后文档版本将更新一版。要更新的文档版本与最新文档版本相差不能超过100个。 |
| requests | object[] | 是 | 更新操作列表 |

### 请求示例

```json
{
	"docid": "DOCID",
	"verison": 10,
	"requests": [
		{
			"insert_text": {
				"text": "text content",
				"location": {
					"index": 10
				}
			}
		},
		{
			"insert_table": {
				"rows": 2,
				"cols": 2,
				"location": {
					"index": 10
				}
			}
		}
	]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok"
}
```
