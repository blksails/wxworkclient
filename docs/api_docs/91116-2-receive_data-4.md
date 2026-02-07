# 支持Http Post请求接收业务数据

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/91116](https://developer.work.weixin.qq.com/document/path/91116)
- **文档 ID**: `91116`
- **API 名称**: `receive_data`
- **请求方法**: `POST`
- **接口地址**: `https://api.3dept.com/`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

接收业务数据，用于企业微信加密签名校验和消息内容解密

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| msg_signature | string | 是 | 企业微信加密签名 |
| timestamp | int32 | 是 | 时间戳 |
| nonce | string | 是 | 随机数 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| XML Body | object | 是 | 接收的业务数据XML结构体 |

### 请求示例

```xml
<xml>
   <ToUserName><![CDATA[toUser]]></ToUserName>
   <AgentID><![CDATA[toAgentID]]></AgentID>
   <Encrypt><![CDATA[msg_encrypt]]></Encrypt>
</xml>
```
