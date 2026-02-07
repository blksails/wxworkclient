# 取消会议事件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97451](https://developer.work.weixin.qq.com/document/path/97451)
- **文档 ID**: `97451`
- **API 名称**: `meeting_change`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/webhook/callback/meeting_change`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

当管理员取消API创建的会议后，触发该事件。

## 请求信息

### 请求示例

```xml
<xml>
   <ToUserName><![CDATA[toUser]]></ToUserName>
   <FromUserName><![CDATA[fromUser]]></FromUserName>
   <CreateTime>1348831860</CreateTime>
   <MsgType><![CDATA[event]]></MsgType>
   <Event><![CDATA[meeting_change]]></Event>
   <ChangeType><![CDATA[cancel_meeting]]></ChangeType>
   <MeetingId><![CDATA[wcjgewCwAAqeJcPI1d8Pwbjt7nttzAAA]]></MeetingId>
</xml>
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| ToUserName | string | 企业微信CorpID |
| FromUserName | string | 成员UserID |
| CreateTime | int32 | 消息创建时间，unix时间戳 |
| MsgType | string | 消息类型，固定为：`event` |
| Event | string | 事件类型，固定为：`meeting_change` |
| ChangeType | string | 事件类型，固定为：`cancel_meeting` |
| MeetingId | string | 会议ID |
