# 获取任务结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100036](https://developer.work.weixin.qq.com/document/path/100036)
- **文档 ID**: `100036`
- **API 名称**: `get_spam_result`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/get_spam_result`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

可调用本接口获取反垃圾分析任务的结果。

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
| status | int32 | 任务执行状态 0: 执行未完成 1: 执行完成 2: 执行失败 |
| analyze_result_list | object[] | 消息分析结果列表 |
| analyze_result_list[].errcode | int32 | 错误码 |
| analyze_result_list[].errmsg | string | 错误码说明 |
| analyze_result_list[].msgid | string | 消息对应的msgid |
| analyze_result_list[].spam_result | int32 | 反垃圾分析结果 0: 无违规 1: 政治敏感 2: 色情 |
