# 删除关键词规则

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99829](https://developer.work.weixin.qq.com/document/path/99829)
- **文档 ID**: `99829`
- **API 名称**: `delete_rule`
- **请求方法**: `POST`
- **接口地址**: `delete_rule`
- **分组信息**: 第 5 个接口，共 5 个

## 接口描述

可通过此接口删除关键词规则

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| rule_id | string | 是 | 规则id |

### 请求示例

```json
{
	"rule_id":"lllllllllllllllll"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok"
}
```
