# 为客户升级为专员或客户群服务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/94702](https://developer.work.weixin.qq.com/document/path/94702)
- **文档 ID**: `94702`
- **API 名称**: `upgrade_service`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/kf/customer/upgrade_service?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

企业可通过其他接口获知客户的 external_userid 以及客户与接待人员的聊天内容，因此可以结合实际业务场景，为客户推荐指定的服务专员或客户群。

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
| type | int32 | 是 | 表示是升级到专员服务还是客户群服务。1:专员服务。2:客户群服务 |
| member | object | 否 | 推荐的服务专员，type等于1时有效 |
| member.userid | string | 是 | 服务专员的userid |
| member.wording | string | 否 | 推荐语 |
| groupchat | object | 否 | 推荐的客户群，type等于2时有效 |
| groupchat.chat_id | string | 是 | 客户群id |
| groupchat.wording | string | 否 | 推荐语 |

### 请求示例

#### 示例 1: 升级专员服务

```json
{
	"open_kfid": "kfxxxxxxxxxxxxxx",
	"external_userid": "wmxxxxxxxxxxxxxxxxxx",
	"type": 1,
	"member": {
		"userid": "zhangsan",
		"wording": "你好，我是你的专属服务专员zhangsan"
	}
}
```

#### 示例 2: 升级客户群服务

```json
{
	"open_kfid": "kfxxxxxxxxxxxxxx",
	"external_userid": "wmxxxxxxxxxxxxxxxxxx",
	"type": 2,
	"groupchat": {
		"chat_id": "wraaaaaaaaaaaaaaaa",
		"wording": "欢迎加入你的专属服务群"
	}
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 错误码描述 |
