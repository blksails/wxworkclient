# 创建知识集

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100030](https://developer.work.weixin.qq.com/document/path/100030)
- **文档 ID**: `100030`
- **API 名称**: `knowledge_base_create`
- **请求方法**: `POST`
- **接口地址**: `knowledge_base_create`
- **分组信息**: 第 2 个接口，共 7 个

## 接口描述

通过SDK调用，具体方式参考专区程序使用指引。创建知识集。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| kb_id | string | 是 | 知识集ID |
| doc_list | object[] | 是 | 内容列表 可填充个数：1 ~ 1000。每个知识集的内容总数量不能超过1000 |
| doc_list.doc_name | string | 是 | 内容名，如果是文件，需要有准确的文件名后缀 不多于200字节 |
| doc_list.type | uint32 | 是 | 内容类型 取值范围： 2 - pdf 4 - xlsx 5 - doc 6 - docx 101 - 网页链接 |
| doc_list.file_media_id | string | 否 | 专区临时文件ID。当type非网页链接时必传 通过上传临时文件到专区接口获取 不多于1024字节 |
| doc_list.web_url | string | 否 | 网页链接。当type为网页链接时必传，以http或https开头的链接 不多于1024字节 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 错误码描述 |
| kb_id | string | 知识集ID |
| doc_list | object[] | 内容列表 |
