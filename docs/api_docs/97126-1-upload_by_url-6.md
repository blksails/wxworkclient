# 生成异步上传任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97126](https://developer.work.weixin.qq.com/document/path/97126)
- **文档 ID**: `97126`
- **API 名称**: `upload_by_url`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/media/upload_by_url?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

为了满足临时素材的大文件诉求（最高支持200M），支持指定文件的CDN链接，由企微微信后台异步下载和处理，处理完成后回调通知任务完成，再通过接口主动查询任务结果。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| scene | uint32 | 是 | 场景值。1-客户联系入群欢迎语素材 |
| type | string | 是 | 媒体文件类型。目前仅支持video-视频，file-普通文件 |
| filename | string | 是 | 文件名，标识文件展示的名称 |
| url | string | 是 | 文件cdn url。url要求支持Range分块下载 |
| md5 | string | 是 | 文件md5。对比从url下载下来的文件md5是否一致 |

### 请求示例

```json
{
    "scene": 1,
    "type": "video",
    "filename": "video.mp4",
    "url": "https://xxxx",
    "md5": "MD5"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 错误码描述 |
| jobid | string | 任务id。可通过此jobid查询结果 |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok",
   "jobid": "jobid"
}
```
