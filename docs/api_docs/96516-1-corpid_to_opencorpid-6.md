# 企业corpid的升级方案

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96516](https://developer.work.weixin.qq.com/document/path/96516)
- **文档 ID**: `96516`
- **API 名称**: `corpid_to_opencorpid`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/service/corpid_to_opencorpid?provider_access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 4 个

## 接口描述

将明文corpid转换为第三方应用获取的corpid

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| provider_access_token | string | 是 | 应用服务商的provider_access_token |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| corpid | string | 是 | 待获取的企业ID |

### 请求示例

```json
{
  "corpid":"xxxxx"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| open_corpid | string | 该服务商第三方应用下的企业ID |

### 响应示例

```json
{
 "errcode":0,
 "errmsg":"ok",
 "open_corpid":"AAAAAA"
}
```
