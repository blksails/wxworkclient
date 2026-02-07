# 企业接口的token

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/90593](https://developer.work.weixin.qq.com/document/path/90593)
- **文档 ID**: `90593`
- **API 名称**: `获取企业access_token`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/gettoken`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

获取企业的access_token，用于调用通讯录、应用、消息等接口服务于企业。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| corpid | string | 是 | 企业的corpid |
| permanent_code | string | 是 | 永久授权码 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
| access_token | string | 企业的access_token，最长为512字节 |
| expires_in | uint32 | access_token有效期（秒） |
