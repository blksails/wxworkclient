# 删除企业客户标签

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96320](https://developer.work.weixin.qq.com/document/path/96320)
- **文档 ID**: `96320`
- **API 名称**: `del_corp_tag`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_corp_tag`
- **分组信息**: 第 4 个接口，共 4 个

## 接口描述

企业可通过此接口删除客户标签库中的标签，或删除整个标签组。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| tag_id | string[] | 否 | 标签的id列表 |
| group_id | string[] | 否 | 标签组的id列表 |
| agentid | uint32 | 否 | 授权方安装的应用agentid。仅旧的第三方多应用套件需要填此参数 |

### 请求示例

```json
{
	"tag_id": ["TAG_ID_1", "TAG_ID_2"],
	"group_id": ["GROUP_ID_1", "GROUP_ID_2"],
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
