# 删除商品图册

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95131](https://developer.work.weixin.qq.com/document/path/95131)
- **文档 ID**: `95131`
- **API 名称**: `delete_product_album`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/delete_product_album`
- **分组信息**: 第 5 个接口，共 5 个

## 接口描述

企业和第三方应用可以通过此接口删除商品信息

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

### 响应示例

```json
{
	"errcode":0,
	"errmsg":"ok"
}
```
