# 批量激活账号

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95553](https://developer.work.weixin.qq.com/document/path/95553)
- **文档 ID**: `95553`
- **API 名称**: `batch_active_account`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/license/batch_active_account?provider_access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

可在一次请求里为一个企业的多个成员激活许可账号，便于服务商批量化处理。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用服务商的接口调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| corpid | string | 是 | 激活码所属企业corpid |
| active_list | array | 是 | 需要激活的账号列表 |
| active_list[].active_code | string | 是 | 账号激活码 |
| active_list[].userid | string | 是 | 待绑定激活的企业成员userid |

### 请求示例

```json
{
	"corpid": "CORPID",
	"active_list":[
	{
		"active_code" : "XXXXXXXX",
		"userid": "USERID"
	},
	{
		"active_code" : "XXXXXXXX",
		"userid": "USERID"
	}]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| active_result | array | 激活结果列表 |
| active_result[].active_code | string | 账号激活码 |
| active_result[].userid | string | 本次激活的企业成员的加密userid |
| active_result[].errcode | int32 | 用户激活错误码，0为成功 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"active_result":[
	{
		"active_code" : "XXXXXXXX",
		"userid": "USERID",
		"errcode":0
	},
	{
		"active_code" : "XXXXXXXX",
		"userid": "USERID",
		"errcode":0
	}]
}
```
