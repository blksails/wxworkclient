# 新增家长事件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/92051](https://developer.work.weixin.qq.com/document/path/92051)
- **文档 ID**: `92051`
- **API 名称**: `create_parent`
- **请求方法**: `POST`
- **接口地址**: `https://wwSuiteId.wxAuthCorpId/change_school_contact`
- **分组信息**: 第 4 个接口，共 8 个

## 接口描述

当学校在家校通讯录中新增家长时，回调此事件至第三方应用/套件的指令回调URL。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| SuiteId | string | 是 | 第三方应用ID |
| AuthCorpId | string | 是 | 授权企业的CorpID |
| InfoType | string | 是 | 固定为change_school_contact |
| TimeStamp | string | 是 | 时间戳 |
| ChangeType | string | 是 | 此时固定为create_parent |
| Id | string | 是 | 新增家长的家校通讯录userid |

### 请求示例

```xml
<xml>
    <SuiteId><![CDATA[wwSuiteId]]></SuiteId>
    <AuthCorpId><![CDATA[wxAuthCorpId]]></AuthCorpId>
    <InfoType><![CDATA[change_school_contact]]></InfoType>
    <TimeStamp>1403610513</TimeStamp>
    <ChangeType><![CDATA[create_parent]]></ChangeType>
    <Id><![CDATA[zhangsan]]></Id>
</xml>
```
