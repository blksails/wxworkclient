# 微信小程序进入直播间

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/93721](https://developer.work.weixin.qq.com/document/path/93721)
- **文档 ID**: `93721`
- **API 名称**: `mini_program_enter_live_room`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

获取到直播living_code之后，在微信小程序里可调用小程序接口wx.navigateToMiniProgram，唤起直播小程序，进入直播或直播回放页.

## 请求信息

### 请求示例

```javascript
wx.navigateToMiniProgram({
  appId: 'wx7424030d69bde86e',
  path: 'pages/watch/index?living_code=LIVING_CODE',
  success(res) {
    // 打开成功
  }
})
```

## 其他说明

### 请求参数

| 参数 | 必须 | 说明 |
| --- | --- | --- |
| appId | 是 | 固定填企业微信直播小程序appid: wx7424030d69bde86e |
| path | 是 | 跳转到直播小程序的路径，支持两种路径如下：   (1) 跳到直播间，固定为：pages/watch/index?living_code=LIVING_CODE，  (2) 跳到回放页，固定为：pages/watch/index?living_code=LIVING_CODE&replay=1,  其中LIVING_CODE为上文中“获取微信观看直播凭证”接口所获取 |
