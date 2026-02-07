# 获取规则组列表

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99540](https://developer.work.weixin.qq.com/document/path/99540)
- **文档 ID**: `99540`
- **API 名称**: `customer_strategy_list`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/customer_strategy/list`
- **分组信息**: 第 1 个接口，共 6 个

## 接口描述

企业可通过此接口获取企业配置的所有客户规则组id列表。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| cursor | string | 否 | 分页查询游标，首次调用可不填 |
| limit | uint32 | 否 | 分页大小,默认为1000，最大不超过1000 |

### 请求示例

```json
{
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
| strategy | object[] | 规则组id列表 |
| strategy[].strategy_id | uint32 | 规则组id |
| next_cursor | string | 分页游标，用于查询下一个分页的数据，无更多数据时不返回 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"strategy":
	[
		{
			"strategy_id":1
		},
		{
			"strategy_id":2
		}
	],
	"next_cursor":"NEXT_CURSOR"
}
```
