# 配置客户联系「联系我」方式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95724](https://developer.work.weixin.qq.com/document/path/95724)
- **文档 ID**: `95724`
- **API 名称**: `add_contact_way`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_contact_way?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 4 个

## 接口描述

企业可以通过此接口为具有客户联系功能的成员生成专属的「联系我」二维码或者「联系我」按钮。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| type | int32 | 是 | 联系方式类型,1-单人, 2-多人 |
| scene | int32 | 是 | 场景，1-在小程序中联系，2-通过二维码联系 |
| style | int32 | 否 | 在小程序中联系时使用的控件样式 |
| remark | string | 否 | 联系方式的备注信息，用于助记，不超过30个字符 |
| skip_verify | bool | 否 | 外部客户添加时是否无需验证，默认为true |
| state | string | 否 | 企业自定义的state参数，用于区分不同的添加渠道，在调用“获取客户详情”时会返回该参数值，不超过30个字符 |
| user | string[] | 否 | 使用该联系方式的用户userID列表，在type为1时为必填，且只能有一个 |
| party | int32[] | 否 | 使用该联系方式的部门id列表，只在type为2时有效 |
| is_temp | bool | 否 | 是否临时会话模式，true表示使用临时会话模式，默认为false |
| expires_in | int32 | 否 | 临时会话二维码有效期，以秒为单位。该参数仅在is_temp为true时有效，默认7天，最多为14天 |
| chat_expires_in | int32 | 否 | 临时会话有效期，以秒为单位。该参数仅在is_temp为true时有效，默认为添加好友后24小时，最多为14天 |
| unionid | string | 否 | 可进行临时会话的客户unionid，该参数仅在is_temp为true时有效，如不指定则不进行限制 |
| is_exclusive | bool | 否 | 是否开启同一外部企业客户只能添加同一个员工，默认为否，开启后，同一个企业的客户会优先添加到同一个跟进人 |
| mark_source | bool | 否 | 是否标记客户添加来源为该应用创建的「联系我」, 默认为true; 仅对「营销获客」应用生效 |
| conclusions | object | 否 | 结束语定义 |

### 请求示例

```json
{
   "type" :1,
   "scene":1,
   "style":1,
   "remark":"渠道客户",
   "skip_verify":true,
   "state":"teststate",
   "user" : ["zhangsan", "lisi", "wangwu"],
   "party" : [2, 3],
   "is_temp":true,
   "expires_in":86400,
   "chat_expires_in":86400,
   "unionid":"oxTWIuGaIt6gTKsQRLau2M0AAAA",
   "is_exclusive":true,
   "mark_source":true,
   "conclusions":
   {
		"text":
		{
			"content":"文本消息内容"
		},
     	"image":
		{
         	"media_id": "MEDIA_ID"
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
         	"page": "/path/index.html"
     	}
   }
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| config_id | string | 新增联系方式的配置id |
| qr_code | string | 联系我二维码链接，仅在scene为2时返回 |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok",
   "config_id":"42b34949e138eb6e027c123cba77fAAA",
   "qr_code":"https://p.qpic.cn/wwhead/duc2TvpEgSdicZ9RrdUtBkv2UiaA/0"
}
```
