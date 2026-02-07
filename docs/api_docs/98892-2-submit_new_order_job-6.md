# 提交多企业新购订单

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98892](https://developer.work.weixin.qq.com/document/path/98892)
- **文档 ID**: `98892`
- **API 名称**: `submit_new_order_job`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/license/submit_new_order_job?provider_access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

创建多企业新购任务之后，需要调用该接口，以提交多企业新购订单任务。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用服务商的接口调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| jobid | string | 是 | 多企业新购任务id |
| buyer_userid | string | 是 | 下单人，服务商企业内成员的明文userid |

### 请求示例

```json
{
	"jobid" : "BUYJOBID",
	"buyer_userid":"xxxx"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok"
}
```
