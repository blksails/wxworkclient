# 获取企业微信服务器的ip段

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/91116](https://developer.work.weixin.qq.com/document/path/91116)
- **文档 ID**: `91116`
- **API 名称**: `get_callback_ip`
- **请求方法**: `GET`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/getcallbackip?access_token=ACCESS_TOKEN`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

获取企业微信服务器的IP段

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### 请求示例

```text
GET https://qyapi.weixin.qq.com/cgi-bin/getcallbackip?access_token=ACCESS_TOKEN
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| ip_list | array | 企业微信服务器IP段 |
| errcode | int32 | 错误码，0表示成功，非0表示调用失败 |
| errmsg | string | 错误信息，调用失败会有相关的错误信息返回 |

### 响应示例

#### 示例 1: 成功响应示例

```json
{
    "ip_list":[
        "1.2.3.4",
        "2.3.3.3"
    ],
    "errcode":0,
    "errmsg":"ok"
}
```

#### 示例 2: 过期响应示例

```json
{
    "ip_list":[],
    "errcode":42001,
    "errmsg":"access_token expired, hint: [1576065934_28_e0fae07666aa64636023c1fa7e8f49a4], from ip: 9.30.0.138, more info at https://open.work.weixin.qq.com/devtool/query?e=42001"
}
```
