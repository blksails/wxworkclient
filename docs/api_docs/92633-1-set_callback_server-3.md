# 设置接收事件服务器

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/92633](https://developer.work.weixin.qq.com/document/path/92633)
- **文档 ID**: `92633`
- **API 名称**: `set_callback_server`
- **请求方法**: `POST`
- **接口地址**: `https://work.weixin.qq.com/api/doc#12974/%E5%AE%A1%E6%89%B9%E7%8A%B6%E6%80%81%E9%80%9A%E7%9F%A5%E4%BA%8B%E4%BB%B6`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

订阅后，当企业内第三方应用所添加的企业微信“审批应用”单据流程发生变化时，会将审批单最新的流程状态回调给开发者。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| 指令回调URL | string | 是 | 第三方应用后台接收企业微信推送请求的访问协议和地址，支持http或https协议（建议使用https） |
| Token | string | 是 | 用于生成签名 |
| EncodingAESKey | string | 是 | 消息体的加密，是AES密钥的Base64编码 |

## 其他说明

### 设置入口

目前，支持将第三方应用添加的模板所对应的申请单的审批状态变化通知回调给第三方应用。第三方应用开发者可在服务商后台配置回调地址，接受此类型回调通知。

### 配置说明

进入配置页面，要求填写指令回调URL、Token、EncodingAESKey三个参数。指令回调URL是第三方应用后台接收企业微信推送请求的访问协议和地址，支持http或https协议（建议使用https）。Token可由企业任意填写，用于生成签名。EncodingAESKey用于消息体的加密，是AES密钥的Base64编码。
