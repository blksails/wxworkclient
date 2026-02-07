# 获取群聊会话同意情况

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99826](https://developer.work.weixin.qq.com/document/path/99826)
- **文档 ID**: `99826`
- **API 名称**: `get_agree_status_room`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/get_agree_status_room`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

通过下述接口，获取群聊会话中所有外企业的外部联系人的同意情况

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| chatid | string | 是 | 待查询的chatid |

### 请求示例

```json
{
	"chatid":"wrjc7bDwAASxc8tZvBErFE02BtPWyAAA"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| agreeinfo | object[] | 同意情况 |
| agreeinfo[].status_change_time | int32 | 同意状态改变的具体时间，utc时间 |
| agreeinfo[].external_userid | string | 群内外部联系人的external_userid |
| agreeinfo[].agree_status | string | 同意状态，Agree 或 Disagree |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok",
   "agreeinfo" : [
    {
     "status_change_time" : 1562766651,
     "external_userid" : "wmeDKaCQAAGdtHdiQWxVadfwV2HxNAAA",
	 "agree_status":"Agree"
    },
	{
     "status_change_time" : 1562766651,
     "external_userid" : "wmeDKaCQAAIQ_p9ACyiopLBBJSGocAAA",
	 "agree_status":"Disagree"
    },
	{
     "status_change_time" : 1562766651,
     "external_userid" : "wmeDKaCQAAIQ_p9ACnxacyBBJSGocAAA",
	 "agree_status":"Agree"
    }
    ]
}
```
