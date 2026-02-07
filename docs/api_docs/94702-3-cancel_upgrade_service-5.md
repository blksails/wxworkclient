# 为客户取消推荐

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/94702](https://developer.work.weixin.qq.com/document/path/94702)
- **文档 ID**: `94702`
- **API 名称**: `cancel_upgrade_service`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/kf/customer/cancel_upgrade_service?access_token=ACCESS_TOKEN`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

当企业通过 API 为客户指定了专员或客户群后，如果客户已经完成服务升级，或是企业需要取消推荐，则可调用该接口清空之前为客户指定的专员或客户群。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| open_kfid | string | 是 | 客服账号ID |
| external_userid | string | 是 | 微信客户的external_userid |

### 请求示例

```json
{
	"open_kfid": "kfxxxxxxxxxxxxxx",
	"external_userid": "wmxxxxxxxxxxxxxxxxxx"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 错误码描述 |
