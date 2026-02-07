# 企业客户微信unionid的升级方案

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96516](https://developer.work.weixin.qq.com/document/path/96516)
- **文档 ID**: `96516`
- **API 名称**: `unionid_to_external_userid`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/unionid_to_external_userid?access_token=ACCESS_TOKEN`
- **分组信息**: 第 4 个接口，共 4 个

## 接口描述

查询企业客户微信unionid对应的external_userid

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| unionid_list | string[] | 是 | 待查询的微信unionid列表 |

### 请求示例

```json
{
  "unionid_list":["xxxxx","yyyyyy"]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| items | object[] | 查询结果列表 |
| items.unionid | string | 待查询的微信unionid |
| items.external_userid | string | 对应的企业客户external_userid |

### 响应示例

```json
{
 "errcode":0,
 "errmsg":"ok",
 "items":[
 	{
 		"unionid":"xxxxx",
 		"external_userid":"AAAA"
 	},
 	{
 		"unionid":"yyyyy",
 		"external_userid":"BBBB"
 	}
 ]
}
```
