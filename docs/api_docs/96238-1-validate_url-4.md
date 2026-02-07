# 支持Http Get请求验证URL有效性

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96238](https://developer.work.weixin.qq.com/document/path/96238)
- **文档 ID**: `96238`
- **API 名称**: `validate_url`
- **请求方法**: `GET`
- **接口地址**: `https://api.3dept.com/`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

验证回调服务的URL有效性

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| msg_signature | string | 是 | 企业微信加密签名 |
| timestamp | int | 是 | 时间戳 |
| nonce | string | 是 | 随机数 |
| echostr | string | 是 | 加密的字符串 |

### 请求示例

```text
GET https://api.3dept.com/?msg_signature=ASDFQWEXZCVAQFASDFASDFSS&timestamp=13500001234&nonce=123412323&echostr=ENCRYPT_STR
```
