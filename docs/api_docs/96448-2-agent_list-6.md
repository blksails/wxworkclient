# 获取access_token对应的应用列表

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96448](https://developer.work.weixin.qq.com/document/path/96448)
- **文档 ID**: `96448`
- **API 名称**: `agent_list`
- **请求方法**: `GET`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/agent/list`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

获取access_token对应的应用列表

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### 请求示例

```json
{
   "access_token": "ACCESS_TOKEN"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 出错返回码，为0表示成功，非0表示调用失败 |
| errmsg | string | 返回码提示语 |
| agentlist | object[] | 当前凭证可访问的应用列表 |

### 响应示例

```json
{
	"errcode":0,
	"errmsg":"ok" ,
	"agentlist":[
		{
			"agentid": 1000005,
			"name": "HR助手",
			"square_logo_url": "https://p.qlogo.cn/bizmail/FicwmI50icF8GH9ib7rUAYR5kicLTgP265naVFQKnleqSlRhiaBx7QA9u7Q/0"
		}
	]
}
```
