# 部门管理接口

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96078](https://developer.work.weixin.qq.com/document/path/96078)
- **文档 ID**: `96078`
- **API 名称**: `create_department`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/department/create`
- **分组信息**: 第 8 个接口，共 14 个

## 接口描述

创建部门

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 部门名称 |
| parentid | uint32 | 是 | 父部门ID |
