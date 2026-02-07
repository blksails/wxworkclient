# 验证

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100761](https://developer.work.weixin.qq.com/document/path/100761)
- **文档 ID**: `100761`
- **API 名称**: `getShareInfo`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/getShareInfo?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

带有shareticket的消息卡片，用户打开网页或小程序，开发者调用getContext时，可以得到shareticket。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 接口调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| shareticket | string | 是 | 分享凭证 |

### 请求示例

```json
{
  "shareticket": "abc123"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| encryptedData | string | 加密的数据 |

### 响应示例

#### 示例 1: 成功响应

```json
{
  "encryptedData": "xyz456"
}
```

#### 示例 2: 失败响应

```json
{
  "errcode": 40002,
  "errmsg": "invalid shareticket"
}
```

## 其他说明

### 注意事项

为了避免encryptedData被重放攻击，我们建议开发者检查curReceiver与oauth2获得的userid（或open_userid）是否一致。
