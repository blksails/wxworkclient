# 获取access_token对应的应用列表

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/90363](https://developer.work.weixin.qq.com/document/path/90363)
- **文档 ID**: `90363`
- **API 名称**: `agent_list`
- **请求方法**: `GET`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/agent/list?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

获取access_token对应的应用列表

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 出错返回码，为0表示成功，非0表示调用失败 |
| errmsg | string | 返回码提示语 |
| agentlist | object[] | 当前凭证可访问的应用列表 |
| agentlist[].agentid | int32 | 企业应用id |
| agentlist[].name | string | 企业应用名称 |
| agentlist[].square_logo_url | string | 企业应用方形头像url |
