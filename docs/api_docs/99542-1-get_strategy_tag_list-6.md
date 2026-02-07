# 获取指定规则组下的企业客户标签

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99542](https://developer.work.weixin.qq.com/document/path/99542)
- **文档 ID**: `99542`
- **API 名称**: `get_strategy_tag_list`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_strategy_tag_list?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 4 个

## 接口描述

企业可通过此接口获取某个规则组内的企业客户标签详情。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| strategy_id | int32 | 否 | 规则组id |
| tag_id | array | 否 | 要查询的标签id |
| group_id | array | 否 | 要查询的标签组id，返回该标签组以及其下的所有标签信息 |

### 请求示例

```json
{
	"strategy_id":1,
	"tag_id":[
		"etXXXXXXXXXX",
		"etYYYYYYYYYY"
	],
	"group_id":[
		"etZZZZZZZZZZZZZ",
		"etYYYYYYYYYYYYY"
	]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| tag_group | object[] | 标签组列表 |
| tag_group[].group_id | string | 标签组id |
| tag_group[].group_name | string | 标签组名称 |
| tag_group[].create_time | uint32 | 标签组创建时间 |
| tag_group[].order | uint32 | 标签组排序的次序值 |
| tag_group[].strategy_id | int32 | 标签组所属的规则组id |
| tag_group[].tag | object[] | 标签组内的标签列表 |
| tag_group[].tag[].id | string | 标签id |
| tag_group[].tag[].name | string | 标签名称 |
| tag_group[].tag[].create_time | uint32 | 标签创建时间 |
| tag_group[].tag[].order | uint32 | 标签排序的次序值 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"tag_group": [{
		"group_id": "TAG_GROUPID1",
		"group_name": "GOURP_NAME",
		"create_time": 1557838797,
		"order": 1,
		"strategy_id":1,
		"tag": [{
				"id": "TAG_ID1",
				"name": "NAME1",
				"create_time": 1557838797,
				"order": 1
			},
			{
				"id": "TAG_ID2",
				"name": "NAME2",
				"create_time": 1557838797,
				"order": 2
			}
		]
	}]
}
```
