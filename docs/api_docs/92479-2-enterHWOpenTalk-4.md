# 加入视频会议

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/92479](https://developer.work.weixin.qq.com/document/path/92479)
- **文档 ID**: `92479`
- **API 名称**: `enterHWOpenTalk`
- **请求方法**: `POST`
- **接口地址**: `wx.qy.enterHWOpenTalk`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

此接口在企业微信2.7.0及以后版本支持。只能加入同企业硬件创建的视频会议

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| object | object | 是 | 参数对象 |
| object.code | String | 是 | 会议码，从对应的视频会议硬件上获取 |
| object.ticket | String | 否 | 会议码票据，调用方可以根据会议码生成对应的会议码票据。此票据会在调用queryCurrHWOpenTalk时返回，便于换回对应的会议码（调用方需要记录票据->会议码的映射关系） |
| object.success | function | 否 | 接口调用成功的回调函数 |
| object.fail | function | 否 | 接口调用失败的回调函数 |
| object.complete | function | 否 | 接口调用结束的回调函数 |

### 请求示例

```text
wx.qy.enterHWOpenTalk({
  code: "",
  ticket: "",
  success: (res) => {
      //发起加入会议请求成功
  },
  fail: (res) => {
    console.log(JSON.stringify(res))
  }
})
```
