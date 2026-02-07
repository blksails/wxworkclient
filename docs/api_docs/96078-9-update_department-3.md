# 部门管理接口

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96078](https://developer.work.weixin.qq.com/document/path/96078)
- **文档 ID**: `96078`
- **API 名称**: `update_department`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/department/update`
- **分组信息**: 第 9 个接口，共 14 个

## 接口描述

更新部门

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | uint32 | 是 | 部门ID |
| name | string | 否 | 部门名称 |
| parentid | uint32 | 否 | 父部门ID |
