# 获取企微通用模型结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100289](https://developer.work.weixin.qq.com/document/path/100289)
- **文档 ID**: `100289`
- **API 名称**: `get_ww_model_result`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/get_ww_model_result`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

通过SDK调用，获取企微通用模型的结果。

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
| status | int32 | 任务执行状态 |
| fail_list | object[] | 错误的消息列表 |
| response_data | string | 企微通用模型的返回结果 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
	"status": 1,
    "fail_list":[{
        "errcode": 710601,
        "errmsg": "xxx",
        "msgid": "MSGID"
    }],
	"response_data": "RESULT"
}
```
