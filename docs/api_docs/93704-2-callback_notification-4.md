# 回调通知

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/93704](https://developer.work.weixin.qq.com/document/path/93704)
- **文档 ID**: `93704`
- **API 名称**: `callback_notification`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/calendar/callback_notification?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

企业微信会将相应的事件推送给日历所属应用配置的回调URL。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 访问令牌 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
