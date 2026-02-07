# 创建话术推荐任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100031](https://developer.work.weixin.qq.com/document/path/100031)
- **文档 ID**: `100031`
- **API 名称**: `create_recommend_dialog_task`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

通过SDK调用，具体方式参考专区程序使用指引。应用在专区的程序可调用本接口传入会话内容，通过模型进行话术推荐。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| kb_id | string | 是 | 大语言模型知识集id，可通过调用「获取知识集列表」接口获取 |
| msg_list | object[] | 是 | 消息列表，最多1000个 |
| msg_list[].msgid | string | 是 | 每条消息对应的msgid。多次出现同一个msgid，以首次出现的为准。目前支持文本、语音、音频存档消息 |
| msg_list[].encrypt_info.secret_key | string | 是 | 该消息的密钥，将encrypted_secret_key用RSA私钥解密后得到 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| jobid | string | 任务id。首次提交时返回 |
| fail_list | object[] | 提交出错的消息列表，只有msgid重复项返回至该列表 |
