# 接口创建文档表现

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97463](https://developer.work.weixin.qq.com/document/path/97463)
- **文档 ID**: `97463`
- **API 名称**: `create_document`
- **请求方法**: `POST`
- **接口地址**: `https://wework.qpic.cn/wwpic/180018_cUam_qCLSRC9r0w_1669789077/0`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

接口创建的文档和收集表将在文档应用中标识出应用创建的信息，文档图标也将替换为应用图标。接口创建的文档和收集表可添加企业成员进入通知范围，仅应用可编辑文档内容，成员无法编辑，但指定的管理员可以修改通知范围和获取收集表数据。通过接口创建、修改、删除文档或收集表后，文档应用将自动向文档或收集表相关成员推送通知。

## 请求信息

### 请求示例

```text
POST https://wework.qpic.cn/wwpic/180018_cUam_qCLSRC9r0w_1669789077/0

Headers:
Content-Type: application/json
Authorization: Bearer ACCESS_TOKEN

Body:
{
  "doc_name": "New Document",
  "content": "This is a new document created by the application."
}
```
