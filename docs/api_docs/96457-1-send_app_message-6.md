# 主动发送应用消息

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96457](https://developer.work.weixin.qq.com/document/path/96457)
- **文档 ID**: `96457`
- **API 名称**: `send_app_message`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

企业后台调用接口通过应用向指定成员发送单聊消息

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| touser | string | 是 | 成员ID列表，多个以|分隔，最多支持1000个 |
| msgtype | string | 是 | 消息类型，text/markdown/image/news/mpnews/voice/file/textcard/news |
| agentid | uint32 | 是 | 企业应用的id |
| text | object | 否 | 文本消息内容 |
| image | object | 否 | 图片消息内容 |
| news | object | 否 | 图文消息内容 |

### 请求示例

```json
{
  "touser": "UserID1|UserID2",
  "msgtype": "text",
  "agentid": 1000002,
  "text": {
    "content": "Hello World"
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
