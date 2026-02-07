# 获取规则组详情

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99540](https://developer.work.weixin.qq.com/document/path/99540)
- **文档 ID**: `99540`
- **API 名称**: `customer_strategy_get`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/customer_strategy/get`
- **分组信息**: 第 2 个接口，共 6 个

## 接口描述

企业可以通过此接口获取某个客户规则组的详细信息。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| strategy_id | uint32 | 是 | 规则组id |

### 请求示例

```json
{
	"strategy_id":1
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| strategy.strategy_id | uint32 | 规则组id |
| strategy.parent_id | uint32 | 父规则组id， 如果当前规则组没父规则组，则为0 |
| strategy.strategy_name | string | 规则组名称 |
| strategy.create_time | uint32 | 规则组创建时间戳 |
| strategy.admin_list | string[] | 规则组管理员userid列表 |
| strategy.privilege | object | 权限配置 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"strategy": {
		"strategy_id":1,
		"parent_id":0,
		"strategy_name": "NAME",
		"create_time": 1557838797,
		"admin_list":[
			"zhangsan",
			"lisi"
		],
		"privilege": { ... }
	}
}
```
