# 授权知识集

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99996](https://developer.work.weixin.qq.com/document/path/99996)
- **文档 ID**: `99996`
- **API 名称**: `auth_knowledge_base`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/auth_knowledge_base`
- **分组信息**: 第 1 个接口，共 4 个

## 接口描述

当企业授权知识集时，企业微信服务器会向该知识集授权应用关联的程序推送消息。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| knowledge_base_id | string | 是 | 知识集ID |
| knowledge_base_name | string | 是 | 知识集名称 |
| timestamp | uint32 | 是 | 授权时间时间戳 |

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
