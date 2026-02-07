# 更新客户群进群方式配置

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99547](https://developer.work.weixin.qq.com/document/path/99547)
- **文档 ID**: `99547`
- **API 名称**: `update_join_way`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/groupchat/update_join_way`
- **分组信息**: 第 3 个接口，共 4 个

## 接口描述

更新进群方式配置信息。注意：使用覆盖的方式更新

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| config_id | string | 是 | 企业联系方式的配置id |
| scene | int32 | 是 | 场景。 1 - 群的小程序插件 2 - 群的二维码插件 |
| remark | string | 否 | 联系方式的备注信息，用于助记，超过30个字符将被截断 |
| auto_create_room | int32 | 否 | 当群满了后，是否自动新建群。0-否；1-是。 默认为1 |
| room_base_name | string | 否 | 自动建群的群名前缀，当auto_create_room为1时有效。最长40个utf8字符 |
| room_base_id | int32 | 否 | 自动建群的群起始序号，当auto_create_room为1时有效 |
| chat_id_list | array | 是 | 使用该配置的客户群ID列表，最多支持5个。见客户群ID获取方法 |
| state | string | 否 | 企业自定义的state参数，用于区分不同的入群渠道。不超过30个UTF-8字符 如果有设置此参数，在调用获取客户群详情接口时会返回每个群成员对应的该参数值 |
| mark_source | bool | 否 | 是否标记客户添加来源为该应用创建的「加入群聊」, 默认值为true; 仅对「营销获客」应用生效, 且只能由创建此二维码的应用更新 |

### 请求示例

```json
{
	"config_id": "9ad7fa5cdaa6511298498f979c4722de",
	"scene": 2,
	"remark": "bb_remark",
	"auto_create_room": 1,
	"room_base_name" : "销售客服群",
	"room_base_id" : 10,
	"chat_id_list": ["wrOgQhDgAAH2Yy-CTZ6POca8mlBEdaaa", "wrOgQhDgAALPUthpRAKvl7mgiQRw_aaa"],
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
