# 获取成员会话组件敏感信息隐藏配置

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100055](https://developer.work.weixin.qq.com/document/path/100055)
- **文档 ID**: `100055`
- **API 名称**: `get_hide_sensitiveinfo_config`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/get_hide_sensitiveinfo_config?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

获取成员会话组件敏感信息隐藏配置。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userid | string | 是 | 成员的密文userid |

### 请求示例

```json
{
	"userid":"xxxxx"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| config.hide_mobile | bool | 是否隐藏手机号。如果未设置，默认为false |
| config.hide_idcard | bool | 是否隐藏身份证号。如果未设置，默认为false |
| config.hide_bankno | bool | 是否隐藏银行卡号。如果未设置，默认为false |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
	"config":{
		"hide_mobile":false,
		"hide_idcard":true,
		"hide_bankno":true
	}
}
```
