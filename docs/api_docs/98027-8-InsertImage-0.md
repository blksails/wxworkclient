# 参数详细说明

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98027](https://developer.work.weixin.qq.com/document/path/98027)
- **文档 ID**: `98027`
- **API 名称**: `InsertImage`
- **分组信息**: 第 8 个接口，共 13 个

## 接口描述

插入图片

## 其他说明

### 字段说明

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| image_id | string | 图片url，通过上传图片接口获得 |
| location | object(Location) | 插入的位置 |
| width | uint32 | 图片的宽，单位是像素（px） |
| height | uint32 | 图片的高， 单位是像素（px） |
