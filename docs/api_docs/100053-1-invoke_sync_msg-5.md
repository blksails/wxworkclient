# 添加程序

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100053](https://developer.work.weixin.qq.com/document/path/100053)
- **文档 ID**: `100053`
- **API 名称**: `invoke_sync_msg`
- **请求方法**: `POST`
- **接口地址**: `/invoke_sync_msg`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

添加获取会话记录能力

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| cursor | string | 否 | 游标 |
| limit | int32 | 否 | 限制数量 |
| token | string | 否 | 令牌 |

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
| msg_list[].msgid | string | 消息ID |
| msg_list[].sender | object | 发送者信息 |
| msg_list[].receiver_list | object[] | 接收者列表 |
| msg_list[].chatid | string | 聊天ID |
| msg_list[].send_time | int32 | 发送时间 |
| msg_list[].msgtype | int32 | 消息类型 |
| msg_list[].service_encrypt_info | object | 服务加密信息 |
| msg_list[].service_encrypt_info.encrypted_secret_key | string | 加密密钥 |
| msg_list[].service_encrypt_info.public_key_ver | int32 | 公钥版本 |
