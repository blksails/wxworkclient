# 在管理后台对应用启用工作台自定义展示

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/94620](https://developer.work.weixin.qq.com/document/path/94620)
- **文档 ID**: `94620`
- **API 名称**: `set_workbench_template`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/agent/set_workbench_template?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 5 个

## 接口描述

设置应用在工作台展示的模版

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| agentid | uint32 | 是 | 应用id |
| type | string | 是 | 模版类型，支持的类型包括 keydata、image、list、webview。若为 normal，则切换为普通展示模式 |
| keydata | object | 否 | 关键数据型模版数据结构 |
| image | object | 否 | 图片型模版数据结构 |
| list | object | 否 | 列表型模版数据结构 |
| webview | object | 否 | webview型模版数据结构 |
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

### 响应示例

```json
{
   "errcode":0,
   "errmsg":"ok"
}
```
