# 引导企业授权接入

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99482](https://developer.work.weixin.qq.com/document/path/99482)
- **文档 ID**: `99482`
- **API 名称**: `get_log_level`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/get_log_level?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

申请通过并发布组件后，你可获得专属的组件授权链接/二维码。可在你的业务页面配置该链接，企业点击后将自动打开企业微信，授权在你的场景中接入获客助手，你可获得改场景中的获客转化数据。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 访问令牌 |
