# 创建发表任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95095](https://developer.work.weixin.qq.com/document/path/95095)
- **文档 ID**: `95095`
- **API 名称**: `add_moment_task`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_moment_task`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

企业和第三方应用可通过该接口创建客户朋友圈的发表任务。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| visible_range | object | 否 | 指定的发表范围；若未指定，则表示执行者为应用可见范围内所有成员 |
| sender_list | object | 否 | 发表任务的执行者列表，详见下文的“可见范围说明” |
| sender_list.user_list | array | 否 | 发表任务的执行者用户列表，最多支持10万个 |
| sender_list.department_list | array | 否 | 发表任务的执行者部门列表 |
| external_contact_list | object | 否 | 可见到该朋友圈的客户列表，详见下文的“可见范围说明” |
| external_contact_list.tag_list | array | 否 | 可见到该朋友圈的客户标签列表。注：这里仅支持企业客户标签，不支持规则组标签 |
| text | object | 否 | 文本消息 |
| text.content | string | 否 | 消息文本内容，不能与附件同时为空，最多支持传入2000个字（4000个字节），若超出长度报错'invalid text size' |
| attachments | array | 否 | 附件，不能与text.content同时为空，最多支持9个图片类型，或者1个视频，或者1个链接。类型只能三选一，若传了不同类型，报错'invalid attachments msgtype' |
| attachments.msgtype | string | 是 | 附件类型，可选image、link或者video |
| attachments.image | object | 否 | 图片消息附件。最多支持传入9个；超过9个报错'invalid attachments size' |
| attachments.image.media_id | string | 是 | 图片的素材id，长边不超过10800像素，短边不超过1080像素。可通过上传附件资源接口获得 |
| attachments.link | object | 否 | 图文消息附件。只支持1个；若超过1个报错'invalid attachments size' |
| attachments.link.title | string | 否 | 图文消息标题，最多64个字(128个字节) |
| attachments.link.url | string | 是 | 图文消息链接 |
| attachments.link.media_id | string | 是 | 图片链接封面，长边不超过10800像素，短边不超过1080像素，可通过上传附件资源接口获得 |
| attachments.video | object | 否 | 视频消息附件。最长不超过30S，最大不超过10MB。只支持1个；若超过1个报错'invalid attachments size' |
| attachments.video.media_id | string | 是 | 视频的素材id，未填写报错'invalid msg'。可通过上传附件资源接口获得 |

### 请求示例

```json
{
	"text": {
		"content": "文本消息内容"
	},
	"attachments": [
		{
			"msgtype": "image",
			"image": {
				"media_id": "MEDIA_ID"
			}
		},
		{
			"msgtype": "video",
			"video": {
				"media_id": "MEDIA_ID"
			}
		},
		{
			"msgtype": "link",
			"link": {
				"title": "消息标题",
				"url": "https://example.link.com/path",
				"media_id": "MEDIA_ID"
			}
		}
	],
 	"visible_range":{
		"sender_list":{
			"user_list":["zhangshan","lisi"],
			"department_list":[2,3]
		},
		"external_contact_list":{
			"tag_list":[ "etXXXXXXXXXX", "etYYYYYYYYYY"]
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
| jobid | string | 异步任务id，最大长度为64字节，24小时有效；可使用获取发表朋友圈任务结果接口查询任务状态 |

### 响应示例

```json
{
	"errcode":0,
	"errmsg":"ok",
	"jobid":"xxxx"
}
```
