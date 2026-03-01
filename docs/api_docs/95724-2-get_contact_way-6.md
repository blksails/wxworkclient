# 获取企业已配置的「联系我」方式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95724](https://developer.work.weixin.qq.com/document/path/95724)
- **文档 ID**: `95724`
- **API 名称**: `get_contact_way`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_contact_way?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 6 个

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
| contact_way | object | 联系我配置详情 |
| contact_way.config_id | string | 联系方式的配置id |
| contact_way.type | int32 | 联系方式类型，1-单人，2-多人 |
| contact_way.scene | int32 | 场景，1-在小程序中联系，2-通过二维码联系 |
| contact_way.style | int32 | 小程序中联系按钮的样式，仅在scene=1时返回 |
| contact_way.remark | string | 联系方式的备注信息，用于助记 |
| contact_way.skip_verify | bool | 外部客户添加时是否无需验证 |
| contact_way.state | string | 企业自定义state参数，用于区分不同的添加渠道 |
| contact_way.qr_code | string | 联系二维码的URL，仅在scene=2时返回 |
| contact_way.user | string[] | 使用该联系方式的用户userID列表 |
| contact_way.party | int32[] | 使用该联系方式的部门id列表 |
| contact_way.is_temp | bool | 是否临时会话模式，默认为false |
| contact_way.expires_in | int32 | 临时会话二维码有效期（秒） |
| contact_way.chat_expires_in | int32 | 临时会话有效期（秒） |
| contact_way.unionid | string | 可进行临时会话的客户unionid |
| contact_way.mark_source | bool | 是否标记客户添加来源为该应用创建的「联系我」；仅对「营销获客」应用生效 |
| contact_way.conclusions | object | 结束语 |
| contact_way.conclusions.text | object | 文本结束语 |
| contact_way.conclusions.text.content | string | 消息文本内容 |
| contact_way.conclusions.image | object | 图片结束语 |
| contact_way.conclusions.image.pic_url | string | 图片url（获取联系我方式时返回） |
| contact_way.conclusions.link | object | 图文结束语 |
| contact_way.conclusions.link.title | string | 图文消息标题 |
| contact_way.conclusions.link.picurl | string | 图文消息封面的url |
| contact_way.conclusions.link.desc | string | 图文消息的描述 |
| contact_way.conclusions.link.url | string | 图文消息的链接 |
| contact_way.conclusions.miniprogram | object | 小程序结束语 |
| contact_way.conclusions.miniprogram.title | string | 小程序消息标题 |
| contact_way.conclusions.miniprogram.pic_media_id | string | 小程序消息封面mediaid |
| contact_way.conclusions.miniprogram.appid | string | 小程序appid |
| contact_way.conclusions.miniprogram.page | string | 小程序page路径 |

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
