# 在管理后台对应用启用工作台自定义展示

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96454](https://developer.work.weixin.qq.com/document/path/96454)
- **文档 ID**: `96454`
- **API 名称**: `set_workbench_template`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/agent/set_workbench_template?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 6 个

## 接口描述

该接口指定应用自定义模版类型。同时也支持设置企业默认模版数据。若type指定为 'normal' 则为取消自定义模式，改为普通展示模式

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| agentid | uint32 | 是 | 应用id |
| type | string | 是 | 模版类型，目前支持的自定义类型包括 'keydata'、 'image'、 'list'、 'webview'. 若设置的type为 'normal', 则相当于从自定义模式切换为普通宫格或者列表展示模式 |
| keydata | object | 否 | 关键数据型模版数据结构 |
| image | object | 否 | 图片型模版数据结构 |
| list | object | 否 | 列表型模版数据结构 |
| webview | object | 否 | webview型模版数据结构 |
| replace_user_data | bool | 否 | 是否覆盖用户工作台的数据。设置为true的时候，会覆盖企业所有用户当前设置的数据。若设置为false, 则不会覆盖用户当前设置的所有数据。默认为false |

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
| errmsg | string | 错误描述 |

### 响应示例

```json
{
   "errcode":0,
   "errmsg":"ok"
}
```
