# 获取客户群进群方式配置

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99547](https://developer.work.weixin.qq.com/document/path/99547)
- **文档 ID**: `99547`
- **API 名称**: `get_join_way`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/groupchat/get_join_way`
- **分组信息**: 第 2 个接口，共 4 个

## 接口描述

获取企业配置的群二维码或小程序按钮

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| config_id | string | 是 | 联系方式的配置id |

### 请求示例

```json
{
    "config_id":"9ad7fa5cdaa6511298498f979c472aaa"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| join_way | object | 配置详情 |
