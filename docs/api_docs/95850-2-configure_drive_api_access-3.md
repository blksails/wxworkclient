# 配置可调用微盘接口的应用

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95850](https://developer.work.weixin.qq.com/document/path/95850)
- **文档 ID**: `95850`
- **API 名称**: `configure_drive_api_access`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/wedrive/configure_drive_api_access?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

应用在调用微盘接口前，需要先获得微盘的使用权限。

## 请求信息

### 请求示例

```json
{
  "app_id": "APP_ID",
  "permissions": ["read", "write"]
}
```

## 其他说明

### 配置可调用微盘接口的应用

应用在调用微盘接口前，需要先获得微盘的使用权限。
