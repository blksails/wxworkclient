# 获取单聊会话同意情况

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100024](https://developer.work.weixin.qq.com/document/path/100024)
- **文档 ID**: `100024`
- **API 名称**: `get_agree_status_single`
- **请求方法**: `SDK调用`
- **接口地址**: `get_agree_status_single`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

通过下述接口，批量获取单聊会话中外部成员的同意情况

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| item | object[] | 是 | 待查询的会话信息，数组 |
| item[].userid | string | 是 | 内部成员的userid |
| item[].external_userid | string | 是 | 外部成员的external_userid |

### 请求示例

```json
{
    "item": [
        {
            "userid": "XuJinSheng",
            "external_userid": "wmeDKaCQAAGd9oGiQWxVsAKwV2HxNAAA"
        },
        {
            "userid": "XuJinSheng",
            "external_userid": "wmeDKaCQAAIQ_p7ACn_jpLVBJSGocAAA"
        },
        {
            "userid": "XuJinSheng",
            "external_userid": "wmeDKaCQAAPE_p7ABnxkpLBBJSGocAAA"
        }
    ]
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
| agreeinfo[].userid | string | 内部成员的userid |
| agreeinfo[].external_userid | string | 外部成员的external_userid |
| agreeinfo[].agree_status | string | 同意状态：'Agree'，不同意：'Disagree' |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok",
   "agreeinfo" : [
    {
     "status_change_time" : 1562766651,
     "userid" : "XuJinSheng",
     "external_userid" : "wmeDKaCPAAGdvxciQWxVsAKwV2HxNAAA",
	 "agree_status":"Agree"
    },
	{
     "status_change_time" : 1562766651,
     "userid" : "XuJinSheng",
     "external_userid" : "wmeDKaCQAAIQ_p7ACnxksfeBJSGocAAA",
	 "agree_status":"Disagree"
    },
	{
     "status_change_time" : 1562766651,
     "userid" : "XuJinSheng",
     "external_userid" : "wmeDKaCwAAIQ_p7ACnxckLBBJSGocAAA",
	 "agree_status":"Agree"
    }
    ]
}
```
