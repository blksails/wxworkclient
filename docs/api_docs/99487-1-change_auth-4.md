# 授权通知事件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99487](https://developer.work.weixin.qq.com/document/path/99487)
- **文档 ID**: `99487`
- **API 名称**: `change_auth`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/change_auth?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

企业更改授权的获客助手链接时，会回调change_auth事件。此时可调用获取获客助手授权链接列表接口查询当前授权的链接。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| SuiteId | string | 是 | 获客助手组件的SuiteId |
| InfoType | string | 是 | 事件类型：可以为create_auth/change_auth/cancel_auth |
| TimeStamp | string | 是 | 时间戳 |
| AuthCorpId | string | 是 | 授权方的corpid，change_auth和cancel_auth事件中返回 |
| State | string | 否 | 构造授权链接指定的state参数，create_auth和change_auth事件中返回 |

### 请求示例

```xml
<xml>
    <SuiteId><![CDATA[wxexxx]]></SuiteId>
    <InfoType><![CDATA[change_auth]]></InfoType>
    <TimeStamp>1341673221</TimeStamp>
    <AuthCorpId><![CDATA[CORPID]]></AuthCorpId>
</xml>
```
