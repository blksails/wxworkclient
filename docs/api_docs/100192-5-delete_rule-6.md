# 删除智能表格指定成员额外权限

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100192](https://developer.work.weixin.qq.com/document/path/100192)
- **文档 ID**: `100192`
- **API 名称**: `delete_rule`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/content_priv/delete_rule?access_token=ACCESS_TOKEN`
- **分组信息**: 第 5 个接口，共 5 个

## 接口描述

该接口用于删除智能表格指定成员额外权限

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 访问令牌 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| docid | string | 是 | 智能表ID，通过新建文档接口创建后获得 |
| rule_id_list | uint32[] | 是 | 需要删除的规则id列表 |

### 请求示例

```json
{
	"docid": "DOCID",
	"rule_id_list": [
		2
	]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok"
}
```
