# 随机字符串生成算法

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98768](https://developer.work.weixin.qq.com/document/path/98768)
- **文档 ID**: `98768`
- **API 名称**: `random_string_algorithm`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

部分API接口协议中包含字段nonce_str，主要保证签名不可预测及防重放攻击。我们推荐生成随机字符串算法如下：调用随机数函数生成，将得到的值转换为字符串。
