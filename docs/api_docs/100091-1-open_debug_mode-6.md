# 应用开启调试模式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100091](https://developer.work.weixin.qq.com/document/path/100091)
- **文档 ID**: `100091`
- **API 名称**: `open_debug_mode`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/open_debug_mode?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

应用通过接口将指定的程序开启调试模式

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| program_id | string | 是 | 应用关联的程序id |
| debug_token | string | 是 | 程序的调试凭证 |

### 请求示例

```json
{
  "program_id": "xxx",
  "debug_token": "xxx"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |

### 响应示例

```json
{
  "errcode": 0,
  "errmsg": "ok"
}
```

## 其他说明

### 权限说明

| 应用类型 | 权限要求 |
| --- | --- |
| 自建应用 | 需具备「数据与智能专区权限」 |
| 代开发应用 | 需具备「数据与智能专区权限」 |
| 第三方应用 | 需具备「数据与智能专区权限」 |

> 对于第三方应用，仅通过测试安装的企业可开启调试模式
> 对于代开发应用，企业必须为服务商的测试企业
