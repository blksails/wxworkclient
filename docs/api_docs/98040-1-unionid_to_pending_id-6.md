# unionid查询pending_id

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98040](https://developer.work.weixin.qq.com/document/path/98040)
- **文档 ID**: `98040`
- **API 名称**: `unionid_to_pending_id`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/corpgroup/unionid_to_pending_id?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

该接口有调用频率限制，按上游企业维度，限制为：10万次/小时、48万次/天、750万次/月。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 上游企业自建应用或代开发应用的access_token |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| unionid | string | 是 | 微信客户的unionid |
| openid | string | 是 | 微信客户的openid |

### 请求示例

```json
{
    "unionid":"UNIONID",
    "openid":"OPENID"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| pending_id | string | unionid和openid对应的pending_id |

### 响应示例

```json
{
    "errcode":0,
    "errmsg":"ok",
    "pending_id":"PENDINGID"
}
```
