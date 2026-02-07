# 修改关键词规则

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99829](https://developer.work.weixin.qq.com/document/path/99829)
- **文档 ID**: `99829`
- **API 名称**: `update_rule`
- **请求方法**: `POST`
- **接口地址**: `update_rule`
- **分组信息**: 第 4 个接口，共 5 个

## 接口描述

通过此接口修改关键词规则

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| rule_id | string | 是 | 规则id |
| name | string | 否 | 关键词规则名称，长度限制在1~20个字符 |
| keyword.word_list | string[] | 否 | 关键词列表，长度1~32个字符，列表大小不超过20个。 |
| keyword.is_case_sensitive | bool | 否 | 匹配关键词时是否区分大小写，0-不区分；1-区分 |
| keyword.match_rule | int32 | 否 | 关键词匹配方式，0-包含；1-完全匹配 |
| keyword.is_trim_msg | bool | 否 | 是否将消息前后的空格、制表符和换行符去掉后进行匹配，0-否；1-是。仅match_rule=1时生效 |
| semantics.semantics_list | int32[] | 否 | 关键行为列表 1-红包 2-手机号码 3-邮箱地址 ...（详细列表见文档） |
| applicable_range | object | 否 | 规则适用说明，详细说明参考规则适用范围结构体说明 |

### 请求示例

```json
{
	"rule_id": "wwwwwwwwwwwwwwwwwww",
	"name": "已回复",
	"keyword": {...},
	"semantics": {...},
	"applicable_range": {...}
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
