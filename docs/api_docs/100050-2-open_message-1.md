# 会话展示组件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100050](https://developer.work.weixin.qq.com/document/path/100050)
- **文档 ID**: `100050`
- **API 名称**: `open_message`
- **分组信息**: 第 2 个接口，共 7 个

## 接口描述

展示会话消息内容

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| message-id | string | 是 | 消息 ID |
| secret-key | string | 是 | 消息密钥，对会话记录中的 encrypted_secretkey 字段进行解密得到 |
| highlight-text | string | 否 | 需要高亮的文本 |
| static-highlight-text-list | string[] | 否 | 需要高亮的静态文本列表 |
| highlight-color | string | 否 | 高亮文本的 color，用于自定义高亮文本的字体颜色 |
| display-type | string | 否 | 指定组件的显示模式，默认为 "normal"；如果指定为 "text"，组件将会以文本总结的形式展示会话内容 |
