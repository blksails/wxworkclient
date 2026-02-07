# 获取情感分析结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100034](https://developer.work.weixin.qq.com/document/path/100034)
- **文档 ID**: `100034`
- **API 名称**: `get_sentiment_result`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/get_sentiment_result`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

通过SDK调用，获取情感分析结果。

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
| errmsg | string | 错误信息 |
| status | int32 | 任务执行状态 0: 执行未完成 1: 执行完成 2: 执行失败 |
| analyze_result_list | object[] | 消息分析结果列表。详见**ItemResult** |
| analyze_result_list[].errcode | int32 | 错误码 |
| analyze_result_list[].errmsg | string | 错误码说明 |
| analyze_result_list[].msgid | string | 消息对应的msgid |
| analyze_result_list[].sentiment_result | int32 | 情感分析结果 0: 无情感 1: 正面 2: 负面 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
    "status": 1,
    "analyze_result_list":[
        {
            "errcode": 0,
            "errmsg": "ok",
            "msgid": "MSGID1",
            "sentiment_result": 2
        },
        {
            "errcode": 710601,
            "errmsg": "xxx",
            "msgid": "MSGID4"
        }
    ]
}
```
