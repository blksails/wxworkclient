# 开启网页授权登录

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98173](https://developer.work.weixin.qq.com/document/path/98173)
- **文档 ID**: `98173`
- **API 名称**: `enable_web_authorization_login`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

登录 企业管理端后台->进入需要开启的自建应用->点击 “企业微信授权登录”，进入如下页面 然后点击 "设置授权回调域"，输入回调域名，点击“保存”。

## 其他说明

### 要求配置的授权回调域，必须与访问链接的域名完全一致

假定重定向访问的链接是：http://mail.qq.com:8080/cgi-bin/login：

| 配置域名 | 是否正确 | 原因 |
| --- | --- | --- |
| mail.qq.com:8080 | ![correct](http://p.qpic.cn/pic_wework/1321807788/0d0bec01471d7e0d428687460b796c3bf039550acc3a25a0/0) | 配置域名与访问域名完全一致 |
| email.qq.com | ![error](http://p.qpic.cn/pic_wework/743967770/f8fe19f41e87ec0691b75a3a9512e1f7a4b61ea8c39933a5/0) | 配置域名必须与访问域名完全一致 |
| support.mail.qq.com | ![error](http://p.qpic.cn/pic_wework/743967770/f8fe19f41e87ec0691b75a3a9512e1f7a4b61ea8c39933a5/0) | 配置域名必须与访问域名完全一致 |
| *.qq.com | ![error](http://p.qpic.cn/pic_wework/743967770/f8fe19f41e87ec0691b75a3a9512e1f7a4b61ea8c39933a5/0) | 不支持泛域名设置 |
| mail.qq.com | ![error](http://p.qpic.cn/pic_wework/743967770/f8fe19f41e87ec0691b75a3a9512e1f7a4b61ea8c39933a5/0) | 配置域名必须与访问域名完全一致，包括端口号 |
| http://mail.qq.com:8080 | ![error](http://p.qpic.cn/pic_wework/743967770/f8fe19f41e87ec0691b75a3a9512e1f7a4b61ea8c39933a5/0) | 不包括协议头 |
