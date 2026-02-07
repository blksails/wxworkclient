# 应用授权

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97172](https://developer.work.weixin.qq.com/document/path/97172)
- **文档 ID**: `97172`
- **API 名称**: `authorize_app`
- **请求方法**: `POST`
- **接口地址**: `https://127.0.0.1/suite/receive`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

企业微信服务器向应用的“指令回调URL”推送授权事件消息。

## 请求信息

### 请求示例

```json
{"event": "authorize", "SuiteId": "123456"}
```

## 响应信息

### 响应示例

```text
success
```
