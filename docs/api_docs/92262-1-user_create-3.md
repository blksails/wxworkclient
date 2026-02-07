# 创建成员对外信息

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/92262](https://developer.work.weixin.qq.com/document/path/92262)
- **文档 ID**: `92262`
- **API 名称**: `user_create`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/user/create`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

调用创建成员接口设置成员对外信息。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| external_profile.external_attr | object[] | 是 | 属性列表，支持文本、网页、小程序三种类型 |
| external_profile.external_attr[].type | uint32 | 是 | 属性类型: 0-文本 1-网页 2-小程序 |
| external_profile.external_attr[].name | string | 是 | 属性名称 |
| external_profile.external_attr[].text | object | 否 | 文本类型的属性 |
| external_profile.external_attr[].text.value | string | 否 | 文本属性内容，长度限制32个UTF8字符 |
| external_profile.external_attr[].web | object | 否 | 网页类型的属性 |
| external_profile.external_attr[].web.url | string | 否 | 网页的url |
| external_profile.external_attr[].web.title | string | 否 | 网页的展示标题，长度限制12个UTF8字符 |
| external_profile.external_attr[].miniprogram | object | 否 | 小程序类型的属性 |
| external_profile.external_attr[].miniprogram.appid | string | 否 | 小程序appid |
| external_profile.external_attr[].miniprogram.title | string | 否 | 小程序的展示标题，长度限制12个UTF8字符 |
| external_profile.external_attr[].miniprogram.pagepath | string | 否 | 小程序的页面路径 |
| external_profile.external_corp_name | string | 否 | 企业对外简称 |
| external_profile.wechat_channels | object | 否 | 视频号属性 |
| external_profile.wechat_channels.nickname | string | 否 | 视频号名字 |
| external_profile.wechat_channels.status | uint32 | 否 | 对外展示视频号状态 |
