# 从企业微信管理端单点登录

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98170](https://developer.work.weixin.qq.com/document/path/98170)
- **文档 ID**: `98170`
- **API 名称**: `admin_login`
- **请求方法**: `GET`
- **接口地址**: `https://www.example.com`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

企业微信管理员可从第三方应用的‘业务设置’入口跳转到第三方网站，流程是：

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| auth_code | string | 是 | 登录授权码 |

### 请求示例

```text
https://www.example.com?auth_code=xxx
```
