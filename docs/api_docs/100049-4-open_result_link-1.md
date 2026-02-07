# 会话展示组件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100049](https://developer.work.weixin.qq.com/document/path/100049)
- **文档 ID**: `100049`
- **API 名称**: `open_result_link`
- **分组信息**: 第 4 个接口，共 7 个

## 接口描述

以链接形式展示异步任务结果

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| result-id | string | 是 | 异步任务结果 ID |
| message-id | string | 是 | 消息密钥（与 result 结果相关的任一消息） |
| secret-key | string | 是 | 消息密钥（与 message-id 配对一致的 secret-key） |
