# 获取接口高频调用凭据

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96168](https://developer.work.weixin.qq.com/document/path/96168)
- **文档 ID**: `96168`
- **API 名称**: `apply_mass_call_ticket`
- **请求方法**: `GET`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/corp/apply_mass_call_ticket?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

企业微信允许服务商在企业授权后3个月内申请一个高频调用凭据，调用相关接口时传入该凭据，可以不受业务频率限制。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证，根据应用场景目前支持下列应用: - 第三方应用access_token 或 代开发应用access_token - 上下游自建或代开发应用的上游应用access_token |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| mass_call_ticket | string | 大批量调用凭据 |
