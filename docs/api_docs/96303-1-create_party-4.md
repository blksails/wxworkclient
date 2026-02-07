# 新增部门事件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96303](https://developer.work.weixin.qq.com/document/path/96303)
- **文档 ID**: `96303`
- **API 名称**: `create_party`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/webhook/change_contact`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

该事件会回调给通讯录同步助手，代开发自建应用以及上游企业共享的应用。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ToUserName | string | 是 | 企业微信CorpID |
| FromUserName | string | 是 | 此事件该值固定为sys，表示该消息由系统生成 |
| CreateTime | int32 | 是 | 消息创建时间 （整型） |
| MsgType | string | 是 | 消息的类型，此时固定为event |
| Event | string | 是 | 事件的类型，此时固定为change_contact |
| ChangeType | string | 是 | 此时固定为create_party |
| Id | string | 是 | 部门Id |
| Name | string | 否 | 部门名称;代开发自建应用需要管理员授权才返回 |
| ParentId | string | 是 | 父部门id |
| Order | int32 | 否 | 部门排序 |

### 请求示例

```xml
<xml>
	<ToUserName><![CDATA[toUser]]></ToUserName>
	<FromUserName><![CDATA[sys]]></FromUserName>
	<CreateTime>1403610513</CreateTime>
	<MsgType><![CDATA[event]]></MsgType>
	<Event><![CDATA[change_contact]]></Event>
	<ChangeType>create_party</ChangeType>
	<Id>2</Id>
	<Name><![CDATA[张三]]></Name>
	<ParentId><![CDATA[1]]></ParentId>
	<Order>1</Order>
</xml>
```
