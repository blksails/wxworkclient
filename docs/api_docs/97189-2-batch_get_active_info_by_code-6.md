# 批量获取激活码详情

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97189](https://developer.work.weixin.qq.com/document/path/97189)
- **文档 ID**: `97189`
- **API 名称**: `batch_get_active_info_by_code`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/license/batch_get_active_info_by_code`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

批量查询账号激活码的状态以及激活绑定情况。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用服务商的接口调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| corpid | string | 是 | 要查询的企业的corpid |
| active_code_list | array | 是 | 激活码列表，最多不超过1000个 |

### 请求示例

```json
{
	"corpid":"xxx",
	"active_code_list" : ["XXXXXXXX","YYYYYYYY","ZZZZZZZZ"]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| active_info_list | object[] | 账号码信息列表 |
| invalid_active_code_list | array | 无效的激活码列表 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"active_info_list": [
		{
			"active_code": "XXXXXXXX",
			"type": 1,
			"status": 1,
			"userid": "USERID1",
			"create_time":1640966400,
			"active_time": 1640966400,
			"expire_time":1640966400,
			"merge_info":
			{
				"to_active_code":"code_new",
				"from_active_code":"code_old"
			},
			"share_info":
			{
				"to_corpid":"CORPID",
				"from_corpid":"CORPID"
			}
		},
		{
			"active_code": "YYYYYYYY",
			"type": 2,
			"status": 1,
			"userid": "USERID2",
			"create_time":1640966400,
			"active_time": 1640966400,
			"expire_time":1640966400,
			"merge_info":
			{
				"to_active_code":"code_new",
				"from_active_code":"code_old"
			},
			"share_info":
			{
				"to_corpid":"CORPID",
				"from_corpid":"CORPID"
			}
		}
	],
	"invalid_active_code_list":["ZZZZZZZZ"]
}
```
