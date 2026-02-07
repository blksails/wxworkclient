# 微信H5页面进入直播间

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/93721](https://developer.work.weixin.qq.com/document/path/93721)
- **文档 ID**: `93721`
- **API 名称**: `h5_enter_live_room`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

获取到直播living_code之后，在微信H5页面里可使用微信开放标签<wx-open-launch-weapp>，唤起直播小程序，进入直播或直播回放页.

## 请求信息

### 请求示例

```html
<wx-open-launch-weapp
  id="launch-btn"
  username="gh_25e071b83ee0"
  path="pages/watch/index?living_code=LIVING_CODE">
  <template>
    <style>.btn { padding: 12px }</style>
    <button class="btn">进入直播间</button>
  </template>
</wx-open-launch-weapp>
<script>
  var btn = document.getElementById('launch-btn');
  btn.addEventListener('launch', function (e) {
    console.log('success');
  });
  btn.addEventListener('error', function (e) {
    console.log('fail', e.detail);
  });
</script>
```

## 其他说明

### 开放标签参数

| 参数 | 必须 | 说明 |
| --- | --- | --- |
| username | 是 | 固定填企业微信直播小程序原始id: gh_25e071b83ee0 |
| path | 是 | 跳转到直播小程序的路径，支持两种路径如下：   (1) 跳到直播间，固定为：pages/watch/index?living_code=LIVING_CODE，  (2) 跳到回放页，固定为：pages/watch/index?living_code=LIVING_CODE&replay=1,  其中LIVING_CODE为上文中“获取微信观看直播凭证”接口所获取 |
