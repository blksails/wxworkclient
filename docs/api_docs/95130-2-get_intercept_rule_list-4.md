# 获取敏感词规则列表

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95130](https://developer.work.weixin.qq.com/document/path/95130)
- **文档 ID**: `95130`
- **API 名称**: `get_intercept_rule_list`
- **请求方法**: `GET`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_intercept_rule_list`
- **分组信息**: 第 2 个接口，共 5 个

## 接口描述

企业和第三方应用可以通过此接口获取敏感词规则列表

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| rule_list | object[] | 规则列表 |
