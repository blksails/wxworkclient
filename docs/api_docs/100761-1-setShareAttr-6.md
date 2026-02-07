# 分享

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100761](https://developer.work.weixin.qq.com/document/path/100761)
- **文档 ID**: `100761`
- **API 名称**: `setShareAttr`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/setShareAttr?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

在用户分享网页或小程序前，先调用 setShareAttr，将本页面的转发声明为shareticket消息。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 接口调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| withShareTicket | bool | 是 | 是否声明为私密消息 |

### 请求示例

```json
{
  "withShareTicket": true
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |

### 响应示例

#### 示例 1: 成功响应

```json
{
  "errcode": 0,
  "errmsg": "ok"
}
```

#### 示例 2: 失败响应

```json
{
  "errcode": 40001,
  "errmsg": "invalid credential"
}
```

## 其他说明

### 注意事项

分享之后，被移出群的成员将不再有该shareticket消息的访问权限，而后来进群的成员则自动拥有了访问权限。
