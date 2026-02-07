# 查询智能表格子表权限

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100192](https://developer.work.weixin.qq.com/document/path/100192)
- **文档 ID**: `100192`
- **API 名称**: `get_sheet_priv`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/content_priv/get_sheet_priv?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 5 个

## 接口描述

该接口用于查询智能表格子表权限详情

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 访问令牌 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| docid | string | 是 | 智能表ID，通过新建文档接口创建后获得 |
| type | uint32 | 是 | 权限规则类型，1-全员权限，2-额外权限 |
| rule_id_list | uint32[] | 否 | 需要查询的规则id列表，查询额外权限时填写 |

### 请求示例

```json
{
	"docid": "DOCID",
	"type": 2,
	"rule_id_list": [
		"RULEID1", "RULEID2"
	]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| rule_list | object[] | 权限列表 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"rule_list": [{
		"rule_id": 1,
		"type": 1,
		"name": "全员权限",
		"priv_list": [{
			"sheet_id": "q979lj",
			"priv": 2,
			"can_insert_record": true,
			"can_delete_record": true,
			"record_priv": {
				"record_range_type": 1
			},
			"field_priv": {
				"field_range_type": 2,
				"field_rule_list": [{
					"field_id": "fsMGQS",
					"field_type": "FIELD_TYPE_TEXT",
					"can_edit": false,
					"can_insert": true,
					"can_view": true
				}],
				"field_default_rule": {
					"can_edit": false,
					"can_insert": false,
					"can_view": true
				}
			},
			"can_create_modify_delete_view": true
		},
		{
			"sheet_id": "kQ65QQ",
			"priv": 1
		}]
	}]
}
```
