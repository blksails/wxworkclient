# 创建标签匹配任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99833](https://developer.work.weixin.qq.com/document/path/99833)
- **文档 ID**: `99833`
- **API 名称**: `create_customer_tag_task`
- **请求方法**: `POST`
- **接口地址**: `create_customer_tag_task`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

应用在专区的程序可调用本接口传入一批会话内容，进行标签匹配。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| tag_group_list[].group_id | string | 是 | 每个id代表一个客户标签组。 |
| msg_list[].msgid | string | 是 | 每条消息对应的msgid。多次出现同一个msgid，以首次出现的为准。目前支持文本、语音、音频存档消息 |
| msg_list[].encrypt_info.secret_key | string | 是 | 该消息的密钥，将encrypted_secret_key用RSA私钥解密后得到 |
| model_id | string | 否 | 模型id。不指定则使用企微后台默认的大语言模型 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| jobid | string | 任务id。首次提交时返回 |
| fail_list[].errcode | int32 | 错误码 |
| fail_list[].errmsg | string | 错误码说明 |
| fail_list[].msgid | string | 每条消息对应的msgid，与入参对应 |
| fail_list[].encrypt_info.secret_key | string | 加密消息用的secret_key |
