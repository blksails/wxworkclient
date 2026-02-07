# 分块上传初始化

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98005](https://developer.work.weixin.qq.com/document/path/98005)
- **文档 ID**: `98005`
- **API 名称**: `file_upload_init`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/wedrive/file_upload_init?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

请求分块上传初始化接口，如果命中秒传，则流程结束，完成上传。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| spaceid | string | 否 | 空间spaceid |
| fatherid | string | 否 | 当前目录的fileid，根目录时为空间spaceid |
| selected_ticket | string | 否 | [微盘和文件选择器jsapi](#40357)返回的selectedTicket。若填此参数，则不需要填`spaceid`/`fatherid`。 |
| file_name | string | 是 | 文件名字 |
| size | uint64 | 是 | 文件大小。最大支持20G |
| block_sha | string[] | 是 | 文件分块累积sha值，按分块顺序填入数组。参考[附录-分块累积sha说明](#40102/%E9%99%84%E5%BD%95-%E5%88%86%E5%9D%97%E7%B4%AF%E7%A7%AFsha%E8%AF%B4%E6%98%8E) |
| skip_push_card | bool | 否 | 文件创建完成时是否推送企业微信卡片。默认false，即默认推送卡片 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| hit_exist | bool | 是否命中秒传 |
| upload_key | string | 文件上传凭证。不命中秒传时返回，作为file_upload_part参数 |
| fileid | string | 文件fileid。命中秒传时返回，此时上传流程完成 |
