# 接收消息

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/90371](https://developer.work.weixin.qq.com/document/path/90371)
- **文档 ID**: `90371`
- **API 名称**: `receive_message`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/webhook/receive?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

企业后台接收来自成员的消息或事件

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 访问令牌 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| msgtype | string | 是 | 消息类型 |
| event | string | 否 | 事件类型 |
| text.content | string | 否 | 消息内容 |

### 请求示例

```json
{
  "msgtype": "text",
  "text": {
    "content": "Hello"
  }
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |

### 响应示例

```json
{
  "errcode": 0,
  "errmsg": "ok"
}
```
