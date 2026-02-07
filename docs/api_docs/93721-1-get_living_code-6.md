# 获取微信观看直播凭证

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/93721](https://developer.work.weixin.qq.com/document/path/93721)
- **文档 ID**: `93721`
- **API 名称**: `get_living_code`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/living/get_living_code`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

通过微信观看直播的凭证，可在微信中H5或小程序页面唤起企业微信直播小程序，并进入对应直播或直播回放。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证。获取方法查看“获取access_token” |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| livingid | string | 是 | 直播id |
| openid | string | 是 | 微信用户的openid |

### 请求示例

```json
{
   "livingid": "XXXXXXXXX",
   "openid": "abcopenid"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| living_code | string | 微信观看直播凭证，5分钟内可以重复使用，且仅能在微信上使用。开发者获取到该凭证后可以在微信H5页面或小程序进入直播或直播回放页 |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok",
   "living_code": "abcdef"
}
```

## 其他说明

### 权限说明

仅允许获取当前应用创建的微信观看直播凭证。

注：从2023年12月1日0点起，不再支持通过系统应用secret调用接口，存量企业暂不受影响 [查看详情](https://developer.work.weixin.qq.com/document/51165)
