# 开启接收消息

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96466](https://developer.work.weixin.qq.com/document/path/96466)
- **文档 ID**: `96466`
- **API 名称**: `set_api_receive`
- **请求方法**: `POST`
- **接口地址**: `https://api.3dept.com/`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

企业可以在应用的管理后台开启接收消息模式，需要提供可用的接收消息服务器URL。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| URL | string | 是 | 企业后台接收企业微信推送请求的访问协议和地址，支持http或https协议 |
| Token | string | 是 | 用于生成签名的参数 |
| EncodingAESKey | string | 是 | 消息体的加密参数 |

### 请求示例

```text
GET https://api.3dept.com/?msg_signature=ASDFQWEXZCVAQFASDFASDFSS&timestamp=13500001234&nonce=123412323&echostr=ENCRYPT_STR
```

## 其他说明

### 验证URL有效性

企业在获取请求时需要做Urldecode处理，否则可能会验证不成功。企业后台接收到验证请求后，需要作出正确的响应才能通过URL验证。
