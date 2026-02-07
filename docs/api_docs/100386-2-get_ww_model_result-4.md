# 获取企微通用模型结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100386](https://developer.work.weixin.qq.com/document/path/100386)
- **文档 ID**: `100386`
- **API 名称**: `get_ww_model_result`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/get_ww_model_result`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

通过SDK调用获取企微通用模型结果。

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
| errmsg | string | 错误信息 |
| status | int32 | 任务执行状态 |
| fail_list | object[] | 错误的消息列表 |
| fail_list[].errcode | int32 | 错误码 |
| fail_list[].errmsg | string | 错误信息 |
| fail_list[].msgid | string | 每条消息对应的msgid |
| response_data | string | 企微通用模型的返回结果 |
