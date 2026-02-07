# 配置客户群进群方式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99546](https://developer.work.weixin.qq.com/document/path/99546)
- **文档 ID**: `99546`
- **API 名称**: `add_join_way`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/groupchat/add_join_way`
- **分组信息**: 第 1 个接口，共 4 个

## 接口描述

企业可调用此接口来生成并配置「加入群聊」的二维码或者小程序按钮，客户通过扫描二维码或点击小程序上的按钮，即可加入特定的客户群。每个企业最多可配置50万个「加入群聊」。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| scene | int32 | 是 | 场景。1 - 群的小程序插件；2 - 群的二维码插件 |
| remark | string | 否 | 联系方式的备注信息，用于助记，超过30个字符将被截断 |
| auto_create_room | int32 | 否 | 当群满了后，是否自动新建群。0-否；1-是。默认为1 |
| room_base_name | string | 否 | 自动建群的群名前缀，当auto_create_room为1时有效。最长40个utf8字符 |
| room_base_id | int32 | 否 | 自动建群的群起始序号，当auto_create_room为1时有效 |
| chat_id_list | string[] | 是 | 使用该配置的客户群ID列表，最多支持5个 |
| state | string | 否 | 企业自定义的state参数，用于区分不同的入群渠道。不超过30个UTF-8字符 |
| mark_source | bool | 否 | 是否标记客户添加来源为该应用创建的「加入群聊」。默认值为true；仅对「营销获客」应用生效 |

### 请求示例

```json
{
	"scene": 2,
	"remark": "aa_remark",
	"auto_create_room": 1,
	"room_base_name" : "销售客服群",
	"room_base_id" : 10,
	"chat_id_list": [
		"wrOgQhDgAAH2Yy-CTZ6POca8mlBEdaaa",
		"wrOgQhDgAALPUthpRAKvl7mgiQRwAAA"
	],
	"state" : "klsdup3kj3s1",
	"mark_source":true
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| config_id | string | 配置id |

### 响应示例

```json
{
	"errcode": 0,
	"errmsg": "ok",
	"config_id": "9ad7fa5cdaa6511298498f979c472aaa"
}
```
