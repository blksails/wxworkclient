# 创建新的规则组

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99540](https://developer.work.weixin.qq.com/document/path/99540)
- **文档 ID**: `99540`
- **API 名称**: `customer_strategy_create`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/customer_strategy/create`
- **分组信息**: 第 4 个接口，共 6 个

## 接口描述

企业可通过此接口创建一个新的客户规则组。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| parent_id | uint32 | 否 | 父规则组id |
| strategy_name | string | 是 | 规则组名称 |
| admin_list | string[] | 是 | 规则组管理员userid列表，不可配置超级管理员，每个规则组最多可配置20个负责人 |
| privilege | object | 否 | 权限配置 |
| range | object[] | 否 | 管理范围节点列表 |

### 请求示例

```json
{
	"parent_id":0,
	"strategy_name": "NAME",
	"admin_list":[
		"zhangsan",
		"lisi"
	],
	"privilege": { ... },
	"range": [ ... ]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| strategy_id | uint32 | 规则组id |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
	"strategy_id":1
}
```
