# 获取企业凭证

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/91201](https://developer.work.weixin.qq.com/document/path/91201)
- **文档 ID**: `91201`
- **API 名称**: `get_corp_access_token`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/service/get_corp_token`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

用于操作授权企业相关接口，如通讯录管理，消息推送等。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| corp_id | string | 是 | 企业CorpID |
| permanent_code | string | 是 | 永久授权码 |

### 请求示例

```json
{
  "corp_id": "ENTERPRISE_CORP_ID",
  "permanent_code": "PERMANENT_AUTH_CODE"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| access_token | string | 企业访问令牌 |

### 响应示例

```json
{
  "access_token": "ACCESS_TOKEN"
}
```
