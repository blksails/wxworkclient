# 添加企业客户标签

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96320](https://developer.work.weixin.qq.com/document/path/96320)
- **文档 ID**: `96320`
- **API 名称**: `add_corp_tag`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_corp_tag`
- **分组信息**: 第 2 个接口，共 4 个

## 接口描述

企业可通过此接口向客户标签库中添加新的标签组和标签，每个企业最多可配置10000个企业标签。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| group_id | string | 否 | 标签组id |
| group_name | string | 否 | 标签组名称，最长为30个字符 |
| order | uint32 | 否 | 标签组次序值 |
| tag.name | string | 是 | 添加的标签名称，最长为30个字符 |
| tag.order | uint32 | 否 | 标签次序值 |
| agentid | uint32 | 否 | 授权方安装的应用agentid。仅旧的第三方多应用套件需要填此参数 |

### 请求示例

```json
{
	"group_id": "GROUP_ID",
	"group_name": "GROUP_NAME",
	"order": 1,
	"tag": [{
		"name": "TAG_NAME_1",
		"order": 1
	},
	{
		"name": "TAG_NAME_2",
		"order": 2
	}],
	 "agentid" : 1000014
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| tag_group | object | 标签组信息 |
| tag_group.group_id | string | 标签组id |
| tag_group.group_name | string | 标签组名称 |
| tag_group.create_time | uint32 | 标签组创建时间 |
| tag_group.order | uint32 | 标签组次序值 |
| tag_group.tag | object[] | 标签组内的标签列表 |
| tag_group.tag.id | string | 新建标签id |
| tag_group.tag.name | string | 新建标签名称 |
| tag_group.tag.create_time | uint32 | 标签创建时间 |
| tag_group.tag.order | uint32 | 标签次序值 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"tag_group": {
		"group_id": "TAG_GROUPID1",
		"group_name": "GOURP_NAME",
		"create_time": 1557838797,
		"order": 1,
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
		}]
	}
}
```
