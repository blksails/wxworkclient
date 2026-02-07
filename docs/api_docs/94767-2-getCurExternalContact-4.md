# 获取当前客户userid

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/94767](https://developer.work.weixin.qq.com/document/path/94767)
- **文档 ID**: `94767`
- **API 名称**: `getCurExternalContact`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/getCurExternalContact?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 3 个

## 接口描述

获取当前客户的userid。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 访问令牌 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| entry | string | 入口值，表示从哪个场景进入 |

## 其他说明

### 接口使用说明

接口使用说明详见“wx.qy.getCurExternalContact”，在客服工具栏里调用该接口，自建应用与第三方应用所需的权限有所不同。
