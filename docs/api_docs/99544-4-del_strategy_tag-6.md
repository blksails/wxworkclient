# 删除指定规则组下的企业客户标签

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99544](https://developer.work.weixin.qq.com/document/path/99544)
- **文档 ID**: `99544`
- **API 名称**: `del_strategy_tag`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_strategy_tag?access_token=ACCESS_TOKEN`
- **分组信息**: 第 4 个接口，共 4 个

## 接口描述

企业可通过此接口删除某个规则组下的标签，或删除整个标签组。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| tag_id | array | 否 | 标签的id列表 |
| group_id | array | 否 | 标签组的id列表 |

### 请求示例

```json
{
	"tag_id": [
		"TAG_ID_1",
		"TAG_ID_2"
	],
	"group_id": [
		"GROUP_ID_1",
		"GROUP_ID_2"
	],
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
