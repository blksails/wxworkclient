# 获取接口高频调用凭据

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96250](https://developer.work.weixin.qq.com/document/path/96250)
- **文档 ID**: `96250`
- **API 名称**: `apply_mass_call_ticket`
- **请求方法**: `GET`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/corp/apply_mass_call_ticket?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

应用被授权安装后，往往需要为企业进行较大规模的数据初始化，而企业微信的ID转换等接口会有较为严格的业务频率限制。企业微信允许服务商在企业授权后3个月内申请一个高频调用凭据，调用相关接口时传入该凭据，可以不受业务频率限制。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证，根据应用场景目前支持下列应用: - 第三方应用access_token或代开发应用access_token - 上下游自建或代开发应用的上游应用access_token |

### 请求示例

```json
无
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| mass_call_ticket | string | 大批量调用凭据 |

### 响应示例

```json
{
  "errcode": 0,
  "errmsg": "ok",
  "mass_call_ticket": "AAAAAA"
}
```
