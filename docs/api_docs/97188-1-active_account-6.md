# 激活账号

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97188](https://developer.work.weixin.qq.com/document/path/97188)
- **文档 ID**: `97188`
- **API 名称**: `active_account`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/license/active_account?provider_access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

下单购买账号并支付完成之后，先调用获取订单中的账号列表接口获取到账号激活码，然后可以调用该接口将激活码绑定到某个企业员工，以对其激活相应的平台服务能力。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用服务商的接口调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| active_code | string | 是 | 账号激活码 |
| corpid | string | 是 | 激活码所属企业corpid |
| userid | string | 是 | 待绑定激活的企业成员userid |

### 请求示例

```json
{
	"active_code" : "XXXXXXXX",
	"corpid": "CORPID",
	"userid": "USERID"
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
