# 获取盘专业版信息

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95861](https://developer.work.weixin.qq.com/document/path/95861)
- **文档 ID**: `95861`
- **API 名称**: `mng_pro_info`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/wedrive/mng_pro_info?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

该接口用于获取专业版信息。

## 请求信息

### 请求示例

```json
{
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误码说明 |
| is_pro | bool | true为专业版，false为不是专业版 |
| total_vip_acct_num | uint32 | 总的vip账号数量 |
| use_vip_acct_num | uint32 | 已使用的vip账号数量 |
| pro_expire_time | uint32 | 专业版到期时间，时间戳，精确到秒 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
    "is_pro": true,
    "total_vip_acct_num": 10,
    "use_vip_acct_num": 5,
    "pro_expire_time": 1754827419
}
```

## 其他说明

### 权限说明

企业需要使用“微盘”secret所获取的accesstoken来调用（accesstoken如何获取？）
自建应用需配置到“可调用应用”列表中的应用secret所获取的accesstoken来调用（accesstoken如何获取？）
第三方应用需具有“微盘”权限
代开发自建应用需具有“微盘”权限
