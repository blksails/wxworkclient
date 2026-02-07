# 获取「分享到朋友圈」按钮点击状态并自定义分享内容

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100758](https://developer.work.weixin.qq.com/document/path/100758)
- **文档 ID**: `100758`
- **API 名称**: `onMenuShareTimeline`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

获取「分享到朋友圈」按钮点击状态并自定义分享内容。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| title | string | 否 | 分享标题 |
| link | string | 否 | 分享链接  在微信上分享时，该链接的域名必须与企业某个应用的可信域名一致 |
| imgUrl | string | 否 | 分享图标 |
| enableIdTrans | number | 否 | 企业微信 4.0.20 是否开启id转译, 1 为开启，0 为关闭，默认为0 仅供第三方应用使用 必须使用应用身份进行注册 |
| type | string | 否 |  |
| dataUrl | string | 否 |  |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| cancel | Function | 否 | 取消回调 |
| complete | Function | 否 | 完成回调 |

### 请求示例

```json
ww.onMenuShareTimeline({
  title: '企业微信',
  link: 'https://work.weixin.qq.com/',
  imgUrl: 'https://res.mail.qq.com/node/ww/wwmng/style/images/index_share_logo$13c64306.png',
  success() {
    // 用户确认分享后回调
  },
  cancel() {
    // 用户取消分享后回调
  }
})
```

## 其他说明

### 使用说明

微信客户端即将废弃该接口。
