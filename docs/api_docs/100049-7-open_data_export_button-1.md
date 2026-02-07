# 会话展示组件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100049](https://developer.work.weixin.qq.com/document/path/100049)
- **文档 ID**: `100049`
- **API 名称**: `open_data_export_button`
- **分组信息**: 第 7 个接口，共 7 个

## 接口描述

导出 包含人名部门名的文件

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| href | string | 是 | 文件下载 url |

## 其他说明

### 模板示例

```<ww-open-data-export-button
	class="export-button"
	href="{{data.fileUrl}}"
	binderror="onExportError"
>
	点击下载文件
</ww-open-data-export-button>
```
