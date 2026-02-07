# 获取获客链接列表

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99484](https://developer.work.weixin.qq.com/document/path/99484)
- **文档 ID**: `99484`
- **API 名称**: `list_link`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/customer_acquisition/list_link?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

服务商可通过此接口获取授权给获客助手组件的链接。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| limit | uint32 | 否 | 返回的最大记录数，最大值100 |
| cursor | string | 否 | 用于分页查询的游标，由上一次调用返回，首次调用可不填 |

### 请求示例

```json
{
   "limit":100,
   "cursor":"CURSOR"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| link_id_list | array | link_id列表 |
| next_cursor | string | 分页游标，在下次请求时填写以获取之后分页的记录 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
	"link_id_list":
	[
		"LINK_ID_AAA",
		"LINK_ID_BBB",
		"LINK_ID_CCC"
	],
	"next_cursor":"CURSOR"
}
```
