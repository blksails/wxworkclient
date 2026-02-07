# 查询异步任务结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97126](https://developer.work.weixin.qq.com/document/path/97126)
- **文档 ID**: `97126`
- **API 名称**: `get_upload_by_url_result`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/media/get_upload_by_url_result?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

查询异步上传任务的结果。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| jobid | string | 是 | 任务id。最长为128字节，60分钟内有效 |

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
| errcode | int32 | 返回码 |
| errmsg | string | 错误码描述 |
| status | string | 任务状态。1-处理中，2-完成，3-异常失败 |
| detail | obj | 结果明细 |
| detail.errcode | int32 | 任务失败返回码。当status为3时返回非0，其他返回0 |
| detail.errmsg | string | 任务失败错误码描述 |
| detail.media_id | string | 媒体文件上传后获取的唯一标识，3天内有效。当status为2时返回 |
| detail.created_at | string | 媒体文件创建的时间戳。当status为2时返回 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
    "status": 2,
    "detail": {
        "errcode": 0,
        "errmsg": "ok",
        "media_id": "3*1*G6nrLmr5EC3MMb_-zK1dDdzmd0p7cNliYu9V5w7o8K0",
        "created_at": "1380000000"
    }
}
```
