# 企微后台调用专区

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99948](https://developer.work.weixin.qq.com/document/path/99948)
- **文档 ID**: `99948`
- **API 名称**: `callback_sdk`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/callback_sdk`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

程序监听端口，接收到企微后台发起的请求后，利用sdk提供的加解密接口进行验签、解密和构造回包。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| method | string | 是 | 请求方法 |
| headers | object | 是 | 请求头 |
| postData | string | 是 | 请求数据 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| decryptSuccess | bool | 解密成功与否 |
