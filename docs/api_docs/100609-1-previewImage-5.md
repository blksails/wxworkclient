# 预览图片

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100609](https://developer.work.weixin.qq.com/document/path/100609)
- **文档 ID**: `100609`
- **API 名称**: `previewImage`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

预览图片

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| params.current | string | 是 | 当前显示图片的链接 |
| params.urls | string[] | 是 | 需要预览的图片链接列表 |
| params.success | Function | 否 | 成功回调 |
| params.fail | Function | 否 | 失败回调 |
| params.cancel | Function | 否 | 取消回调 |
| params.complete | Function | 否 | 完成回调 |

### 请求示例

```text
ww.previewImage({
  current: imgURL,
  urls: [imgURL]
});
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errMsg | string | 通用错误信息 |
| errCode | number | 通用错误码 |

## 其他说明

### 使用说明

从2.4.6版本开始，IOS版企业微信浏览器升级为WkWebView，企业微信原生层面的网络请求读取不到WKWebview中设置的cookie，即使域名是相同的。
**问题说明：**
如果页面的资源或图片存储的服务器依赖校验Cookie来返回数据的情况，在切换到WKWebview后，在企业微信内长按保存，或者点击预览大图时，原生层面发起的网络请求将不会完整地带上所设置的Cookie，会导致图片保存失败或预览失败。
**适配建议**
建议静态资源cookie free。如果确实有信息需要传递，可通过业务后台存储需要传递的信息，然后给页面一个存储信息相对应的access_token加密码，再通过Url中加入自己业务的access_token进行页面间信息传递.
