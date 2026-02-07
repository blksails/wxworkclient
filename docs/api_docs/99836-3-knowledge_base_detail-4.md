# 获取知识集详情

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99836](https://developer.work.weixin.qq.com/document/path/99836)
- **文档 ID**: `99836`
- **API 名称**: `knowledge_base_detail`
- **请求方法**: `POST`
- **接口地址**: `knowledge_base_detail`
- **分组信息**: 第 3 个接口，共 7 个

## 接口描述

通过SDK调用，获取知识集详情。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| kb_id | string | 是 | 知识集ID |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 错误码描述 |
| kb_id | string | 知识集ID |
| kb_name | string | 知识集名称 |
| doc_list | object[] | 内容列表 |
