# 获取自有分析程序结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99873](https://developer.work.weixin.qq.com/document/path/99873)
- **文档 ID**: `99873`
- **API 名称**: `get_program_task_result`
- **请求方法**: `POST`
- **接口地址**: `get_program_task_result`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

通过SDK调用，获取自有分析程序结果。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| jobid | string | 是 | 任务id |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| fail_list | object[] | 错误的消息列表，如msgid不存在、非文本等 |
| fail_list[].errcode | int32 | 错误码 |
| fail_list[].errmsg | string | 错误码说明 |
| fail_list[].msgid | string | 每条消息对应的msgid，与入参对应 |
| response_errcode | int32 | 专区程序返回的错误码 |
| response_data | string | 专区程序的输出结果，为自定义的JSON字符串 |
