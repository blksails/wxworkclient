# 分块上传文件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98005](https://developer.work.weixin.qq.com/document/path/98005)
- **文档 ID**: `98005`
- **API 名称**: `file_upload_part`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/wedrive/file_upload_part?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

将文件内容按2M分块，依次请求分块上传文件接口。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| upload_key | string | 是 | 文件上传凭证。file_upload_init返回的upload_key |
| index | int32 | 是 | 文件分块号。文件内容按2M分块，从1开始 |
| file_base64_content | string | 是 | 分块的文件内容base64。（注意：只需要填入文件内容的Base64，不需要添加任何如:"data:application/x-javascript;base64" 的数据类型描述信息） |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
