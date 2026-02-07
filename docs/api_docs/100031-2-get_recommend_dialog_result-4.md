# 获取话术推荐结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100031](https://developer.work.weixin.qq.com/document/path/100031)
- **文档 ID**: `100031`
- **API 名称**: `get_recommend_dialog_result`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
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
| status | int32 | 任务执行状态 0: 执行未完成 1: 执行完成 2: 执行失败 |
| fail_list | object[] | 错误的消息列表，如msgid不存在、非文本等 |
| response_data | string | 话术推荐的结果 |
