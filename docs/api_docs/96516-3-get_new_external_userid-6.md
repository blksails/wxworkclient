# 企业客户external_userid的升级方案

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96516](https://developer.work.weixin.qq.com/document/path/96516)
- **文档 ID**: `96516`
- **API 名称**: `get_new_external_userid`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_new_external_userid?access_token=ACCESS_TOKEN`
- **分组信息**: 第 3 个接口，共 4 个

## 接口描述

转换已获授权企业的external_userid

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| external_userid_list | string[] | 是 | 旧外部联系人id列表，建议200个，最多不超过1000个 |

### 请求示例

```json
{
  "external_userid_list":["xxxxx","yyyyyy"]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| items | object[] | 转换成功的external_userid列表 |
| items.external_userid | string | 旧外部联系人id |
| items.new_external_userid | string | 新外部联系人id |

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
