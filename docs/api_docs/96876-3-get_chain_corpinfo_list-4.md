# 获取企业上下游通讯录分组下的企业详情列表

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96876](https://developer.work.weixin.qq.com/document/path/96876)
- **文档 ID**: `96876`
- **API 名称**: `get_chain_corpinfo_list`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/corpgroup/corp/get_chain_corpinfo_list`
- **分组信息**: 第 3 个接口，共 4 个

## 接口描述

自建应用/代开发应用可通过该接口获取企业上下游通讯录的某个分组下的企业列表

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证。上游企业应用access_token |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| chain_id | string | 是 | 上下游id |
| groupid | int32 | 否 | 分组id。如果不填，表示根目录 |
| need_pending | bool | 否 | 是否需要返回未加入的企业。默认不返回 |
| cursor | string | 否 | 开启分页使用，传入返回值next_cursor |
| limit | int32 | 否 | >0开启分页功能 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| has_more | bool | 开启分页时告知是否还有更多记录 |
| next_cursor | string | 下次请求时应传入的cursor |
| group_corps | object[] | 分组列表数据 |
| group_corps[].groupid | int32 | 企业所属上下游的分组id |
| group_corps[].corpid | string | 企业id，最多64个字节，已加入的企业返回 |
| group_corps[].corp_name | string | 企业名称 |
| group_corps[].custom_id | string | 上下游企业自定义id |
| group_corps[].invite_userid | string | 该上下游的邀请人的userid |
| group_corps[].pending_corpid | string | 未加入企业id |
| group_corps[].is_joined | int32 | 企业是否已加入 |
