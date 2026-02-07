# 分块上传完成

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98005](https://developer.work.weixin.qq.com/document/path/98005)
- **文档 ID**: `98005`
- **API 名称**: `file_upload_finish`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/wedrive/file_upload_finish?access_token=ACCESS_TOKEN`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

请求分块上传完成接口，流程结束，完成上传。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| upload_key | string | 是 | 文件上传凭证。file_upload_init返回的upload_key |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| fileid | string | 文件fileid |
