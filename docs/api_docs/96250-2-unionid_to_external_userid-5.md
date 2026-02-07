# 凭据使用示例

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96250](https://developer.work.weixin.qq.com/document/path/96250)
- **文档 ID**: `96250`
- **API 名称**: `unionid_to_external_userid`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/idconvert/unionid_to_external_userid?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

以unionid转换为第三方external_userid为例，在请求中加入mass_call_ticket字段即可。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| unionid | string | 是 | 微信客户的unionid |
| openid | string | 是 | 微信客户的openid |
| subject_type | int32 | 否 | 小程序或公众号的主体类型： 0表示主体名称是企业的， 1表示主体名称是服务商的 |
| mass_call_ticket | string | 否 | 大批量调用凭据 |

### 请求示例

```json
{
  "unionid": "oAAAAAAA",
  "openid": "oBBBB",
  "subject_type": 1,
  "mass_call_ticket": "TICKET"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
