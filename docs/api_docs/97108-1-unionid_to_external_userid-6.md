# unionid转换为第三方external_userid

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97108](https://developer.work.weixin.qq.com/document/path/97108)
- **文档 ID**: `97108`
- **API 名称**: `unionid_to_external_userid`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/idconvert/unionid_to_external_userid`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

当微信用户进入服务商的小程序或公众号时，服务商可通过此接口，将微信客户的unionid转为第三方主体的external_userid，若该微信用户尚未成为企业的客户，则返回pending_id。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证，第三方应用access_token或代开发应用access_token |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| unionid | string | 是 | 微信客户的unionid |
| openid | string | 是 | 微信客户的openid |
| subject_type | uint32 | 否 | 小程序或公众号的主体类型：0表示主体名称是企业的 (默认)， 1表示主体名称是服务商的 |

### 请求示例

```json
{
  "unionid":"oAAAAAAA",
  "openid":"oBBBB",
  "subject_type":1
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| external_userid | string | 该授权企业的外部联系人ID |
| pending_id | string | 该微信账号尚未成为企业客户时，返回的临时外部联系人ID，该ID有效期为90天，当该用户在90天内成为企业客户时，可以通过external_userid查询pending_id关联 |

### 响应示例

```json
{
 "errcode":0,
 "errmsg":"ok",
 "external_userid":"ooAAAAAAAAAAA",
 "pending_id":"ooBBBBBB"
}
```
