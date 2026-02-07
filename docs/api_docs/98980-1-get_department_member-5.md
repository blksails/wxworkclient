# 代开发应用获取基础权限

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98980](https://developer.work.weixin.qq.com/document/path/98980)
- **文档 ID**: `98980`
- **API 名称**: `get_department_member`
- **请求方法**: `POST`
- **接口地址**: `https://developer.work.weixin.qq.com/document/path/90200`
- **分组信息**: 第 1 个接口，共 5 个

## 接口描述

可获取应用可见范围内，成员基础信息，包括成员账号和部门id，其他敏感信息无法获取； 具备基础的成员ID互换、验证、邀请的接口权限。

## 请求信息

### 请求示例

```json
{"department_id": 1}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
| department_id | uint32 | 部门ID |
| member_id | string | 成员账号 |

### 响应示例

```json
{"errcode": 0, "errmsg": "ok", "department_id": 1, "member_id": "john_doe"}
```
