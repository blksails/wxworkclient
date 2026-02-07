# 获取自定义模型结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99835](https://developer.work.weixin.qq.com/document/path/99835)
- **文档 ID**: `99835`
- **API 名称**: `get_model_task_result`
- **请求方法**: `POST`
- **接口地址**: `get_model_task_result`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

通过SDK调用，具体方式参考专区程序使用指引。

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
| response_errcode | int32 | 自有模型上报的错误码 |
| response_data | string | 自有模型上报的结果，必顥符合模型能力对应的输出协议 |
