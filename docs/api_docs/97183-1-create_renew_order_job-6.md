# 创建续期任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97183](https://developer.work.weixin.qq.com/document/path/97183)
- **文档 ID**: `97183`
- **API 名称**: `create_renew_order_job`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/license/create_renew_order_job?provider_access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

在同一个订单里，首次创建任务无须指定jobid，后续指定同一个jobid，表示往同一个订单任务追加续期的成员。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用服务商的接口调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| corpid | string | 是 | 企业id |
| account_list | object[] | 是 | 续期的账号列表，每次最多1000个。同一个jobid最多关联1000000个基础账号跟1000000个互通账号 |
| account_list[].userid | string | 是 | 续期企业的成员userid |
| account_list[].type | int32 | 是 | 续期账号类型。1:基础账号，2:互通账号 |
| jobid | string | 否 | 任务id，若不传则默认创建一个新任务。若指定第一次调用后拿到jobid，可以通过该接口将jobid关联多个userid |

### 请求示例

```json
{
	"corpid" : "wwxxx",
	"account_list":[
		{
			"userid":"userid1",
			"type":1
		}
	],
	"jobid":"JOBID"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| jobid | string | 任务id，请求包中未指定jobid时，会生成一个新的jobid返回 |
| invalid_account_list | object[] | 不合法的续期账号列表 |
| invalid_account_list[].errcode | int32 | 账号不合法相关错误码 |
| invalid_account_list[].errmsg | string | 账号不合法相关错误描述 |
| invalid_account_list[].userid | string | 用户userid |
| invalid_account_list[].type | int32 | 续期账号类型。1:基础账号，2:互通账号 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"jobid": "xxxx",
	"invalid_account_list":[
		{
			"errcode": 1,
			"errmsg": "xxx",
			"userid":"userid1",
			"type":1
		}
	]
}
```
