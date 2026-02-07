# 获客助手权限确认事件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98962](https://developer.work.weixin.qq.com/document/path/98962)
- **文档 ID**: `98962`
- **API 名称**: `approve_special_auth`
- **请求方法**: `POST`
- **接口地址**: `https://ww4asffe99e54c0f4c/cgi-bin/customer_acquisition/approve_special_auth`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

具有获客助手权限的第三方/代开发应用授权后，需要授权企业的管理员进行二次确认后，才可调用相关接口。当授权企业的管理员完成确认后，企业微信服务器会向应用的“指令回调URL”推送该事件。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| SuiteId | string | 是 | 第三方应用ID |
| AuthCorpId | string | 是 | 授权企业的CorpID |
| InfoType | string | 是 | 固定为approve_special_auth |
| TimeStamp | string | 是 | 时间戳 |
| AuthType | string | 是 | 此时固定为customer_acquisition |

### 请求示例

```xml
<xml>
	<SuiteId><![CDATA[ww4asffe99e54c0f4c]]></SuiteId>
	<AuthCorpId><![CDATA[wxf8b4f85f3a794e77]]></AuthCorpId>
	<InfoType><![CDATA[approve_special_auth]]></InfoType>
	<TimeStamp>1403610513</TimeStamp>
	<AuthType><![CDATA[customer_acquisition]]></AuthType>
</xml>
```
