# 获取配置的专员与客户群

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/94702](https://developer.work.weixin.qq.com/document/path/94702)
- **文档 ID**: `94702`
- **API 名称**: `get_upgrade_service_config`
- **请求方法**: `GET`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/kf/customer/get_upgrade_service_config?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

提供获取配置的专员与客户群列表的能力。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 错误码描述 |
| member_range | object | 专员服务配置范围 |
| member_range.userid_list | string | 专员userid列表 |
| member_range.department_list | uint32 | 专员部门列表 |
| groupchat_range | object | 客户群配置范围 |
| groupchat_range.chat_id_list | string | 客户群列表 |
