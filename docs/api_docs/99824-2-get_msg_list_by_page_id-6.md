# page_id获取消息列表

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99824](https://developer.work.weixin.qq.com/document/path/99824)
- **文档 ID**: `99824`
- **API 名称**: `get_msg_list_by_page_id`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/get_msg_list_by_page_id`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

通过page_id获取消息列表。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page_id | string | 是 | [sync_msg](#%E8%8E%B7%E5%8F%96%E4%BC%9A%E8%AF%9D%E8%AE%B0%E5%BD%95)返回 |

### 请求示例

```json
{
	"page_id": "PAGEID"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| msg_list | object[] | 消息列表，字段详细描述见[sync_msg](#sync_msg_field_desc) |

### 响应示例

```json
{
    "errcode":0,
    "errmsg":"ok",
    "msg_list":[
    ]
}
```
