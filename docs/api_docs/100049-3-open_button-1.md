# 会话展示组件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100049](https://developer.work.weixin.qq.com/document/path/100049)
- **文档 ID**: `100049`
- **API 名称**: `open_button`
- **分组信息**: 第 3 个接口，共 7 个

## 接口描述

业务授权按钮

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| open-type | string | 是 | 业务类型：`getExportCode` |

## 其他说明

### 事件说明

| 事件名称 | 说明 | event.detail |
| --- | --- | --- |
| bindgetexportcode | open-type 为 `getExportCode` 时，用户点击后，会触发回调 | `{ exportCode }` |
