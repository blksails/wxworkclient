# 获取规则组管理范围

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99540](https://developer.work.weixin.qq.com/document/path/99540)
- **文档 ID**: `99540`
- **API 名称**: `customer_strategy_get_range`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/customer_strategy/get_range`
- **分组信息**: 第 3 个接口，共 6 个

## 接口描述

企业可通过此接口获取某个客户规则组管理的成员和部门列表

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| strategy_id | uint32 | 是 | 规则组id |
| cursor | string | 否 | 分页游标 |
| limit | uint32 | 否 | 每个分页的成员/部门节点数，默认为1000，最大为1000 |

### 请求示例

```json
{
	"strategy_id": 1,
	"cursor":"CURSOR",
	"limit":1000
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| range | object[] | 管理范围节点列表 |
| range.type | uint32 | 节点类型，1-成员 2-部门 |
| range.userid | string | 管理范围内配置的成员userid，仅`type`为1时返回 |
| range.partyid | uint32 | 管理范围内配置的部门partyid，仅`type`为2时返回 |
| next_cursor | string | 分页游标，用于查询下一个分页的数据，无更多数据时不返回 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
	"range":
	[
		{
			"type":1,
			"userid":"zhangsan"
		},
		{
			"type":2,
			"partyid":1
		}
	],
	"next_cursor":"NEXT_CURSOR"
}
```
