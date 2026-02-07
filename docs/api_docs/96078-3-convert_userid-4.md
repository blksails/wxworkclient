# ID转换接口

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96078](https://developer.work.weixin.qq.com/document/path/96078)
- **文档 ID**: `96078`
- **API 名称**: `convert_userid`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/user/convert_to_openid`
- **分组信息**: 第 3 个接口，共 14 个

## 接口描述

将userid转换为open_userid

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userid | string | 是 | 待转换的userid |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| open_userid | string | 转换后的open_userid |
