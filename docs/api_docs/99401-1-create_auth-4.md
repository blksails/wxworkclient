# 授权成功通知

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99401](https://developer.work.weixin.qq.com/document/path/99401)
- **文档 ID**: `99401`
- **API 名称**: `create_auth`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/create_auth`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

企业授权微信客服组件时，企业微信后台会推送授权成功通知。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| SuiteId | string | 是 | 套件ID |
| AuthCode | string | 是 | 授权码 |
| InfoType | string | 是 | 信息类型 |
| TimeStamp | uint32 | 是 | 时间戳 |
| State | string | 是 | 状态 |
| ExtraInfo.AuthOpenKfIdList | object[] | 是 | 用户本次授权的客服账号列表 |

### 请求示例

```xml
<xml>
    <SuiteId><![CDATA[wxxxxxxx]]></SuiteId>
    <AuthCode><![CDATA[AUTHCODE]]></AuthCode>
    <InfoType><![CDATA[create_auth]]></InfoType>
    <TimeStamp>1403610513</TimeStamp>
    <State><![CDATA[STATE]]></State>
    <ExtraInfo>
        <AuthOpenKfIdList>
            <OpenKfId><![CDATA[wk11111]]></OpenKfId>
            <OpenKfId><![CDATA[wk22222]]></OpenKfId>
            <OpenKfId><![CDATA[wk33333]]></OpenKfId>
        </AuthOpenKfIdList>
    </ExtraInfo>
</xml>
```
