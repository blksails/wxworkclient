# 结束临时会话

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95724](https://developer.work.weixin.qq.com/document/path/95724)
- **文档 ID**: `95724`
- **API 名称**: `close_temp_chat`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/close_temp_chat?access_token=ACCESS_TOKEN`
- **分组信息**: 第 6 个接口，共 6 个

## 接口描述

将指定的企业成员和客户之间的临时会话断开，断开前会自动下发已配置的结束语。注意：需保证成员和客户之间仍有有效的临时会话；通过其他方式添加的外部联系人无法通过此接口关闭会话。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userid | string | 是 | 企业成员的userid |
| external_userid | string | 是 | 客户的外部联系人userid |

### 请求示例

```json
{
	"userid":"zhangyisheng",
	"external_userid":"woAJ2GCAAAXtWyujaWJHDDGi0mACHAAA"
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
