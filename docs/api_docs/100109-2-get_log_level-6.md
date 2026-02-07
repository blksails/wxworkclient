# 获取当前日志打印级别

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100109](https://developer.work.weixin.qq.com/document/path/100109)
- **文档 ID**: `100109`
- **API 名称**: `get_log_level`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/get_log_level`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

获取指定模型或程序的日志打印级别。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| program_id | string | 是 | 应用关联的程序id |

### 请求示例

```json
{
    "program_id": "xxxx"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 错误码描述 |
| log_level | uint32 | 日志级别 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
    "log_level": 3
}
```

## 其他说明

### 权限说明

* 应用需具有数据专区权限
* 指定的程序program_id需与应用有授权关系
* 官方模型不支持
