# 参数详细说明

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98027](https://developer.work.weixin.qq.com/document/path/98027)
- **文档 ID**: `98027`
- **API 名称**: `UpdateRequest`
- **分组信息**: 第 2 个接口，共 13 个

## 接口描述

更新文档的操作，每个UpdateRequest的Object中能同时填一个字段，填入多个的只会有一个生效

## 请求信息

### 请求示例

```json
{
	"replace_text": {},
	"delete_content": {}
}
```

## 其他说明

### 字段说明

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| replace_text | object(ReplaceText) | 替换指定位置文本内容 |
| insert_text | object(InsertText) | 在指定位置插入文本内容 |
| delete_content | object(DeleteContent) | 删除指定位置内容 |
| insert_image | object(InsertImage) | 在指定位置插入图片 |
| insert_page_break | object(InsertPageBreak) | 在指定位置插入分页符 |
| insert_table | object(InsertTable) | 在指定位置插入表格 |
| insert_paragraph | object(InsertParagraph) | 在指定位置插入段落 |
| update_text_property | object(UpdateTextProperty) | 更新指定位置文本属性 |
