# 成员管理接口

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96078](https://developer.work.weixin.qq.com/document/path/96078)
- **文档 ID**: `96078`
- **API 名称**: `create_user`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/user/create`
- **分组信息**: 第 4 个接口，共 14 个

## 接口描述

创建成员

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userid | string | 是 | 成员userid |
| name | string | 是 | 成员姓名 |
| mobile | string | 是 | 成员手机号 |
| department | uint32[] | 是 | 成员所属部门ID列表 |
