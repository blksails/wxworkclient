# getShareInfo

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/94494](https://developer.work.weixin.qq.com/document/path/94494)
- **文档 ID**: `94494`
- **API 名称**: `getShareInfo`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

企业微信的shareticket属性不支持同步到微信，当shareticket消息分享到包含微信用户的会话中，用户在微信打开时是没法获取到shareticket的。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| shareTicket | string | 是 | 调用getContext时获取到的shareTicket |

### 请求示例

```text
wx.qy.getShareInfo ({
  shareTicket:"xxxx",
  success: function(res) {
    var encryptedData = res.encryptedData; //转发信息的加密数据
	var iv = res.iv; //加密算法的初始向量
  }
})
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| encryptedData | string | 转发信息的加密数据 |
| iv | string | 加密算法的初始向量 |
