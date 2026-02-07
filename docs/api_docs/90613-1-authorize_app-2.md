# 应用授权

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/90613](https://developer.work.weixin.qq.com/document/path/90613)
- **文档 ID**: `90613`
- **API 名称**: `authorize_app`
- **请求方法**: `POST`
- **接口地址**: `https://127.0.0.1/suite/receive`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

企业微信服务器向应用的“指令回调URL”推送授权事件消息。

## 其他说明

### 概述

在发生授权、通讯录变更、ticket变化等事件时，企业微信服务器会向应用的“指令回调URL”推送相应的事件消息。消息结构体将使用创建应用时的EncodingAESKey进行加密（特别注意, 在第三方回调事件中使用加解密算法，receiveid的内容为suiteid），请参考接收消息解析数据包。本章节的回调事件，服务商在收到推送后都必须直接返回字符串 'success'，若返回值不是 'success'，企业微信会把返回内容当作错误信息。各个事件皆假设指令回调URL设置为：https://127.0.0.1/suite/receive。收到的数据包中ToUserName为产生事件的SuiteId，AgentID为空。各个事件的数据包仅是接收的数据包中的Encrypt参数解密后的内容说明。
