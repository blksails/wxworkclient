# 获客助手权限取消事件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98959](https://developer.work.weixin.qq.com/document/path/98959)
- **文档 ID**: `98959`
- **API 名称**: `cancel_special_auth`
- **请求方法**: `POST`
- **接口地址**: `https://ww4asffe99e54c0f4c/cgi-bin/callback`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

当授权企业的管理员取消对于第三方/代开发应用获客助手权限的授权时，企业微信服务器会向应用的“指令回调URL”推送该事件。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| SuiteId | string | 是 | 第三方应用ID |
| AuthCorpId | string | 是 | 授权企业的CorpID |
| InfoType | string | 是 | 固定为cancel_special_auth |
| TimeStamp | string | 是 | 时间戳 |
| AuthType | string | 是 | 此时固定为customer_acquisition |

### 请求示例

```xml
<xml>
	<SuiteId><![CDATA[ww4asffe99e54c0f4c]]></SuiteId>
	<AuthCorpId><![CDATA[wxf8b4f85f3a794e77]]></AuthCorpId>
	<InfoType><![CDATA[cancel_special_auth]]></InfoType>
	<TimeStamp>1403610513</TimeStamp>
	<AuthType><![CDATA[customer_acquisition]]></AuthType>
</xml>
```
