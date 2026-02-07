# 申请群ID的升级

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99601](https://developer.work.weixin.qq.com/document/path/99601)
- **文档 ID**: `99601`
- **API 名称**: `apply_to_upgrade_chatid`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/idconvert/apply_to_upgrade_chatid?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

设置代开发应用群ID完成升级的时间。在调用该接口后，用户可以使用新旧两种群ID调用相关接口。在到达设置的完成升级的时间点后，用户必须使用升级后的群ID调用接口，企业微信会返回升级后的群ID。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 代开发应用的接口凭证，服务商可通过“获取企业access_token”获得此调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| upgrade_time | int | 是 | 完成升级的时间戳。不得设置早于当前时间或7天之后的时间 |

### 请求示例

```json
{
  "upgrade_time": 1234567
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok"
}
```
