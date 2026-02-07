# 获取上下游列表

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96876](https://developer.work.weixin.qq.com/document/path/96876)
- **文档 ID**: `96876`
- **API 名称**: `get_chain_list`
- **请求方法**: `GET`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/corpgroup/corp/get_chain_list`
- **分组信息**: 第 1 个接口，共 4 个

## 接口描述

自建应用/代开发应用可调用，仅返回应用可见范围内的上下游列表

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证。上游企业应用access_token |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| chains | object[] | 企业上下游列表 |
| chains[].chain_id | string | 上下游id |
| chains[].chain_name | string | 上下游名称 |
