# 提交续期订单

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97183](https://developer.work.weixin.qq.com/document/path/97183)
- **文档 ID**: `97183`
- **API 名称**: `submit_order_job`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/license/submit_order_job?provider_access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

创建续期任务之后，需要调用该接口，以提交订单任务。注意，提交之后，需要到服务商管理端发起支付，支付完成之后，订单才能生效。也可以通过接口使用余额支付订单。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用服务商的接口调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| jobid | string | 是 | 任务id |
| buyer_userid | string | 是 | 下单人，服务商企业内成员的明文userid。该userid必须登录过企业微信，并且企业微信已绑定微信，且必须为服务商企业内具有“购买接口许可”权限的管理员。 |
| account_duration | object | 是 | 账号购买时长 |
| account_duration.months | int32 | 否 | 购买的月数，每个月按照31天计算。最多购买60个月。(若企业为服务商测试企业，每次续期只能续期1个月) |
| account_duration.new_expire_time | int32 | 否 | 指定的新到期时间戳，不可为今天和过去的时间，不可为1860天后的时间。须填当天的24时0分0秒，否则系统自动处理为当天的24时0分0秒。(若企业为服务商测试企业，不支持指定新的到期时间来续期) |

### 请求示例

```json
{
	"jobid" : "wwxxx",
	"buyer_userid":"xxxx",
	"account_duration":
	{
		"months":2
		//"new_expire_time":1700000000
	}
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| order_id | string | 订单号 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"order_id": "xxxx"
}
```
