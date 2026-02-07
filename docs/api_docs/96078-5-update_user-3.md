# 成员管理接口

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96078](https://developer.work.weixin.qq.com/document/path/96078)
- **文档 ID**: `96078`
- **API 名称**: `update_user`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/user/update`
- **分组信息**: 第 5 个接口，共 14 个

## 接口描述

更新成员

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userid | string | 是 | 成员userid |
| name | string | 否 | 成员姓名 |
| mobile | string | 否 | 成员手机号 |
| department | uint32[] | 否 | 成员所属部门ID列表 |
