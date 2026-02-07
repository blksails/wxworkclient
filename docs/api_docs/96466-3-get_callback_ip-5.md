# 获取企业微信服务器的ip段

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96466](https://developer.work.weixin.qq.com/document/path/96466)
- **文档 ID**: `96466`
- **API 名称**: `get_callback_ip`
- **请求方法**: `GET`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/getcallbackip?access_token=ACCESS_TOKEN`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

企业微信在回调企业指定的URL时，是通过特定的IP发送出去的。可以通过这个接口获取到所有相关的IP段。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| ip_list | string | 企业微信回调的IP段 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"ip_list": ["101.226.103.*", "101.226.62.*"]
}
```
