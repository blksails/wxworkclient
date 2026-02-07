# 获取上下游通讯录分组

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96876](https://developer.work.weixin.qq.com/document/path/96876)
- **文档 ID**: `96876`
- **API 名称**: `get_chain_group`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/corpgroup/corp/get_chain_group`
- **分组信息**: 第 2 个接口，共 4 个

## 接口描述

自建应用/代开发应用可通过该接口获取企业上下游通讯录分组详情

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证。上游企业应用access_token |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| chain_id | string | 是 | 上下游id |
| groupid | int32 | 否 | 分组id。填写此参数返回指定分组，不填则返回全部分组 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| groups | object[] | 分组列表数据 |
| groups[].groupid | int32 | 分组id |
| groups[].group_name | string | 分组名称 |
| groups[].parentid | int32 | 父分组id。根分组id为1 |
| groups[].order | int32 | 父部门中的次序值。order值大的排序靠前。值范围是[0, 2^32) |
