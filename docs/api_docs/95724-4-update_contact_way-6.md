# 更新企业已配置的「联系我」方式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95724](https://developer.work.weixin.qq.com/document/path/95724)
- **文档 ID**: `95724`
- **API 名称**: `update_contact_way`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/update_contact_way?access_token=ACCESS_TOKEN`
- **分组信息**: 第 4 个接口，共 6 个

## 接口描述

更新企业配置的「联系我」二维码和「联系我」小程序按钮中的信息，如使用人员和备注等。注意：已失效的临时会话联系方式无法编辑；临时会话模式仅支持单人；party或user必须在应用可见范围或客户可建联的成员范围内。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| config_id | string | 是 | 企业联系方式的配置id |
| remark | string | 否 | 联系方式的备注信息，不超过30个字符，将覆盖之前的备注 |
| skip_verify | bool | 否 | 外部客户添加时是否无需验证 |
| style | int32 | 否 | 样式，只针对“在小程序中联系”的配置生效 |
| state | string | 否 | 企业自定义state参数，用于区分不同的添加渠道 |
| user | string[] | 否 | 使用该联系方式的用户列表，将覆盖原有用户列表 |
| party | int32[] | 否 | 使用该联系方式的部门列表，将覆盖原有部门列表；仅type=2时有效 |
| expires_in | int32 | 否 | 临时会话二维码有效期（秒）；仅临时会话模式有效 |
| chat_expires_in | int32 | 否 | 临时会话有效期（秒）；仅临时会话模式有效 |
| unionid | string | 否 | 可进行临时会话的客户unionid；仅临时会话模式有效 |
| mark_source | bool | 否 | 是否标记客户添加来源为该应用创建的「联系我」，默认为true；仅对「营销获客」应用生效，且只能由创建此「联系我」的应用更新 |
| conclusions | object | 否 | 结束语；仅临时会话模式（is_temp=true）可设置 |
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
| conclusions.miniprogram.pic_media_id | string | 否 | 小程序消息封面mediaid |
| conclusions.miniprogram.appid | string | 否 | 小程序appid（必须是关联到企业的小程序应用） |
| conclusions.miniprogram.page | string | 否 | 小程序page路径 |

### 请求示例

```json
{
  "config_id":"42b34949e138eb6e027c123cba77fAAA",
  "remark":"渠道客户",
  "skip_verify":true,
  "style":1,
  "state":"teststate",
  "user" : ["zhangsan", "lisi", "wangwu"],
  "party" : [2, 3],
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
        	"page": "/path/index"
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

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok"
}
```
