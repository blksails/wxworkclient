# 转换客户群成员external_userid

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97107](https://developer.work.weixin.qq.com/document/path/97107)
- **文档 ID**: `97107`
- **API 名称**: `get_new_external_userid`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/groupchat/get_new_external_userid?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

转换客户群中无好友关系的群成员external_userid。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 代开发自建应用或第三方应用的接口凭证，服务商可通过“获取企业access_token”获得此调用凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| chat_id | string | 是 | 客户群ID |
| external_userid_list | array | 是 | 企业主体下的external_userid列表，建议200个，最多不超过1000个 |

### 请求示例

```json
{
  "chat_id":"wrOgQhDgAAMYQiS5ol9G7gK9JVAAAA",
  "external_userid_list":["xxxxx","yyyyyy"]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| items | object[] | 转换结果列表 |
| items[].external_userid | string | 原始external_userid |
| items[].new_external_userid | string | 服务商主体下的新external_userid |

### 响应示例

```json
{
 "errcode":0,
 "errmsg":"ok",
 "items":[
 	{
 		"external_userid":"xxxxx",
 		"new_external_userid":"AAAA"
 	},
 	{
 		"external_userid":"yyyyy",
 		"new_external_userid":"BBBB"
 	}
 ]
}
```
