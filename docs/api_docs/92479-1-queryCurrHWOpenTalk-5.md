# 查询当前是否在视频会议

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/92479](https://developer.work.weixin.qq.com/document/path/92479)
- **文档 ID**: `92479`
- **API 名称**: `queryCurrHWOpenTalk`
- **请求方法**: `POST`
- **接口地址**: `wx.qy.queryCurrHWOpenTalk`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

此接口在企业微信2.7.0及以后版本支持

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| object | object | 是 | 参数对象 |
| object.success | function | 否 | 接口调用成功的回调函数 |
| object.fail | function | 否 | 接口调用失败的回调函数 |
| object.complete | function | 否 | 接口调用结束的回调函数 |

### 请求示例

```text
wx.qy.queryCurrHWOpenTalk({
  success: (res) => {
      if (res.inTalkType != "None") {
            // busy
          if (res.inTalkType == "HWOpenTalk") {
                //res.ticket
          }
      }
  },
  fail: (res) => {
    console.log(JSON.stringify(res))
  }
})
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| res.inTalkType | String | 当前通话的类型，取值为None/HWOpenTalk/VoIP/SystemCall |
| res.ticket | string | 当前会议码票据（仅在视频会议中返回） |
