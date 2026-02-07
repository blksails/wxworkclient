# 获取当前上下游互联群的群ID

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95827](https://developer.work.weixin.qq.com/document/path/95827)
- **文档 ID**: `95827`
- **API 名称**: `getCurCorpGroupChat`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

获取当前上下游互联群的群ID

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| object | object | 否 | 参数对象 |
| object.success | Function | 否 | 接口调用成功的回调函数 |
| object.fail | Function | 否 | 接口调用失败的回调函数 |
| object.complete | Function | 否 | 接口调用结束的回调函数 |

### 请求示例

```text
wx.qy.getCurCorpGroupChat ({
  success: function(res) {
    chatId  = res.chatId ; //返回当前互联群的群聊ID
  }
})
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| res | object | 返回结果对象 |
| res.chatId | String | 返回当前互联群的群聊ID |
