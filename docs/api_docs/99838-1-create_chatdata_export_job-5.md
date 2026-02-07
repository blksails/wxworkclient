# 创建会话内容导出任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99838](https://developer.work.weixin.qq.com/document/path/99838)
- **文档 ID**: `99838`
- **API 名称**: `create_chatdata_export_job`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/create_chatdata_export_job`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

通过此接口，创建专区消息内容导出异步任务。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | string | 是 | 从会话展示组件获取的code，只能使用一次，有效时间为五分钟 |
| media_id | string | 是 | 导出内容的模板文件media_id，支持Word(doc/docx)、Excel(xls/xlsx)和Txt(txt)格式的文件 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| jobid | string | 所创建任务的任务id |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
    "jobid": "xxxxx"
}
```
