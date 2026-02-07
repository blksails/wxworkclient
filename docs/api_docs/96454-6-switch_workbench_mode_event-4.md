# 修改设置工作台自定义开关事件推送

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96454](https://developer.work.weixin.qq.com/document/path/96454)
- **文档 ID**: `96454`
- **API 名称**: `switch_workbench_mode_event`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/agent/switch_workbench_mode_event?access_token=ACCESS_TOKEN`
- **分组信息**: 第 6 个接口，共 6 个

## 接口描述

修改设置工作台自定义开关事件推送

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| agentid | uint32 | 是 | 企业应用的id |
| mode | int32 | 是 | 1表示开启工作台自定义模式，0表示关闭工作台自定义模式 |

### 请求示例

```xml
<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[FromUser]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[switch_workbench_mode]]></Event>
<Mode>1</Mode
<AgentID>1</AgentID>
</xml>
```
