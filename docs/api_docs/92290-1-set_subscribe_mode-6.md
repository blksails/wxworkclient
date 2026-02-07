# 设置关注「学校通知」的模式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/92290](https://developer.work.weixin.qq.com/document/path/92290)
- **文档 ID**: `92290`
- **API 名称**: `set_subscribe_mode`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/set_subscribe_mode`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

可通过此接口修改家长关注「学校通知」的模式：“可扫码填写资料加入”或“禁止扫码填写资料加入”

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| subscribe_mode | int32 | 是 | 关注模式, 1:可扫码填写资料加入, 2:禁止扫码填写资料加入 |

### 请求示例

```json
{
   "subscribe_mode":1
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok"
}
```
