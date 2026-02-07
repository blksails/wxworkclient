# 参数详细说明

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98027](https://developer.work.weixin.qq.com/document/path/98027)
- **文档 ID**: `98027`
- **API 名称**: `ReplaceText`
- **分组信息**: 第 5 个接口，共 13 个

## 请求信息

### 请求示例

```json
{
	"text": "hello world",
	"ranges": [
		{
			"start_index": 10,
			"length": 5
		}
	]
}
```

## 其他说明

### 字段说明

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| text | string | 要替换的文本 |
| ranges | object[] | 要替换的文档范围，可同时替换多个位置的文本, rangs个数不超过10。 |
