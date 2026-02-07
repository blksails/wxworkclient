# 编辑规则组及其管理范围

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99540](https://developer.work.weixin.qq.com/document/path/99540)
- **文档 ID**: `99540`
- **API 名称**: `customer_strategy_edit`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/customer_strategy/edit`
- **分组信息**: 第 5 个接口，共 6 个

## 接口描述

企业可通过此接口编辑规则组的基本信息和修改客户规则组管理范围。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| strategy_id | uint32 | 是 | 规则组id |
| strategy_name | string | 否 | 规则组名称 |
| admin_list | string[] | 否 | 管理员列表 |
| privilege | object | 否 | 权限配置 |
| range_add | object[] | 否 | 向管理范围添加的节点列表 |
| range_del | object[] | 否 | 从管理范围删除的节点列表 |

### 请求示例

```json
{
	"strategy_id":1,
	"strategy_name": "NAME",
	"admin_list":[
		"zhangsan",
		"lisi"
	],
	"privilege": { ... },
	"range_add": [ ... ],
	"range_del": [ ... ]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok"
}
```
