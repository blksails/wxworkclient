# 编辑商品图册

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95131](https://developer.work.weixin.qq.com/document/path/95131)
- **文档 ID**: `95131`
- **API 名称**: `update_product_album`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/update_product_album`
- **分组信息**: 第 4 个接口，共 5 个

## 接口描述

企业和第三方应用可以通过此接口修改商品信息

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| product_id | string | 是 | 商品id |
| description | string | 是 | 商品的名称、特色等;不超过300个字 |
| price | uint32 | 是 | 商品的价格，单位为分；最大不超过5万元 |
| product_sn | string | 否 | 商品编码；不超过128个字节；只能输入数字和字母 |
| attachments | object[] | 否 | 附件类型，仅支持image |
| attachments[].type | string | 是 | 附件类型，仅支持image |
| attachments[].image.media_id | string | 否 | 图片的media_id，仅支持通过上传附件资源接口的资源 |

### 请求示例

```json
{
	"product_id" : "xxxxxxxxxx",
	"description":"世界上最好的商品",
	"price":30000,
	"product_sn":"xxxxxx",
	"attachments":[
		{
			"type": "image",
			"image": {
				"media_id": "MEDIA_ID"
			}
		}
	]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |

### 响应示例

```json
{
	"errcode":0,
	"errmsg":"ok"
}
```
