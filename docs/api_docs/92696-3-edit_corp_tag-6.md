# 编辑企业客户标签

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/92696](https://developer.work.weixin.qq.com/document/path/92696)
- **文档 ID**: `92696`
- **API 名称**: `edit_corp_tag`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/edit_corp_tag?access_token=ACCESS_TOKEN`
- **分组信息**: 第 3 个接口，共 4 个

## 接口描述

企业可通过此接口编辑客户标签/标签组的名称或次序值。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | string | 是 | 标签或标签组的id |
| name | string | 否 | 新的标签或标签组名称，最长为30个字符 |
| order | uint32 | 否 | 标签/标签组的次序值 |
| agentid | string | 否 | 授权方安装的应用agentid |

### 请求示例

```json
{
	"id": "TAG_ID",
	"name": "NEW_TAG_NAME",
	"order": 1,
	"agentid" : 1000014
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
