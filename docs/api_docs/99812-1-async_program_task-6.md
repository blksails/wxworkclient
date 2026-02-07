# 创建专区程序调用任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99812](https://developer.work.weixin.qq.com/document/path/99812)
- **文档 ID**: `99812`
- **API 名称**: `async_program_task`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/async_program_task`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

用于创建专区程序调用任务

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 访问令牌 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| program_id | string | 是 | 应用关联的程序id |
| ability_id | string | 是 | 程序关联的能力id |
| request_data | string | 是 | 请求的输入JSON，要求与配置的格式匹配 |

### 请求示例

```json
{
  "program_id": "xxx",
  "ability_id": "xxx",
  "request_data": "{\"input\":\"xxx\"}"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| jobid | string | 任务id |

### 响应示例

```json
{
  "errcode": 0,
  "errmsg": "ok",
  "jobid": "JOBID"
}
```
