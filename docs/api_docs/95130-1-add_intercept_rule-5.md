# 新建敏感词规则

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95130](https://developer.work.weixin.qq.com/document/path/95130)
- **文档 ID**: `95130`
- **API 名称**: `add_intercept_rule`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_intercept_rule`
- **分组信息**: 第 1 个接口，共 5 个

## 接口描述

企业和第三方应用可以通过此接口新建敏感词规则

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| rule_name | string | 是 | 规则名称，长度1~20个utf8字符 |
| word_list | array | 是 | 敏感词列表，敏感词长度1~32个utf8字符，列表大小不能超过300个 |
| semantics_list | array | 否 | 额外的拦截语义规则，1：手机号、2：邮箱地址、3：红包 |
| intercept_type | int32 | 是 | 拦截方式，1:警告并拦截发送；2:仅发警告 |
| applicable_range.user_list | array | 是 | 可使用的userid列表。必须为应用可见范围内的成员；最多支持传1000个节点 |
| applicable_range.department_list | array | 是 | 可使用的部门列表，必须为应用可见范围内的部门；最多支持传1000个节点 |

### 请求示例

```json
{
	"rule_name":"rulename",
	"word_list":[
	  "敏感词1","敏感词2"
	],
	"semantics_list":[1,2,3],
	"intercept_type":1,
	"applicable_range":{
		"user_list":["zhangshan"],
		"department_list":[2,3]
	}
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| rule_id | string | 规则id |
