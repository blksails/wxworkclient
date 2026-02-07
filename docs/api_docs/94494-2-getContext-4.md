# getContext

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/94494](https://developer.work.weixin.qq.com/document/path/94494)
- **文档 ID**: `94494`
- **API 名称**: `getContext`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

用户进入网页时，网页通过oauth2可获得用户的userid（第三方应用可获得open_userid）。调用getShareInfo时，企业微信会将当前用户的userid或open_userid通过curReceiver加密在encryptedData里返回。为了避免encryptedData被重放攻击，我们建议开发者检查curReceiver与oauth2获得的userid（或open_userid）是否一致。

## 请求信息

### 请求示例

```text
wx.qy.getContext ({
  success: function(res) {
    var entry = res.entry; //返回进入小程序的入口类型
	var shareTicket = res.shareTicket;
  }
})
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| entry | string | 返回进入小程序的入口类型 |
| shareTicket | string | 调用getContext时获取到的shareTicket |
