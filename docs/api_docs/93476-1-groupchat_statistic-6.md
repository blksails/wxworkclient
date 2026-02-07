# 按群主聚合的方式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/93476](https://developer.work.weixin.qq.com/document/path/93476)
- **文档 ID**: `93476`
- **API 名称**: `groupchat_statistic`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/groupchat/statistic?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

获取指定日期的统计数据。注意，企业微信仅存储180天的数据。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| day_begin_time | uint32 | 是 | 起始日期的时间戳，填当天的0时0分0秒。取值范围：昨天至前180天。 |
| day_end_time | uint32 | 否 | 结束日期的时间戳，填当天的0时0分0秒。取值范围：昨天至前180天。 如果不填，默认同 day_begin_time（即默认取一天的数据） |
| owner_filter.userid_list | string[] | 是 | 群主ID列表。最多100个 |
| order_by | uint32 | 否 | 排序方式。 1 - 新增群的数量 2 - 群总数 3 - 新增群人数 4 - 群总人数  默认为1 |
| order_asc | uint32 | 否 | 是否升序。0-否；1-是。默认降序 |
| offset | uint32 | 否 | 分页，偏移量, 默认为0 |
| limit | uint32 | 否 | 分页，预期请求的数据量，默认为500，取值范围 1 ~ 1000 |

### 请求示例

```json
{
	"day_begin_time": 1600272000,
	"day_end_time": 1600444800,
	"owner_filter": {
		"userid_list": ["zhangsan"]
	},
	"order_by": 2,
	"order_asc": 0,
	"offset" : 0,
	"limit" : 1000
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| total | int32 | 命中过滤条件的记录总个数 |
| next_offset | int32 | 当前分页的下一个offset。当next_offset和total相等时，说明已经取完所有 |
| items | object[] | 记录列表。表示某个群主所拥有的客户群的统计数据 |
| items.owner | string | 群主ID |
| items.data | object | 详情 |
| items.data.new_chat_cnt | int32 | 新增客户群数量 |
| items.data.chat_total | int32 | 截至当天客户群总数量 |
| items.data.chat_has_msg | int32 | 截至当天有发过消息的客户群数量 |
| items.data.new_member_cnt | int32 | 客户群新增群人数 |
| items.data.member_total | int32 | 截至当天客户群总人数 |
| items.data.member_has_msg | int32 | 截至当天有发过消息的群成员数 |
| items.data.msg_total | int32 | 截至当天客户群消息总数 |
| items.data.migrate_trainee_chat_cnt | int32 | 截至当天新增迁移群数(仅教培行业返回) |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"total": 2,
	"next_offset": 2,
	"items": [{
			"owner": "zhangsan",
			"data": {
				"new_chat_cnt": 2,
				"chat_total": 2,
				"chat_has_msg": 0,
				"new_member_cnt": 0,
				"member_total": 6,
				"member_has_msg": 0,
				"msg_total": 0,
				"migrate_trainee_chat_cnt": 3
			}
		},
		{
			"owner": "lisi",
			"data": {
				"new_chat_cnt": 1,
				"chat_total": 3,
				"chat_has_msg": 2,
				"new_member_cnt": 0,
				"member_total": 6,
				"member_has_msg": 0,
				"msg_total": 0,
				"migrate_trainee_chat_cnt": 3
			}
		}
	]
}
```
