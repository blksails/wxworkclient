# 获取群发记录列表

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/93439](https://developer.work.weixin.qq.com/document/path/93439)
- **文档 ID**: `93439`
- **API 名称**: `get_groupmsg_list_v2`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_groupmsg_list_v2`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

企业和第三方应用可通过此接口获取企业与成员的群发记录。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| chat_type | string | 是 | 群发任务的类型，默认为single，表示发送给客户，group表示发送给客户群 |
| start_time | int32 | 是 | 群发任务记录开始时间 |
| end_time | int32 | 是 | 群发任务记录结束时间 |
| creator | string | 否 | 群发任务创建人企业账号id |
| filter_type | int32 | 否 | 创建人类型。0：企业发表 1：个人发表 2：所有，包括个人创建以及企业创建，默认情况下为所有类型 |
| limit | int32 | 否 | 返回的最大记录数，整型，最大值100，默认值50，超过最大值时取默认值 |
| cursor | string | 否 | 用于分页查询的游标，字符串类型，由上一次调用返回，首次调用可不填 |

### 请求示例

```json
{
   "chat_type":"single",
   "start_time":1605171726,
   "end_time":1605172726,
   "creator":"zhangshan",
   "filter_type":1,
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
| next_cursor | string | 分页游标，再下次请求时填写以获取之后分页的记录，如果已经没有更多的数据则返回空 |
| group_msg_list | object[] | 群发记录列表 |

### 响应示例

```json
{
	"errcode":0,
	"errmsg":"ok",
	"next_cursor":"CURSOR",
	"group_msg_list":[
		{
			"msgid":"msgGCAAAXtWyujaWJHDDGi0mAAAA",
			"creator":"xxxx",
			"create_time":"xxxx",
			"create_type":1,
			"text": {
				"content":"文本消息内容"
			},
			"attachments": [
				{
					"msgtype": "image",
					"image": {
						"media_id": "MEDIA_ID",
						"pic_url": "http://p.qpic.cn/pic_wework/3474110808/7a6344sdadfwehe42060/0"
					}
				},
				...
			]
		}
	]
}
```

## 其他说明

### 补充说明

群发任务记录的起止时间间隔不能超过1个月
3.1.6版本之前不支持多附件，请参考获取群发记录列表接口获取群发记录列表

### 权限说明

企业需要使用配置到“可调用应用”列表中的自建应用secret所获取的accesstoken来调用（accesstoken如何获取？）。
自建应用调用，只会返回应用可见范围内用户的发送情况。
第三方应用调用需要企业授权客户联系下群发消息给客户和客户群的权限
