# 位置消息

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/90375](https://developer.work.weixin.qq.com/document/path/90375)
- **文档 ID**: `90375`
- **API 名称**: `location`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 5 个接口，共 6 个

## 接口描述

接收和发送位置消息的消息格式和参数说明。

## 请求信息

### 请求示例

```xml
<xml>
   <ToUserName><![CDATA[toUser]]></ToUserName>
   <FromUserName><![CDATA[fromUser]]></FromUserName>
   <CreateTime>1351776360</CreateTime>
   <MsgType><![CDATA[location]]></MsgType>
   <Location_X>23.134</Location_X>
   <Location_Y>113.358</Location_Y>
   <Scale>20</Scale>
   <Label><![CDATA[位置信息]]></Label>
   <MsgId>1234567890123456</MsgId>
   <AgentID>1</AgentID>
   <AppType><![CDATA[wxwork]]></AppType>
</xml>
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| ToUserName | string | 企业微信CorpID |
| FromUserName | string | 成员UserID |
| CreateTime | int32 | 消息创建时间（整型） |
| MsgType | string | 消息类型，固定为：location |
| Location_X | string | 地理位置纬度 |
| Location_Y | string | 地理位置经度 |
| Scale | int32 | 地图缩放大小 |
| Label | string | 地理位置信息 |
| MsgId | int64 | 消息id，64位整型 |
| AgentID | int32 | 企业应用的id，整型。可在应用的设置页面查看 |
| AppType | string | app类型，在企业微信固定返回wxwork，在微信不返回该字段 |
