# 删除知识集内容

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100030](https://developer.work.weixin.qq.com/document/path/100030)
- **文档 ID**: `100030`
- **API 名称**: `knowledge_base_remove_doc`
- **请求方法**: `POST`
- **接口地址**: `knowledge_base_remove_doc`
- **分组信息**: 第 5 个接口，共 7 个

## 接口描述

通过SDK调用，具体方式参考专区程序使用指引。删除知识集内容。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| kb_id | string | 是 | 知识集ID |
| docid_list | uint64[] | 是 | 要删除的docid列表 可填充个数：1 ~ 1000 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 错误码描述 |
