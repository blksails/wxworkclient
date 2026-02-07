# 不同应用获取的ID不同

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96248](https://developer.work.weixin.qq.com/document/path/96248)
- **文档 ID**: `96248`
- **API 名称**: `different_ids`
- **请求方法**: `GET`
- **分组信息**: 第 1 个接口，共 8 个

## 接口描述

企业微信中基础的ID概念，不同类型应用获取的ID值不同。

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| corpid | string | 企业ID |
| userid | string | 账号 |
| external_userid | string | 企业外部联系人ID |

## 其他说明

### 不同应用获取的ID不同

在【开发指南-基本概念介绍】中，介绍了企业微信中基础的ID概念，其中corpid、userid、external_userid最为基础，且出于对企业数据的保护，这三种ID类型对企业自建应用、代开发应用、第三方应用返回的ID值有所不同。具体如下：

| 应用类型 | corpid | userid | external_userid |
| --- | --- | --- | --- |
| 自建应用 | 明文corpid | 明文userid | 企业主体下的external_userid |
| 未升级的代开发应用与第三方应用 | 明文corpid | 明文userid | 企业主体下的external_userid |
| 升级后的代开发应用与第三方应用 | 服务商主体下的密文corpid | 服务商主体下的密文userid，也即open_userid | 服务商主体下的external_userid |
