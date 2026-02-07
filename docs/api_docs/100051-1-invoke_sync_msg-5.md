# 添加程序

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100051](https://developer.work.weixin.qq.com/document/path/100051)
- **文档 ID**: `100051`
- **API 名称**: `invoke_sync_msg`
- **请求方法**: `POST`
- **接口地址**: `/invoke_sync_msg`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

调用专区程序获取会话记录能力

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| cursor | string | 是 | 游标 |
| limit | int32 | 是 | 限制数量 |
| token | string | 是 | 访问令牌 |

### 请求示例

```json
{"program_id": "xxx","ability_id": "invoke_sync_msg","request_data": "{\"cursor\":\"xxx\",\"token\":\"xxx\",\"limit\":200}"}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
| has_more | int32 | 是否还有更多数据 |
| next_cursor | string | 下一个游标 |
| msg_list | object[] | 消息列表 |
