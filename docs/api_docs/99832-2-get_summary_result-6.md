# 获取摘要提取结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99832](https://developer.work.weixin.qq.com/document/path/99832)
- **文档 ID**: `99832`
- **API 名称**: `get_summary_result`
- **请求方法**: `POST`
- **接口地址**: `get_summary_result`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

应用在专区的程序可调用本组接口获取摘要提取结果。

## 请求信息

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
| status | int32 | 任务执行状态 0: 执行未完成 1: 执行完成 2: 执行失败 |
| fail_list | object[] | 错误的消息列表，如msgid不存在、非文本等，详见“创建标签匹配任务”的FailMsg说明 |
| response_data | string | 摘要提取的结果 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
    "status": 1,
    "fail_list":[{
        "errcode": 710601,
        "errmsg": "xxx",
        "msgid": "MSGID2"
    }],
    "response_data": "xxx"
}
```
