# 如何接入

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100008](https://developer.work.weixin.qq.com/document/path/100008)
- **文档 ID**: `100008`
- **API 名称**: `upload_model_program`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/upload_model_program?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 13 个

## 接口描述

在数据与智能专区中上传服务商的模型/程序。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| path | string | 是 | 上传路径 |

### 请求示例

```json
{
  "path": "桌面端服务商助手 - 工具 - 数据与智能专区"
}
```

## 其他说明

### 提示

「数据与智能专区」能力当前灰度开放，若服务商有匹配的应用场景，且希望加入灰度范围，可在页面底部扫码添加企业微信产品客服进行申请。
