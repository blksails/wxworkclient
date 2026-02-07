# 获取服务商凭证

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/91201](https://developer.work.weixin.qq.com/document/path/91201)
- **文档 ID**: `91201`
- **API 名称**: `get_provider_access_token`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/service/get_provider_token`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

用于服务商级别的接口调用，比如登录授权、推广二维码等。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| corpid | string | 是 | 服务商CorpID |
| provider_secret | string | 是 | 服务商密钥 |

### 请求示例

```json
{
  "corpid": "wxdd725338566d6ffe",
  "provider_secret": "vQT_03RsfVA3uE6J5dofR7hJeOdiXUvccqV8mDgLdLI"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| provider_access_token | string | 服务商访问令牌 |

### 响应示例

```json
{
  "provider_access_token": "ACCESS_TOKEN"
}
```
