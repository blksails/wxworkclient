# 获取客户群进群方式配置

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99546](https://developer.work.weixin.qq.com/document/path/99546)
- **文档 ID**: `99546`
- **API 名称**: `get_join_way`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/groupchat/get_join_way`
- **分组信息**: 第 2 个接口，共 4 个

## 接口描述

获取企业配置的群二维码或小程序按钮。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| config_id | string | 是 | 联系方式的配置id |

### 请求示例

```json
{
    "config_id":"9ad7fa5cdaa6511298498f979c472aaa"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| join_way | object | 配置详情 |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"join_way": {
		"config_id": "9ad7fa5cdaa6511298498f979c472aaa",
		"scene": 2,
		"remark": "aa_remark",
		"auto_create_room": 1,
		"room_base_name" : "销售客服群",
		"room_base_id" : 10,
		"chat_id_list": ["wrOgQhDgAAH2Yy-CTZ6POca8mlBEdaaa", "wrOgQhDgAALPUthpRAKvl7mgiQRw_aaa"],
		"qr_code": "http://p.qpic.cn/wwhead/nMl9ssowtibVGyrmvBiaibzDtp703nXuzpibnKtbSDBRJTLwS3ic4ECrf3ibLVtIFb0N6wWwy5LVuyvMQ22/0",
		"state" : "klsdup3kj3s1",
		"mark_source":true
	}
}
```
