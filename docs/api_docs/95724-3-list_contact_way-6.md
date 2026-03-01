# 获取企业已配置的「联系我」列表

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95724](https://developer.work.weixin.qq.com/document/path/95724)
- **文档 ID**: `95724`
- **API 名称**: `list_contact_way`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/list_contact_way?access_token=ACCESS_TOKEN`
- **分组信息**: 第 3 个接口，共 6 个

## 接口描述

获取企业配置的「联系我」二维码和「联系我」小程序插件列表（不包含临时会话）。注意：仅可获取2021年7月10日以后创建的「联系我」。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| start_time | int32 | 否 | 「联系我」创建起始时间戳，默认为90天前 |
| end_time | int32 | 否 | 「联系我」创建结束时间戳，默认为当前时间 |
| cursor | string | 否 | 分页查询游标，为上次请求返回的next_cursor |
| limit | int32 | 否 | 每次查询分页大小，默认为100，最大1000 |

### 请求示例

```json
{
   "start_time":1622476800,
   "end_time":1625068800,
   "cursor":"CURSOR",
   "limit":1000
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| contact_way | object[] | 联系方式列表 |
| contact_way[].config_id | string | 联系方式的配置id |
| next_cursor | string | 分页参数，用于查询下一个分页的数据；为空表示没有更多分页 |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok",
    "contact_way":
	[
		{
			"config_id":"534b63270045c9ABiKEE814ef56d91c62f"
		},
		{
			"config_id":"87bBiKEE811c62f63270041c62f5c9A4ef"
		}
	],
	"next_cursor":"NEXT_CURSOR"
}
```
