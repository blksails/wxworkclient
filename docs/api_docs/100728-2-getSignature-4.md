# 根据提供的参数生成 jsapi 签名

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100728](https://developer.work.weixin.qq.com/document/path/100728)
- **文档 ID**: `100728`
- **API 名称**: `getSignature`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

根据提供的参数生成 jsapi 签名

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| options.ticket | string | 是 | 用于签名的 jsapi ticket |
| options.nonceStr | string | 否 | 生成签名的随机串 |
| options.timestamp | string | 否 | 生成签名的时间戳 |
| options.url | string | 否 | 当前页面的 URL |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| timestamp | string | 生成签名的时间戳 |
| nonceStr | string | 生成签名的随机串 |
| signature | string | jsapi 签名 |

## 其他说明

### 功能描述

根据提供的参数生成 jsapi 签名

### 参数说明

#### options: Object

|  | 属性 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
|  | ticket | string | 是 | 用于签名的 jsapi ticket |
|  | nonceStr | string | 否 | 生成签名的随机串 |
|  | timestamp | string | number | 否 | 生成签名的时间戳 |
|  | url | string | 否 | 当前页面的 URL |

### 返回说明

**Object**

|  | 属性 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
|  | timestamp | string | number | 是 | 生成签名的时间戳 |
|  | nonceStr | string | 是 | 生成签名的随机串 |
|  | signature | string | 是 | jsapi 签名 |
