# 通讯录批量搜索

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/91844](https://developer.work.weixin.qq.com/document/path/91844)
- **文档 ID**: `91844`
- **API 名称**: `batchsearch`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/service/contact/batchsearch?provider_access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

通讯录批量搜索接口用于批量查询企业通讯录中的用户或部门信息。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用提供商的provider_access_token |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| auth_corpid | string | 是 | 查询的企业corpid |
| agentid | int32 | 否 | 应用id，若非0则只返回应用可见范围内的用户或部门信息 |
| query_request_list | object[] | 是 | 搜索请求列表，每次搜索列表数量不超过50 |

### 请求示例

```json
{
	"auth_corpid":"wwxxxxxx",
	"agentid": 1000046,
    "query_request_list":[
		{
			"query_word": "zhangsan",
			"query_type":1,
			"query_range":1,
			"limit":50,
			"full_match_field":1,
			"cursor":"CURSOR"
		}
	]
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
