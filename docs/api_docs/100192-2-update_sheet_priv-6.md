# 更新智能表格子表权限

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100192](https://developer.work.weixin.qq.com/document/path/100192)
- **文档 ID**: `100192`
- **API 名称**: `update_sheet_priv`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/content_priv/update_sheet_priv?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 5 个

## 接口描述

该接口用于设置全员权限或者成员额外权限的权限详情

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 访问令牌 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| docid | string | 是 | 智能表ID，通过新建文档接口创建后获得 |
| type | uint32 | 是 | 权限规则类型，1-全员权限，2-额外权限。每个智能表格有且只有一个全员权限 |
| rule_id | uint32 | 否 | 当type为2时必填 |
| name | string | 否 | 更新权限名称，仅当type为2时有效 |
| priv_list | object[] | 否 | 针对不同子表设置内容权限 |

### 请求示例

```json
{
	"docid": "DOCID",
	"type": 2,
	"rule_id": 2,
	"name": "NAME",
	"priv_list": [{
		"sheet_id": "SHEETID",
		"priv": 1,
		"can_insert_record": true,
		"can_delete_record": true,
		"can_create_modify_delete_view": true,
		"field_priv": {
			"field_range_type": 2,
			"field_rule_list": [{
				"field_id": "FIELDID1",
				"can_edit": true,
				"can_insert": true,
				"can_view": true
			},
			{
				"field_id": "FIELDID2",
				"can_edit": false,
				"can_insert": true,
				"can_view": true
			}]
		},
		"record_priv": {
			"record_range_type": 2,
			"record_rule_list": [{
				"field_id": "FIELDI1",
				"field_type": "FIELD_TYPE_TEXT",
				"oper_type": 1
			},
			{
				"field_id": "CREATED_USER",
				"oper_type": 1
			},
			{
				"field_id": "FIELDID2",
				"oper_type": 2,
				"field_type": "FIELD_TYPE_SELECT",
				"value": [
					"OPTION1", "OPTION2", "OPTION3"
				]
			}]
		},
		"clear": false
	}]
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
