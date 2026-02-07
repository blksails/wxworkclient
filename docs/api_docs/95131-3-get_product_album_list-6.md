# 获取商品图册列表

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95131](https://developer.work.weixin.qq.com/document/path/95131)
- **文档 ID**: `95131`
- **API 名称**: `get_product_album_list`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_product_album_list`
- **分组信息**: 第 3 个接口，共 5 个

## 接口描述

企业和第三方应用可以通过此接口导出商品

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| limit | uint32 | 否 | 返回的最大记录数，整型，最大值100，默认值50，超过最大值时取默认值 |
| cursor | string | 否 | 用于分页查询的游标，字符串类型，由上一次调用返回，首次调用可不填 |

### 请求示例

```json
{
   "limit":50,
   "cursor":"CURSOR"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| next_cursor | string | 用于分页查询的游标，字符串类型，用于下一次调用 |
| product_list | object[] | 商品列表 |
| product_list.product_id | string | 商品id |
| product_list.product_sn | string | 商品编码 |
| product_list.description | string | 商品的名称、特色等 |
| product_list.price | uint32 | 商品的价格，单位为分 |
| product_list.attachments | object[] | 附件类型 |
| product_list.attachments.type | string | 附件类型，目前仅支持image |
| product_list.attachments.image.media_id | string | 图片的media_id，可以通过获取临时素材下载资源 |

### 响应示例

```json
{
	"errcode":0,
	"errmsg":"ok",
	"next_cursor":"CURSOR",
	"product_list":[
		{
			"product_id" : "xxxxxxxxxx",
			"description":"世界上最好的商品",
			"price":30000,
			"product_sn":"xxxxxxxx",
			"attachments":[
				{
					"type": "image",
					"image": {
						"media_id": "MEDIA_ID"
					}
				}
			]
		}
	]
}
```
