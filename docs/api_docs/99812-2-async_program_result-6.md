# 获取专区程序任务结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99812](https://developer.work.weixin.qq.com/document/path/99812)
- **文档 ID**: `99812`
- **API 名称**: `async_program_result`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/async_program_result`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

用于获取专区程序任务结果

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 访问令牌 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| jobid | string | 是 | 任务id |

### 请求示例

```json
{
  "jobid": "JOBID"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| response_errcode | int32 | [上报异步任务结果](#53367)中上报的errcode。代表专区程序返回的错误码 |
| response_data | string | [上报异步任务结果](#53367)中上报的result。代表专区程序的输出结果，为自定义的JSON字符串，要求与管理端配置的**输出协议**格式匹配 |

### 响应示例

```json
{
  "errcode": 0,
  "errmsg": "ok",
  "response_errcode": 0,
  "response_data": "{\"output\":\"xxx\"}"
}
```
