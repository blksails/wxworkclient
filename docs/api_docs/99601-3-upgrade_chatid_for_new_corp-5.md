# 对所有新授权企业升级群ID

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99601](https://developer.work.weixin.qq.com/document/path/99601)
- **文档 ID**: `99601`
- **API 名称**: `upgrade_chatid_for_new_corp`
- **请求方法**: `GET`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/idconvert/upgrade_chatid_for_new_corp?suite_access_token=SUITE_ACCESS_TOKEN`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

对代开发应用模板进行群ID升级。调用该接口后，该模板的所有新增授权企业都会升级为服务商主体的群ID，无需逐个企业调用“申请群ID的升级”接口来升级群ID。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| suite_access_token | string | 是 | 代开发模板的接口凭证，服务商可通过“获取代开发应用模板凭证”获得此调用凭证 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |

### 响应示例

```text

```
