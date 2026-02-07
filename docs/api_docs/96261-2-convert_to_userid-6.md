# openid转userid

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96261](https://developer.work.weixin.qq.com/document/path/96261)
- **文档 ID**: `96261`
- **API 名称**: `convert_to_userid`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/user/convert_to_userid?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

该接口主要应用于使用企业支付之后的结果查询。开发者需要知道某个结果事件的openid对应企业微信内成员的信息时，可以通过调用该接口进行转换查询。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| openid | string | 是 | 在使用企业支付之后，返回结果的openid |

### 请求示例

```json
{
   "openid": "oDjGHs-1yCnGrRovBj2yHij5JAAA"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| userid | string | 该openid在企业微信对应的成员userid |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok",
   "userid": "zhangsan"
}
```
