# 创建自定义模型任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99835](https://developer.work.weixin.qq.com/document/path/99835)
- **文档 ID**: `99835`
- **API 名称**: `create_model_task`
- **请求方法**: `POST`
- **接口地址**: `create_model_task`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

通过SDK调用，具体方式参考专区程序使用指引。应用在专区中的程序可调用本接口传入会话内容，使用自己上传的大语言模型进行会话分析。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| model_id | string | 是 | 模型id |
| ability_id | string | 是 | 模型能力id |
| kb_id | string | 否 | 知识集id。若同时传kb_id跟service_kb_id，则忽略service_kb_id |
| tag_group_list | object[] | 否 | 客户标签组列表 |
| tag_group_list[].group_id | string | 是 | 每个id代表一个客户标签组 |
| msg_list | object[] | 是 | 消息列表，最多1000个 |
| msg_list[].msgid | string | 是 | 每条消息对应的msgid。多次出现同一个msgid，以首次出现的为准。目前支持文本、语音、音频存档消息 |
| msg_list[].encrypt_info.secret_key | string | 是 | 该消息的密钥，将encrypted_secret_key用RSA私钥解密后得到 |
| debug_info | object | 否 | 仅当处于调试模式时生效，将使用此字段下的内容而不是实际的知识集/标签组/消息来替换对应的占位符 |
| debug_info.chat | string | 是 | 将用于替换{chat}占位符 |
| debug_info.chat_content | string | 是 | 将用于替换{chatcontent}占位符 |
| debug_info.knowledge | string | 否 | 将用于替换{knowledge}占位符 |
| debug_info.tagjson | string | 否 | 将用于替换{tagjson}占位符 |
| escape_type | int32 | 否 | 传入自有模型的内容的转义方式。会被转义的字符包括`"`、`\`、`/`、`\b`、`\f`、`\n`、`\r`、`\t`。默认为0 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| jobid | string | 任务id。首次提交时返回 |
| fail_list | object[] | 提交出错的消息列表，只有msgid重复项返回至该列表 |
