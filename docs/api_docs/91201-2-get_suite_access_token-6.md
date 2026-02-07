# 获取第三方应用凭证

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/91201](https://developer.work.weixin.qq.com/document/path/91201)
- **文档 ID**: `91201`
- **API 名称**: `get_suite_access_token`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/service/get_suite_token`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

用于获取第三方应用的预授权码，获取授权企业信息等。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| suite_id | string | 是 | 第三方应用ID |
| suite_secret | string | 是 | 第三方应用密钥 |

### 请求示例

```json
{
  "suite_id": "YOUR_SUITE_ID",
  "suite_secret": "YOUR_SUITE_SECRET"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| suite_access_token | string | 第三方应用访问令牌 |

### 响应示例

```json
{
  "suite_access_token": "ACCESS_TOKEN"
}
```
