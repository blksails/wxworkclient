# 获取标签任务结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100032](https://developer.work.weixin.qq.com/document/path/100032)
- **文档 ID**: `100032`
- **API 名称**: `get_customer_tag_result`
- **请求方法**: `POST`
- **接口地址**: `get_customer_tag_result`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

获取标签任务结果。

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
| fail_list[].errcode | int32 | 错误码 |
| fail_list[].errmsg | string | 错误码说明 |
| fail_list[].msgid | string | 每条消息对应的msgid，与入参对应 |
| tag_result_list[].group_id | string | 客户标签组id |
| tag_result_list[].tag_id | string | 命中的标签id |
