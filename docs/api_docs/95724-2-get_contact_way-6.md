# 获取企业已配置的「联系我」方式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95724](https://developer.work.weixin.qq.com/document/path/95724)
- **文档 ID**: `95724`
- **API 名称**: `get_contact_way`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_contact_way?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 4 个

## 接口描述

获取企业配置的「联系我」二维码和「联系我」小程序按钮。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| config_id | string | 是 | 联系方式的配置id |

### 请求示例

```json
{
   "config_id":"42b34949e138eb6e027c123cba77fad7"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| contact_way | object | 联系方式信息 |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok",
   "contact_way":
    {
        "config_id":"42b34949e138eb6e027c123cba77fAAA",
        "type":1,
        "scene":1,
        "style":2,
		"remark":"test remark",
		"skip_verify":true,
		"state":"teststate",
		"qr_code":"https://p.qpic.cn/wwhead/duc2TvpEgSdicZ9RrdUtBkv2UiaA/0",
		"user" : ["zhangsan", "lisi", "wangwu"],
        "party" : [2, 3],
		"is_temp":true,
		"expires_in":86400,
        "chat_expires_in":86400,
		"unionid":"oxTWIuGaIt6gTKsQRLau2M0AAAA",
		"mark_source":true,
		"conclusions":
		{
    		"text":
		{
			"content":"文本消息内容"
		},
    		"image":
		{
         	"pic_url": "https://p.qpic.cn/pic_wework/XXXXX"
     	},
    		"link":
		{
         	"title": "消息标题",
         	"picurl": "https://example.pic.com/path",
         	"desc": "消息描述",
         	"url": "https://example.link.com/path"
     	},
     	"miniprogram":
		{
         	"title": "消息标题",
			"pic_media_id": "MEDIA_ID",
         	"appid": "wx8bd80126147dfAAA",
         	"page": "/path/index"
     	}
    }
    }
}
```
