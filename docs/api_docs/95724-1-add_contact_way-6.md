# 配置客户联系「联系我」方式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95724](https://developer.work.weixin.qq.com/document/path/95724)
- **文档 ID**: `95724`
- **API 名称**: `add_contact_way`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_contact_way?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 6 个

## 接口描述

企业可通过此接口为具有客户联系功能的成员生成专属的「联系我」二维码或「联系我」按钮（小程序）。注意：通过API添加的「联系我」不会在管理端展示；每企业最多配置50万个；需妥善存储返回的config_id（丢失可能导致无法编辑/删除）。临时会话模式不占用数量但每日最多10万个，仅支持单人，且添加好友完成后二维码即刻失效。每个联系方式最多配置100个使用成员（含部门展开成员）。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| type | int32 | 是 | 联系方式类型, 1-单人, 2-多人 |
| scene | int32 | 是 | 场景，1-在小程序中联系，2-通过二维码联系 |
| style | int32 | 否 | 在小程序中联系时使用的控件样式（仅scene=1时生效），详见附录 |
| remark | string | 否 | 联系方式的备注信息，用于助记，不超过30个字符 |
| skip_verify | bool | 否 | 外部客户添加时是否无需验证，默认为true |
| state | string | 否 | 企业自定义state参数，用于区分不同渠道（获取客户详情时会返回），不超过30个字符 |
| user | string[] | 否 | 使用该联系方式的用户userID列表；type=1时必填且只能有一个 |
| party | int32[] | 否 | 使用该联系方式的部门id列表；仅type=2时有效 |
| is_temp | bool | 否 | 是否临时会话模式，true表示使用临时会话模式，默认为false |
| expires_in | int32 | 否 | 临时会话二维码有效期（秒）；仅is_temp=true时有效；默认7天，最多14天 |
| chat_expires_in | int32 | 否 | 临时会话有效期（秒）；仅is_temp=true时有效；默认添加好友后24小时，最多14天 |
| unionid | string | 否 | 可进行临时会话的客户unionid；仅is_temp=true时有效；不指定则不限制 |
| is_exclusive | bool | 否 | 是否开启同一外部企业客户只能添加同一个员工，默认为否；开启后同企业客户会优先添加到同一跟进人 |
| mark_source | bool | 否 | 是否标记客户添加来源为该应用创建的「联系我」，默认为true；仅对「营销获客」应用生效 |
| conclusions | object | 否 | 结束语：会话结束时自动发送给客户；仅is_temp=true时有效 |
| conclusions.text | object | 否 | 文本结束语 |
| conclusions.text.content | string | 否 | 消息文本内容（最长4000字节） |
| conclusions.image | object | 否 | 图片结束语（构造结束语时只能填写media_id） |
| conclusions.image.media_id | string | 否 | 图片的media_id |
| conclusions.link | object | 否 | 图文结束语 |
| conclusions.link.title | string | 否 | 图文消息标题（最长128字节） |
| conclusions.link.picurl | string | 否 | 图文消息封面url |
| conclusions.link.desc | string | 否 | 图文消息描述（最长512字节） |
| conclusions.link.url | string | 否 | 图文消息链接 |
| conclusions.miniprogram | object | 否 | 小程序结束语 |
| conclusions.miniprogram.title | string | 否 | 小程序消息标题（最长64字节） |
| conclusions.miniprogram.pic_media_id | string | 否 | 小程序消息封面mediaid（建议尺寸520*416） |
| conclusions.miniprogram.appid | string | 否 | 小程序appid（必须是关联到企业的小程序应用） |
| conclusions.miniprogram.page | string | 否 | 小程序page路径 |

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

## 其他说明

### 权限说明

调用接口的应用需满足权限要求：自建应用需配置到「客户联系 可调用接口的应用」中；代开发/第三方应用需具备「配置「联系我」二维码」权限（第三方应用在营销获客应用且客户建联方式配置为「联系我」二维码）。传入成员和部门需在应用可见范围内；使用成员需已激活、实名认证并配置客户联系功能。临时会话二维码有有效期，仅支持医疗行业企业创建，可配置会话结束自动发送结束语。

### 结束语规则（摘要）

text、image、link、miniprogram四者不能同时为空；text可与另外三者同时发送（两条消息触达）；image/link/miniprogram三者只能有一个，若同时填按image>link>miniprogram优先；media_id可通过素材管理接口获取；构造结束语的image仅填media_id，获取含image结构时返回pic_url。
