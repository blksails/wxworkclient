# 参数详细说明

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98027](https://developer.work.weixin.qq.com/document/path/98027)
- **文档 ID**: `98027`
- **API 名称**: `InsertTable`
- **分组信息**: 第 10 个接口，共 13 个

## 接口描述

在指定位置插入表格，表格大小限制：
- 行数<=100
- 列数<=60
- 单元格总数<=1000

## 其他说明

### 字段说明

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| rows | uint32 | 表格行数 |
| cols | uint32 | 表格列数 |
| location | object(Location) | 插入的位置 |
