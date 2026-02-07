# 获取企业上下游通讯录下的企业信息

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96876](https://developer.work.weixin.qq.com/document/path/96876)
- **文档 ID**: `96876`
- **API 名称**: `get_chain_corpinfo`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/corpgroup/corp/get_chain_corpinfo`
- **分组信息**: 第 4 个接口，共 4 个

## 接口描述

自建应用/代开发应用可通过该接口获取企业上下游通讯录的某个企业的自定义id和所属分组的分组id

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证。上游企业应用access_token |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| chain_id | string | 是 | 上下游id |
| corpid | string | 否 | 已加入企业id |
| pending_corpid | string | 否 | 待加入企业id（corpid和pending_corpid至少填一个，同时填corpid生效 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| corp_name | string | 企业名称 |
| qualification_status | int32 | 企业是否验证或认证，1表示未验证，2表示已验证，3表示已认证，已加入的企业返回 |
| custom_id | string | 上下游企业自定义id |
| groupid | int32 | 企业所属上下游的分组id |
| is_joined | bool | 企业是否已加入 |
