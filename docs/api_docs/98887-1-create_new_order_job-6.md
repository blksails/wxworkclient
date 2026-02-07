# 创建多企业新购任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98887](https://developer.work.weixin.qq.com/document/path/98887)
- **文档 ID**: `98887`
- **API 名称**: `create_new_order_job`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/license/create_new_order_job?provider_access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

在同一个订单里，首次创建任务无须指定jobid，后续指定同一个jobid，表示往同一个订单任务追加新购的企业。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用服务商的接口调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| buy_list[].corpid | string | 是 | 企业id |
| buy_list[].account_count.base_count | uint32 | 否 | 基础账号个数，最多1000000个 |
| buy_list[].account_count.external_contact_count | uint32 | 否 | 互通账号个数，最多1000000个 |
| buy_list[].account_duration.months | uint32 | 否 | 购买的月数 |
| buy_list[].account_duration.days | uint32 | 否 | 购买的天数 |
| buy_list[].auto_active_status | uint32 | 否 | 是否开启自动激活，0：关闭，1：开启 |
| jobid | string | 否 | 多企业新购任务id，不传默认创建一个新任务，有传必须为第一次调用后返回的jobid |

### 请求示例

```json
{
	"buy_list": [{
		"corpid" : "CORPID",
		"account_count": {
			"base_count": 100,
			"external_contact_count": 100
		},
		"account_duration": {
			"months": 2,
			"days": 20
		},
		"auto_active_status": 1
	}],
	"jobid": "JOBID"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
| jobid | string | 多企业新购任务id |
| invalid_list | object[] | 不合法的新购信息列表 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"jobid": "BUYJOBID",
	"invalid_list":[
		{
			"corpid":"CORPID",
			"errcode": 1,
			"errmsg": "xxx"
		}
	]
}
```
