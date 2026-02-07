# 支持Http Post请求接收业务数据

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/91116](https://developer.work.weixin.qq.com/document/path/91116)
- **文档 ID**: `91116`
- **API 名称**: `receive_business_data`
- **请求方法**: `POST`
- **接口地址**: `https://api.3dept.com/`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

接收业务数据，需要解密后得到明文消息内容。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| msg_signature | string | 是 | 企业微信加密签名 |
| timestamp | int | 是 | 时间戳 |
| nonce | string | 是 | 随机数 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| XML data | object | 是 | 包含加密的消息结构体 |

### 请求示例

```text
POST https://api.3dept.com/?msg_signature=ASDFQWEXZCVAQFASDFASDFSS&timestamp=13500001234&nonce=123412323

<xml>
   <ToUserName><![CDATA[toUser]]></ToUserName>
   <AgentID><![CDATA[toAgentID]]></AgentID>
   <Encrypt><![CDATA[msg_encrypt]]></Encrypt>
</xml>
```
