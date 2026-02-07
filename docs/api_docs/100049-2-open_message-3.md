# 会话展示组件

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100049](https://developer.work.weixin.qq.com/document/path/100049)
- **文档 ID**: `100049`
- **API 名称**: `open_message`
- **请求方法**: `GET`
- **接口地址**: `https://open.work.weixin.qq.com/wwopen/js/jwxwork-1.0.0.js`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

展示会话消息内容

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| message-id | string | 是 | 消息 ID |
| secret-key | string | 是 | 消息密钥 |
| highlight-text | string | 否 | 需要高亮的文本 |
| static-highlight-text-list | string[] | 否 | 需要高亮的静态文本列表 |
| highlight-color | string | 否 | 高亮文本的 color |
| display-type | string | 否 | 指定组件的显示模式，默认为 'normal' |

## 其他说明

### 参数说明

展示会话消息内容。

### 参数说明

消息 ID

### 参数说明

消息密钥，对会话记录中的 encrypted_secretkey 字段进行解密得到，参考 encrypt_secretkey 解密方式

### 参数说明

需要高亮的文本，文本会由企业微信后台进行智能分词处理

### 参数说明

需要高亮的静态文本列表，不会进行智能分词处理，如果存在 highlight-text，最终高亮表现以 hightlight-text 为准

### 参数说明

高亮文本的 color，用于自定义高亮文本的字体颜色, e.g. #267EF0

### 参数说明

指定组件的显示模式，默认为 'normal'；如果指定为 'text'，组件将会以文本总结的形式展示会话内容，同时组件的 class 可以对文本的颜色、字体大小等文本相关样式进行自定义处理
