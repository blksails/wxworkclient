# 创建自定义模型任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100035](https://developer.work.weixin.qq.com/document/path/100035)
- **文档 ID**: `100035`
- **API 名称**: `create_model_task`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/create_model_task`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

通过SDK调用，创建自定义模型任务。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| model_id | string | 是 | 模型id |
| ability_id | string | 是 | 模型能力id |
| kb_id | string | 否 | 知识集id |
| tag_group_list | object[] | 否 | 客户标签组列表 |
| tag_group_list[].group_id | string | 是 | 每个id代表一个客户标签组 |
| msg_list | object[] | 是 | 消息列表，最多1000个 |
| msg_list[].msgid | string | 是 | 每条消息对应的msgid。支持文本、语音、音频存档消息 |
| msg_list[].encrypt_info.secret_key | string | 是 | 消息的密钥，用RSA私钥解密后得到 |
| debug_info | object | 否 | 调试模式下的内容替换 |
| debug_info.chat | string | 是 | 替换{chat}占位符 |
| debug_info.chat_content | string | 是 | 替换{chatcontent}占位符 |
| debug_info.knowledge | string | 否 | 替换{knowledge}占位符 |
| debug_info.tagjson | string | 否 | 替换{tagjson}占位符 |
| escape_type | int32 | 否 | 自有模型的内容的转义方式，0或1，默认为0 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| jobid | string | 任务id |
| fail_list | object[] | 提交出错的消息列表 |
