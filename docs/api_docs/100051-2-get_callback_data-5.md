# 添加程序

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100051](https://developer.work.weixin.qq.com/document/path/100051)
- **文档 ID**: `100051`
- **API 名称**: `get_callback_data`
- **请求方法**: `POST`
- **接口地址**: `/get_callback_data`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

获取回调数据能力

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| notify_id | string | 是 | 通知ID |

### 请求示例

```json
{"program_id": "xxx","ability_id": "get_callback_data","notify_id": "xxx","request_data": "{}"}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
| event_type | string | 事件类型 |
| timestamp | int32 | 时间戳 |
| chat_archive_audit_approved | object | 客户同意进行聊天内容存档事件回调 |
| conversation_new_message | object | 产生会话回调通知 |
| hit_keyword | object | 命中关键词规则通知 |
| auth_knowledge_base | object | 知识集管理回调 |
| chat_archive_export_finished | object | 会话内容导出完成通知 |
