# 上下游共享应用事件回调

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/93373](https://developer.work.weixin.qq.com/document/path/93373)
- **文档 ID**: `93373`
- **API 名称**: `share_chain_change`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/...`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

本事件触发时机为上游企业把第三方应用共享给下游企业使用或移除下游企业。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| SuiteId | string | 是 | 第三方应用的SuiteId |
| InfoType | string | 是 | share_chain_change |
| TimeStamp | uint32 | 是 | 时间戳 |
| AppId | int32 | 是 | 旧的多应用套件中的对应应用id，新开发者请忽略 |
| CorpId | string | 是 | 上游企业corpid |
| AgentId | int32 | 是 | 上游企业应用id |

### 请求示例

```xml
<xml>
	<SuiteId><![CDATA[ww4asffe99exxx0f4c]]></SuiteId>
	<InfoType><![CDATA[share_chain_change]]></InfoType>
	<TimeStamp>1403610513</TimeStamp>
	<AppId>11</AppId>
	<CorpId>![CDATA[ww11111]]</CorpId>
	<AgentId>11</AgentId>
</xml>
```
