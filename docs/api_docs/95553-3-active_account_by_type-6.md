# 指定账号类型激活

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95553](https://developer.work.weixin.qq.com/document/path/95553)
- **文档 ID**: `95553`
- **API 名称**: `active_account_by_type`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/license/active_account_by_type?provider_access_token=ACCESS_TOKEN`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

userid当前必须未激活指定类型的许可或者绑定的该类型账号已过期。从当前企业中选择一个该指定类型的激活截止时间最早的未激活的激活码进行激活。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用服务商的接口调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| type | int32 | 是 | 账号类型。1：基础账号 2：互通账号 |
| corpid | string | 是 | 激活码所属企业corpid |
| userid | string | 是 | 待绑定激活的企业成员userid |

### 请求示例

```json
{
	"type" : 1,
	"corpid": "CORPID",
	"userid": "USERID"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok"
}
```
