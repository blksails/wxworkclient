# 获取盘容量信息

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95861](https://developer.work.weixin.qq.com/document/path/95861)
- **文档 ID**: `95861`
- **API 名称**: `mng_capacity`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/wedrive/mng_capacity`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

该接口用于获取盘容量信息。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 访问令牌 |

### 请求示例

```json
{
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| total_capacity_for_all | uint64 | 全员容量总数,单位是B |
| total_capacity_for_vip | uint64 | 专业容量总数,单位是B |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
    "total_capacity_for_all": 22666689904640,
    "total_capacity_for_vip": 22300038149020
}
```

## 其他说明

### 权限说明

企业需要使用“微盘”secret所获取的accesstoken来调用...
