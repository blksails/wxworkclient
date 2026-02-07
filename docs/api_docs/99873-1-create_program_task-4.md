# 创建自有分析程序任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99873](https://developer.work.weixin.qq.com/document/path/99873)
- **文档 ID**: `99873`
- **API 名称**: `create_program_task`
- **请求方法**: `POST`
- **接口地址**: `create_program_task`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

开发者可调用本接口传入会话内容，使用自己上传的分析程序进行会话分析。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| program_id | string | 是 | 应用关联的程序id |
| ability_id | string | 是 | 能力id |
| msg_list | object[] | 是 | 消息列表，最多1000个 |
| msg_list[].msgid | string | 是 | 每条消息对应的msgid。多次出现同一个msgid，以首次出现的为准。目前支持文本、语音、音频存档消息 |
| msg_list[].encrypt_info.secret_key | string | 是 | 该消息的密钥，将encrypted_secret_key用RSA私钥解密后得到 |
| debug_info | object | 否 | 仅当处于调试模式时生效，将使用此字段下的内容而不是实际的消息来替换对应的占位符。 |
| debug_info.chat | string | 是 | 将用于替换{chat}占位符 |
| debug_info.chat_content | string | 是 | 将用于替换{chatcontent}占位符 |
| escape_type | int32 | 否 | 传入自有模型的内容的转义方式 会被转义的字符包括`"`、`\`、`/`、`\b`、`\f`、`\n`、`\r`、`\t` 该字段为0时，这些字符将被转义成空格； 该字段为1时，这些字符将分别被转义成`\"`、`\\`、`\/`、`\b`、`\f`、`\n`、`\r`、`\t` 默认为0 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| jobid | string | 任务id。首次提交时返回 |
| fail_list | object[] | 提交出错的消息列表，只有msgid重复项返回至该列表 |
| fail_list[].errcode | int32 | 错误码 |
| fail_list[].errmsg | string | 错误码说明 |
| fail_list[].msgid | string | 每条消息对应的msgid。与入参对应 |
| fail_list[].encrypt_info | object | 每条消息对应的加密信息。与入参对应 |
| fail_list[].encrypt_info.secret_key | string | 加密消息用的secret_key |
