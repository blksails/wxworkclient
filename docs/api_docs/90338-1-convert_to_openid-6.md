# userid转openid

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/90338](https://developer.work.weixin.qq.com/document/path/90338)
- **文档 ID**: `90338`
- **API 名称**: `convert_to_openid`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/user/convert_to_openid?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

该接口使用场景为企业支付，在使用企业红包和向员工付款时，需要自行将企业微信的userid转成openid。需要成员使用微信登录企业微信或者关注微信插件（原企业号）才能转成openid。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userid | string | 是 | 企业内的成员id |

### 请求示例

```json
{
   "userid": "zhangsan"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| openid | string | 企业微信成员userid对应的openid |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok",
   "openid": "oDjGHs-1yCnGrRovBj2yHij5JAAA"
}
```
