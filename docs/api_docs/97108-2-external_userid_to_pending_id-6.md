# external_userid查询pending_id

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97108](https://developer.work.weixin.qq.com/document/path/97108)
- **文档 ID**: `97108`
- **API 名称**: `external_userid_to_pending_id`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/idconvert/batch/external_userid_to_pending_id`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

该接口可用于当一个微信用户成为企业客户前已经使用过服务商服务的场景。本接口获取到的pending_id可以维持unionid和external_userid的关联关系。pending_id有效期为90天，超过有效期之后，将无法通过该接口将external_userid换取对应的pending_id。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 ，第三方应用access_token或代开发应用access_token |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| chat_id | string | 否 | 群id，如果有传入该参数，则只检查群主是否在可见范围，同时会忽略在该群以外的external_userid。如果不传入该参数，则只检查客户跟进人是否在可见范围内。 |
| external_userid | string[] | 是 | 该企业的外部联系人ID，最多可同时查询100个外部联系人 |

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
| result[].external_userid | string | 该企业的外部联系人ID |
| result[].pending_id | string | 该微信账号还未成为企业客户时，unionid_to_external_userid接口返回的临时外部联系人ID |

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
