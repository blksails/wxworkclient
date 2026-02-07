# 删除获客链接

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97394](https://developer.work.weixin.qq.com/document/path/97394)
- **文档 ID**: `97394`
- **API 名称**: `delete_link`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/customer_acquisition/delete_link?access_token=ACCESS_TOKEN`
- **分组信息**: 第 5 个接口，共 5 个

## 接口描述

企业可通过此接口删除获客链接，删除后的获客链接将无法继续使用。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| link_id | string | 是 | 获客链接的id。需要是当前应用创建 |

### 请求示例

```json
{
   "link_id":"LINK_ID"
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
