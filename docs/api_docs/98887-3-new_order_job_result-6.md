# 获取多企业新购订单提交结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98887](https://developer.work.weixin.qq.com/document/path/98887)
- **文档 ID**: `98887`
- **API 名称**: `new_order_job_result`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/license/new_order_job_result?provider_access_token=ACCESS_TOKEN`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

提交多企业新购订单之后，用于获取该订单的创建结果。该结果仅在提交多企业新购订单后7天内可获取。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用服务商的接口调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| jobid | string | 是 | 多企业新购任务id |

### 请求示例

```json
{
	"jobid" : "BUYJOBID"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
| status | int32 | 订单创建结果，1：创建完成，2：创建中，稍后再试，3：创建失败 |
| order_id | string | 订单号 |
| fail_list | object[] | 下单失败的企业及原因 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"status": 1,
	"order_id": "xxxx",
	"fail_list": [{
		"corpid": "CORPID",
		"errcode": 700400,
		"errmsg": "xxx"
	}]
}
```
