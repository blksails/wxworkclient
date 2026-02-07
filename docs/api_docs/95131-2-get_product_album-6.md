# 获取商品图册

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95131](https://developer.work.weixin.qq.com/document/path/95131)
- **文档 ID**: `95131`
- **API 名称**: `get_product_album`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_product_album`
- **分组信息**: 第 2 个接口，共 5 个

## 接口描述

企业和第三方应用可以通过此接口获取商品信息

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| product_id | string | 是 | 商品id |

### 请求示例

```json
{
	"product_id" : "xxxxxxxxxx"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| product | object | 商品详情 |
| product.product_id | string | 商品id |
| product.product_sn | string | 商品编码 |
| product.description | string | 商品的名称、特色等 |
| product.price | uint32 | 商品的价格，单位为分 |
| product.create_time | uint32 | 商品图册创建时间 |
| product.attachments | object[] | 附件类型 |
| product.attachments.type | string | 附件类型，目前仅支持image |
| product.attachments.image.media_id | string | 图片的media_id，可以通过获取临时素材下载资源 |

### 响应示例

```json
{
	"errcode":0,
	"errmsg":"ok",
	"product": {
			"product_id" : "xxxxxxxxxx",
			"description":"世界上最好的商品",
			"price":30000,
			"create_time":1600000000,
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
}
```
