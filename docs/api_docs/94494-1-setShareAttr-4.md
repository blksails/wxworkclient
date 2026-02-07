# setShareAttr

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/94494](https://developer.work.weixin.qq.com/document/path/94494)
- **文档 ID**: `94494`
- **API 名称**: `setShareAttr`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 1 个接口，共 3 个

## 接口描述

调用setShareAttr时，可以传一个state参数，该参数值由开发者自由指定。shareticket消息分享之后，当接收者打开消息的H5页面或小程序时，开发者调用getShareInfo，企业微信会将state值加密返回，开发者可在后台解密并加以校验。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| withShareTicket | bool | 否 | 默认为false |
| state | string | 否 | 详见[state的作用] |

### 请求示例

```text
wx.qy.setShareAttr ({
    withShareTicket:true,
    state: "STATE",
    success: function(res) {

  }
})
```
