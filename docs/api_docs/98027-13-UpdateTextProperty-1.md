# 参数详细说明

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98027](https://developer.work.weixin.qq.com/document/path/98027)
- **文档 ID**: `98027`
- **API 名称**: `UpdateTextProperty`
- **分组信息**: 第 13 个接口，共 13 个

## 接口描述

更新指定范围的文本属性

## 请求信息

### 请求示例

```json
{
	"text_property": {},
	"ranges": []
}
```

## 其他说明

### 字段说明

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| text_property | object(TextProperty) | 文本属性 |
| ranges | object[](Range) | 更新文本属性的范围，ranges个数不超过10 |
