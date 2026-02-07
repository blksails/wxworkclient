# 授权知识集

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100046](https://developer.work.weixin.qq.com/document/path/100046)
- **文档 ID**: `100046`
- **API 名称**: `auth_knowledge_base`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/webhook/callback`
- **分组信息**: 第 1 个接口，共 4 个

## 接口描述

企业授权知识集时，企业微信服务器向知识集授权应用关联的程序推送消息。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| event_type | string | 是 | 事件类型，固定为：`auth_knowledge_base` |
| knowledge_base_id | string | 是 | 知识集ID |
| knowledge_base_name | string | 是 | 知识集名称 |
| timestamp | int32 | 是 | 授权时间时间戳 |

### 请求示例

```json
{
    "event_type": "auth_knowledge_base",
    "timestamp": 1408091189,
    "auth_knowledge_base": {
        "knowledge_base_id": "xxxxxxx",
        "knowledge_base_name": "zzzzz"
    }
}
```
