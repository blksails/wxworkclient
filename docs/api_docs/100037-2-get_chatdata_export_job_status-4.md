# 获取会话内容导出任务结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100037](https://developer.work.weixin.qq.com/document/path/100037)
- **文档 ID**: `100037`
- **API 名称**: `get_chatdata_export_job_status`
- **请求方法**: `POST`
- **接口地址**: `get_chatdata_export_job_status`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

通过此接口，获取消息内容导出任务的处理状态。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| jobid | string | 是 | 创建会话内容导出任务接口获得的任务id |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| status | int32 | 任务当前状态，1、等待开始 2、进行中 3、已完成 |
| result_id | string | 结果id，任务处于已完成状态，且任务返回码为0时返回，用于在会话展示组件中展示结果。该结果只可用ww-open-result-link模板组件进行展示。14天内有效。 |
| result_errcode | int32 | 任务返回码，任务处于已完成状态时返回，表示任务的执行结果 |
| result_errmsg | string | 任务返回信息，任务处于已完成状态时返回，对任务返回码的文本描述内容 |
