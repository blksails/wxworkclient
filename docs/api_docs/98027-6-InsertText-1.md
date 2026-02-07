# 参数详细说明

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98027](https://developer.work.weixin.qq.com/document/path/98027)
- **文档 ID**: `98027`
- **API 名称**: `InsertText`
- **分组信息**: 第 6 个接口，共 13 个

## 接口描述

插入文本

## 请求信息

### 请求示例

```json
{
	"text": "hello world",
	"location": {
		"index": 10
	}
}
```

## 其他说明

### 字段说明

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| text | string | 要插入的文本 |
| location | object(Location) | 插入的位置 |
