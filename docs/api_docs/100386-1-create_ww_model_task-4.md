# 创建企微通用模型任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100386](https://developer.work.weixin.qq.com/document/path/100386)
- **文档 ID**: `100386`
- **API 名称**: `create_ww_model_task`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/create_ww_model_task`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

通过SDK调用创建企微通用模型任务。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ability_id | string | 是 | 模型能力id |
| tag_group_list[].group_id | string | 否 | 客户标签组列表 |
| kb_id | string | 否 | 知识集id |
| kb_retrieval_words | string | 否 | 用于从知识集中检索相关内容 |
| msg_list | object[] | 否 | 消息列表，最多1000个 |
| msg_list[].msgid | string | 是 | 每条消息对应的msgid |
| msg_list[].encrypt_info.secret_key | string | 是 | 该消息的密钥 |
| model_id | string | 否 | 调用的模型id |
| need_think_result | bool | 否 | 是否返回模型的思考过程部分 |
| var_args | object[] | 否 | 自定义变量列表，最多50个 |
| var_args[].name | string | 是 | 自定义变量名 |
| var_args[].value | string | 是 | 自定义变量值 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
| jobid | string | 任务id |
| fail_list | object[] | 提交出错的消息列表 |
| fail_list[].errcode | int32 | 错误码 |
| fail_list[].errmsg | string | 错误信息 |
| fail_list[].msgid | string | 每条消息对应的msgid |
| fail_list[].encrypt_info.secret_key | string | 加密消息用的secret_key |
