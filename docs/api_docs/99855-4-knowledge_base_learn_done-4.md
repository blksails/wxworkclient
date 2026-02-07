# 內容学习完成(每个內容学习完成都会回调一次)

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99855](https://developer.work.weixin.qq.com/document/path/99855)
- **文档 ID**: `99855`
- **API 名称**: `knowledge_base_learn_done`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/knowledge_base_learn_done`
- **分组信息**: 第 4 个接口，共 4 个

## 接口描述

当每个內容学习完成时，企业微信服务器会向该知识集授权应用关联的程序推送消息。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| event_type | string | 是 | 事件类型，固定为：`knowledge_base_learn_done` |
| timestamp | uint32 | 是 | 删除知识集时间戳 |
| knowledge_base_id | string | 是 | 知识集ID |
| knowledge_base_name | string | 是 | 知识集名称 |
| doc_id | int32 | 是 | 內容ID |
| learn_status | int32 | 是 | 学习状态。0-学习成功；1-学习失败 |

### 请求示例

```json
{
	"event_type": "knowledge_base_learn_done",
	"timestamp": 1408091189,
	"knowledge_base_learn_done": {
		"knowledge_base_id": "xxxxxxx",
		"knowledge_base_name": "zzzzz",
		"doc_id" : 1,
		"learn_status" : 0
	}
}
```
