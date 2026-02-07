# 获取应用共享信息

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/93644](https://developer.work.weixin.qq.com/document/path/93644)
- **文档 ID**: `93644`
- **API 名称**: `get_shared_app_info`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/get_shared_app_info?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 6 个

## 接口描述

上级企业需要使用特定的接口获取下级应用的身份和权限才能控制下级应用。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 访问令牌 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| corpid | string | 下级企业的企业ID |
| app_id_list | array | 应用ID列表 |
