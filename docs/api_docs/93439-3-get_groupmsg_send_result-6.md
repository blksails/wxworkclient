# 获取企业群发成员执行结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/93439](https://developer.work.weixin.qq.com/document/path/93439)
- **文档 ID**: `93439`
- **API 名称**: `get_groupmsg_send_result`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_groupmsg_send_result`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

企业和第三方应用可通过此接口获取企业群发成员执行结果。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| msgid | string | 是 | 群发消息的id，通过获取群发记录列表接口返回 |
| userid | string | 是 | 发送成员userid，通过获取群发成员发送任务列表接口返回 |
| limit | int32 | 否 | 返回的最大记录数，整型，最大值1000，默认值500，超过最大值时取默认值 |
| cursor | string | 否 | 用于分页查询的游标，字符串类型，由上一次调用返回，首次调用可不填 |

### 请求示例

```json
{
    "msgid": "msgGCAAAXtWyujaWJHDDGi0mACAAAA",
	"userid":"zhangsan ",
	"limit":50,
	"cursor":"CURSOR"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| next_cursor | string | 分页游标，再下次请求时填写以获取之后分页的记录，如果已经没有更多的数据则返回空 |
| send_list | object[] | 群成员发送结果列表 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
	"next_cursor":"CURSOR",
    "send_list": [
        {
            "external_userid": "wmqfasd1e19278asdasAAAA",
			"chat_id":"wrOgQhDgAAMYQiS5ol9G7gK9JVAAAA",
            "userid": "zhangsan",
            "status": 1,
            "send_time": 1552536375
        }
    ]
}
```

## 其他说明

### 权限说明

企业需要使用配置到“可调用应用”列表中的自建应用secret所获取的accesstoken来调用（accesstoken如何获取？）。
自建应用调用，只会返回应用可见范围内用户的发送情况。
第三方应用调用需要企业授权客户联系下群发消息给客户和客户群的权限
