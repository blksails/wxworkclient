# 设置日志打印级别

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100106](https://developer.work.weixin.qq.com/document/path/100106)
- **文档 ID**: `100106`
- **API 名称**: `set_log_level`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/set_log_level`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

设置指定模型或程序的日志打印级别。专区程序只会存储不高于该级别的日志。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| program_id | string | 是 | 应用关联的程序id |
| log_level | uint32 | 是 | 日志级别。指定后，仅会存储不高于该级别的日志。默认级别为2。取值范围：1 - ERR, 2 - INFO, 3 - DBG |

### 请求示例

```json
{
    "program_id": "xxxx",
    "log_level": 2
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 错误码描述 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok"
}
```
