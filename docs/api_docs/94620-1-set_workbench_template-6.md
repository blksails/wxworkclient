# 在管理后台对应用启用工作台自定义展示

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/94620](https://developer.work.weixin.qq.com/document/path/94620)
- **文档 ID**: `94620`
- **API 名称**: `set_workbench_template`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/agent/set_workbench_template?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 4 个

## 接口描述

设置应用在工作台展示的模版

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| agentid | uint32 | 是 | 应用id |
| type | string | 是 | 模版类型，支持的自定义类型包括 'keydata', 'image', 'list', 'webview'. 若设置的type为 'normal', 则相当于从自定义模式切换为普通展示模式 |
| image | object | 否 | 图片型模版数据 |
| replace_user_data | bool | 否 | 是否覆盖用户工作台的数据 |

### 请求示例

```json
{
    "agentid":1000005,
    "type":"image",
    "image":{
        "url":"xxxx",
        "jump_url":"http://www.qq.com"
    },
    "replace_user_data":true
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |

### 响应示例

```json
{
   "errcode":0,
   "errmsg":"ok"
}
```
