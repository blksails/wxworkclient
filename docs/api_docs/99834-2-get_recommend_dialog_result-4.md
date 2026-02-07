# 获取话术推荐结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99834](https://developer.work.weixin.qq.com/document/path/99834)
- **文档 ID**: `99834`
- **API 名称**: `get_recommend_dialog_result`
- **请求方法**: `POST`
- **接口地址**: `get_recommend_dialog_result`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

应用在专区的程序可调用本接口传入会话内容，通过模型进行话术推荐。

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
| status | int32 | 任务执行状态 0: 执行未完成 1: 执行完成 2: 执行失败 |
| fail_list | object[] | 错误的消息列表，如msgid不存在、非文本等，详见“创建话术推荐任务”的FailMsg说明 |
| response_data | string | 话术推荐的结果 |
