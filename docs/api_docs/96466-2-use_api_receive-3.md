# 使用接收消息

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96466](https://developer.work.weixin.qq.com/document/path/96466)
- **文档 ID**: `96466`
- **API 名称**: `use_api_receive`
- **请求方法**: `POST`
- **接口地址**: `https://api.3dept.com/`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

企业微信会将消息发送给企业填写的URL，企业后台需要做正确的响应。

## 请求信息

### 请求示例

```text
POST https://api.3dept.com/?msg_signature=ASDFQWEXZCVAQFASDFASDFSS&timestamp=13500001234&nonce=123412323

<xml>
   <ToUserName><![CDATA[toUser]]></ToUserName>
   <AgentID><![CDATA[toAgentID]]></AgentID>
   <Encrypt><![CDATA[msg_encrypt]]></Encrypt>
</xml>
```

## 其他说明

### 接收消息协议的说明

企业微信服务器在五秒内收不到响应会断掉连接，并且重新发起请求，总共重试三次。如果企业在调试中，发现成员无法收到被动回复的消息，可以检查是否消息处理超时。
