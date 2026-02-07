# 删除敏感词规则

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95130](https://developer.work.weixin.qq.com/document/path/95130)
- **文档 ID**: `95130`
- **API 名称**: `del_intercept_rule`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_intercept_rule`
- **分组信息**: 第 5 个接口，共 5 个

## 接口描述

企业和第三方应用可以通过此接口修改敏感词规则

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| rule_id | string | 是 | 规则id |

### 请求示例

```json
{
	"rule_id":"xxx"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
