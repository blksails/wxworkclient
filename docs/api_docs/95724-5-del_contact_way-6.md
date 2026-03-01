# 删除企业已配置的「联系我」方式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95724](https://developer.work.weixin.qq.com/document/path/95724)
- **文档 ID**: `95724`
- **API 名称**: `del_contact_way`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_contact_way?access_token=ACCESS_TOKEN`
- **分组信息**: 第 5 个接口，共 6 个

## 接口描述

删除一个已配置的「联系我」二维码或者「联系我」小程序按钮。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| config_id | string | 是 | 企业联系方式的配置id |

### 请求示例

```json
{
	"config_id":"42b34949e138eb6e027c123cba77fAAA"
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
