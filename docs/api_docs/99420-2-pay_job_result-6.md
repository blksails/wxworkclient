# 获取订单支付结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99420](https://developer.work.weixin.qq.com/document/path/99420)
- **文档 ID**: `99420`
- **API 名称**: `pay_job_result`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/license/pay_job_result`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

使用该接口获取余额订单支付任务的执行结果。仅在提交了 “余额支付订单任务” 后的7天内可获取。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用服务商的接口调用凭证，获取方法参见服务商的凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| jobid | string | 是 | “提交余额支付订单任务” 返回的jobid |

### 请求示例

```json
{
	"jobid": "JOBID"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码，表示接口调用是否成功（而非支付是否成功）。 如：支付失败时，该错误码会返回0。 |
| errmsg | string | 错误码说明 |
| status | int32 | 支付任务结果。  1：支付成功  2：支付任务执行中，稍后再试 3：支付失败 |
| pay_job_result | object | 支付结果的信息，仅在支付失败时返回，详见PayJobResult |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"status": 3,
	"pay_job_result": {
		"errcode": 700001,
		"errmsg": "xxx",
		"fail_corp_list": [{
			"corpid": "wwxxx",
			"errcode": 700002,
			"errmsg": "xxx"
		}]
	}
}
```
