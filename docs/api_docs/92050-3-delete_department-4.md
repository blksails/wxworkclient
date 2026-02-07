# 删除部门事件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/92050](https://developer.work.weixin.qq.com/document/path/92050)
- **文档 ID**: `92050`
- **API 名称**: `delete_department`
- **请求方法**: `POST`
- **接口地址**: `https://wwSuiteId`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

当学校删除家校通讯录部门时，回调此事件至第三方应用/套件的指令回调URL。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| SuiteId | string | 是 | 第三方应用ID |
| AuthCorpId | string | 是 | 授权企业的CorpID |
| InfoType | string | 是 | 事件的类型，此时固定为change_school_contact |
| TimeStamp | string | 是 | 消息创建时间 （整型） |
| ChangeType | string | 是 | 此时固定为delete_department |
| Id | string | 是 | 删除部门的Id |

### 请求示例

```xml
<xml>
    <SuiteId><![CDATA[wwSuiteId]]></SuiteId>
    <AuthCorpId><![CDATA[wxAuthCorpId]]></AuthCorpId>
    <InfoType><![CDATA[change_school_contact]]></InfoType>
    <TimeStamp>1403610513</TimeStamp>
    <ChangeType><![CDATA[delete_department]]></ChangeType>
    <Id>1</Id>
</xml>
```
