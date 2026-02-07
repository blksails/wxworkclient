# 使用OAuth2前须知

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/91860](https://developer.work.weixin.qq.com/document/path/91860)
- **文档 ID**: `91860`
- **API 名称**: `oauth2_preparation`
- **分组信息**: 第 3 个接口，共 3 个

## 其他说明

### 关于网页授权的可信域名

REDIRECT_URL中的域名，需要先配置至应用的“可信域名”，否则跳转时会提示“redirect_uri参数错误”。要求配置的可信域名，必须与访问链接的域名完全一致。

### 关于UserID机制

UserId用于在一个企业内唯一标识一个用户，通过网页授权接口可以获取到当前用户的UserId信息，如果需要获取用户的更多信息可以调用 通讯录管理 - 成员接口 来获取。

### 静默授权与手动授权

静默授权：用户点击链接后，页面直接302跳转至 redirect_uri?code=CODE&state=STATE
手动授权：用户点击链接后，会弹出一个中间页，让用户选择是否授权，用户确认授权后再302跳转至 redirect_uri?code=CODE&state=STATE

### 缓存方案建议

通过OAuth2.0验证接口获取成员身份会有一定的时间开销。对于频繁获取成员身份的场景，建议采用如下方案：
1、企业应用中的URL链接直接填写企业自己的页面地址
2、成员操作跳转到步骤1的企业页面时，企业后台校验是否有标识成员身份的cookie信息，此cookie由企业生成
3、如果没有匹配的cookie，则重定向到OAuth验证链接，获取成员的身份信息后，由企业后台植入标识成员身份的cookie信息
4、根据cookie获取成员身份后，再进入相应的页面
