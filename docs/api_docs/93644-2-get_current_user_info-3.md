# 获取当前使用者信息

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/93644](https://developer.work.weixin.qq.com/document/path/93644)
- **文档 ID**: `93644`
- **API 名称**: `get_current_user_info`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/get_current_user_info?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 6 个

## 接口描述

需要得知当前使用者到底属于哪个企业。

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| UserId | string | 当前使用者的UserID，格式为CorpId/userid |
