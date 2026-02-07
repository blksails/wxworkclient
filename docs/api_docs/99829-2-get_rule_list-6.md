# 获取关键词列表

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99829](https://developer.work.weixin.qq.com/document/path/99829)
- **文档 ID**: `99829`
- **API 名称**: `get_rule_list`
- **请求方法**: `POST`
- **接口地址**: `get_rule_list`
- **分组信息**: 第 2 个接口，共 5 个

## 接口描述

通过此接口获取客户企业下的关键词规则列表

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| cursor | string | 否 | 由企业微信后台返回，第一次调用可不填 |
| limit | int32 | 否 | 指定获取的数量上限，不填默认100 |

### 请求示例

```json
{
	"cursor":"XMGIENJGJ",
	"limit":100
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
| rule_list | object[] | 规则列表 |
| has_more | bool | 是否还有更多数据 |
| next_cursor | string | 下次调用时将该字段填入cursor中 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"rule_list": [{
		"rule_id": "xxxxxxxxx",
		"name": "已回复",
		"create_time": 16666666666
	}],
	"has_more":false,
	"next_cursor":"JIUENGMG"
}
```
