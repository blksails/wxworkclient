# external_userid查询pending_id

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98040](https://developer.work.weixin.qq.com/document/path/98040)
- **文档 ID**: `98040`
- **API 名称**: `external_userid_to_pending_id`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/corpgroup/batch/external_userid_to_pending_id?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 上下游企业共享的自建应用或代开发应用的access_token |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| chat_id | string | 否 | 群id，如果有传入该参数，则只检查群主是否在可见范围，同时会忽略在该群以外的external_userid。如果不传入该参数，则只检查客户跟进人是否在可见范园内。 |
| external_userid | string[] | 是 | 上游或下游企业外部联系人id，最多同时查询100个 |

### 请求示例

```json
{
  "chat_id":"xxxxxx",
  "external_userid":["oAAAAAAA", "oBBBBB"]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| result | object[] | 转换结果 |
| result[].external_userid | string | 转换的external_userid |
| result[].pending_id | string | 该微信账号还未成为企业客户时，返回的临时外部联系人ID |

### 响应示例

```json
{
    "errcode":0,
    "errmsg":"ok",
	"result":[
		 {
			"external_userid":"oAAAAAAA",
			"pending_id":"pAAAAA"
		 },
		 {
			"external_userid":"oBBBBB",
			"pending_id":"pBBBBB"
		 }
	 ]
}
```
