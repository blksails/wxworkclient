# 异步导出接口

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96292](https://developer.work.weixin.qq.com/document/path/96292)
- **文档 ID**: `96292`
- **API 名称**: `get_department_id_list`
- **请求方法**: `GET`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/asyncexport/get_department_id_list?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

获取部门ID列表

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
| department_id_list | string[] | 部门ID列表 |
