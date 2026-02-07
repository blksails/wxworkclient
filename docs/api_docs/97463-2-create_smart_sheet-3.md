# 接口创建智能表格的表现

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97463](https://developer.work.weixin.qq.com/document/path/97463)
- **文档 ID**: `97463`
- **API 名称**: `create_smart_sheet`
- **请求方法**: `POST`
- **接口地址**: `https://wework.qpic.cn/wwpic3az/747742_GTt17meRR4W5mF9_1717070671/0`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

接口创建的智能表格将在智能表格中标识出应用创建的信息。应用自动加入智能表格，成员可查询应用信息。成员首次编辑智能表格时，展示 应用可获取编辑内容 提示。

## 请求信息

### 请求示例

```text
POST https://wework.qpic.cn/wwpic3az/747742_GTt17meRR4W5mF9_1717070671/0

Headers:
Content-Type: application/json
Authorization: Bearer ACCESS_TOKEN

Body:
{
  "sheet_name": "New Smart Sheet",
  "content": "This is a new smart sheet created by the application."
}
```
