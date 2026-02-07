# secret的获取

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97163](https://developer.work.weixin.qq.com/document/path/97163)
- **文档 ID**: `97163`
- **API 名称**: `get_permanent_code`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/service/v2/get_permanent_code?suite_access_token=SUITE_ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

对于代开发应用的secret获取方式与第三方应用中的企业永久授权码相似，流程如下...

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| auth_code | string | 是 | 临时授权码，会在授权成功时附加在redirect_uri中跳转回第三方服务商网站，或通过授权成功通知回调推送给服务商。长度为64至512个字节 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
| permanent_code | string | 企业微信永久授权码，最长为512字节 |
| auth_corp_info.corpid | string | 授权方企业微信id |
| auth_corp_info.corp_name | string | 授权方企业名称，即企业简称 |
| auth_user_info.userid | string | 授权管理员的userid，可能为空 |
| auth_user_info.open_userid | string | 授权管理员的open_userid，可能为空 |
| auth_user_info.name | string | 授权管理员的name，可能为空 |
| auth_user_info.avatar | string | 授权管理员的头像url，可能为空 |
| register_code_info.register_code | string | 注册码 |
| register_code_info.template_id | string | 推广包ID |
| register_code_info.state | string | 仅当获取注册码指定该字段时才返回 |
| state | string | 安装应用时，扫码或者授权链接中带的state值。详见state说明 |
