# 通过调用该sdk接口，专区程序可将一些事件通知应用后台。

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100040](https://developer.work.weixin.qq.com/document/path/100040)
- **文档 ID**: `100040`
- **API 名称**: `spec_notify_app`
- **请求方法**: `SDK调用`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

通过调用该sdk接口，专区程序可将一些事件通知应用后台。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| notify_id | string | 否 | 可指定`notify_id`，见SDK生成notify_id。如果不指定，则由接口自动生成。不超过64字节。 |
| notify_scene | int32 | 否 | 通知场景值，可用于标识此次通知对应的事件类型。取值范围：0~255，满足条件则通过应用接收专区通知回调给开发者，否则忽略该字段。 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| notify_id | string | 10分钟内有效，同时会通过应用接收专区通知回调给开发者。如果请求包体指定了`notify_id`，则直接采用并返回，否则由接口自动生成。 |
