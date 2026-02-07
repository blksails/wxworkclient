# 获取关键词规则详情

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99829](https://developer.work.weixin.qq.com/document/path/99829)
- **文档 ID**: `99829`
- **API 名称**: `get_rule_detail`
- **请求方法**: `POST`
- **接口地址**: `get_rule_detail`
- **分组信息**: 第 3 个接口，共 5 个

## 接口描述

通过此接口获取企业下的关键词规则详情

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| rule_id | string | 是 | 规则id |

### 请求示例

```json
{
	"rule_id":"aaaaaaaaaaaaaaaa"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
| name | string | 关键词规则名称 |
| keyword.word_list | string[] | 关键词列表 |
| keyword.is_case_sensitive | bool | 匹配关键词时是否区分大小写 |
| keyword.match_rule | int32 | 关键词匹配方式 |
| keyword.is_trim_msg | bool | 是否将消息前后的空格、制表符和换行符去掉后进行匹配 |
| semantics.semantics_list | int32[] | 关键行为列表 |
| applicable_range | object | 规则适用说明 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"name": "已回复",
	"keyword": {...},
	"semantics": {...},
	"applicable_range": {...}
}
```
