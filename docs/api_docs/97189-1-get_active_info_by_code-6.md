# 获取激活码详情

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97189](https://developer.work.weixin.qq.com/document/path/97189)
- **文档 ID**: `97189`
- **API 名称**: `get_active_info_by_code`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/license/get_active_info_by_code`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

查询某个账号激活码的状态以及激活绑定情况。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用服务商的接口调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| corpid | string | 是 | 要查询的企业的corpid |
| active_code | string | 是 | 激活码 |

### 请求示例

```json
{
	"corpid":"xxx",
	"active_code" : "XXXXXXXX"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| active_info | object | 账号码信息 |
| active_info.active_code | string | 账号激活码 |
| active_info.type | int32 | 账号类型：1:基础账号，2:互通账号 |
| active_info.status | int32 | 账号状态 |
| active_info.userid | string | 账号绑定激活的企业成员userid |
| active_info.create_time | int32 | 创建时间 |
| active_info.active_time | int32 | 首次激活绑定用户的时间 |
| active_info.expire_time | int32 | 过期时间 |
| active_info.merge_info | object | 合并信息 |
| active_info.share_info | object | 分配信息 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"active_info": {
		"active_code": "code1",
		"type": 1,
		"status": 1,
		"userid": "USERID",
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
}
```
