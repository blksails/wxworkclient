# 提交余额支付订单任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99420](https://developer.work.weixin.qq.com/document/path/99420)
- **文档 ID**: `99420`
- **API 名称**: `submit_pay_job`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/license/submit_pay_job`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

使用该接口创建支付任务，该接口默认使用充值账户余额进行支付。提交成功后，该订单无法再变更支付方式。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用服务商的接口调用凭证，获取方法参见服务商的凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| payer_userid | string | 是 | 支付人，服务商企业内成员的明文userid，用于充值账户的流水记录。该userid必须登录过企业微信，并且企业微信已绑定微信，且必须为服务商企业内具有“购买接口许可”权限的管理员。 |
| order_id | string | 是 | 要使用充值账户余额支付的接口许可订单id |

### 请求示例

```json
{
	"payer_userid": "USERID",
	"order_id": "ORDERID"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| jobid | string | 支付任务的jobid |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"jobid": "JOBID"
}
```
