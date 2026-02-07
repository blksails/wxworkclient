# 获取应用在工作台展示的模版

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96454](https://developer.work.weixin.qq.com/document/path/96454)
- **文档 ID**: `96454`
- **API 名称**: `get_workbench_template`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/agent/get_workbench_template?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 6 个

## 接口描述

获取应用在工作台展示的模版

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| agentid | uint32 | 是 | 应用id |

### 请求示例

```json
{
    "agentid":1000005
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误描述 |
| type | string | 模版类型 |
| image | object | 图片型模版数据结构 |
| replace_user_data | bool | 是否覆盖用户工作台的数据 |

### 响应示例

```json
{
   "errcode":0,
   "errmsg":"ok",
   "type":"image",
   "image":{
               "url":"xxxx",
               "jump_url":"http://www.qq.com"
      },
      "replace_user_data":true
}
```
