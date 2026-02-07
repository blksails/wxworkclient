# 获取自有分析程序结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100038](https://developer.work.weixin.qq.com/document/path/100038)
- **文档 ID**: `100038`
- **API 名称**: `get_program_task_result`
- **请求方法**: `POST`
- **接口地址**: `get_program_task_result`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

通过SDK调用，获取自有分析程序的结果。

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
| fail_list | array | 错误的消息列表，如msgid不存在、非文本等 |
| response_errcode | int32 | 专区程序返回的错误码 |
| response_data | string | 专区程序的输出结果，为自定义的JSON字符串 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
    "fail_list":[{
        "errcode": 710601,
        "errmsg": "xxx",
        "msgid": "MSGID"
    }],
	"response_errcode": 0,
	"response_data": "{\"output\":\"xxx\"}"
}
```
