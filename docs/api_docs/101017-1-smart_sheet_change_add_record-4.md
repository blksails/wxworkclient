# 新增记录事件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/101017](https://developer.work.weixin.qq.com/document/path/101017)
- **文档 ID**: `101017`
- **API 名称**: `smart_sheet_change_add_record`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/callback/record_change/add`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

当成员在API创建的智能表格上修改了记录后，触发该事件。RecordId一次最多回调1000个，超过会分批回调

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ToUserName | string | 是 | 企业微信CorpID |
| FromUserName | string | 是 | 本企业成员为userid，非本企业成员为tmp_external_userid |
| CreateTime | uint32 | 是 | 消息创建时间，unix时间戳 |
| MsgType | string | 是 | 消息类型，固定为：event |
| Event | string | 是 | 事件类型，固定为：smart_sheet_change |
| ChangeType | string | 是 | 事件类型，固定为：add_record |
| DocId | string | 是 | 文档ID |
| SheetId | string | 是 | 子表ID |
| RecordId | string[] | 是 | 记录ID列表 |

### 请求示例

```xml
<xml>
   <ToUserName><![CDATA[toUser]]></ToUserName>
   <FromUserName><![CDATA[fromUser]]></FromUserName>
   <CreateTime>1348831860</CreateTime>
   <MsgType><![CDATA[event]]></MsgType>
   <Event><![CDATA[smart_sheet_change]]></Event>
   <ChangeType><![CDATA[add_record]]></ChangeType>
   <DocId><![CDATA[dcjgewCwAAqeJcPI1d8Pwbjt7nttzAAA]]></DocId>
   <SheetId><![CDATA[SheetId]]></SheetId>
   <RecordId><![CDATA[RecordId1]]></RecordId>
   <RecordId><![CDATA[RecordId2]]></RecordId>
</xml>
```
