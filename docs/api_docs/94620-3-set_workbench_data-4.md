# 设置应用在用户工作台展示的数据

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/94620](https://developer.work.weixin.qq.com/document/path/94620)
- **文档 ID**: `94620`
- **API 名称**: `set_workbench_data`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/agent/set_workbench_data?access_token=ACCESS_TOKEN`
- **分组信息**: 第 3 个接口，共 4 个

## 接口描述

设置应用在用户工作台展示的数据

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| agentid | uint32 | 是 | 应用id |
| userid | string | 是 | 需要设置的用户的userid |
| type | string | 是 | 模版类型，支持 'keydata', 'image', 'list', 'webview' |
| keydata | object | 否 | 关键数据型模版数据 |
| image | object | 否 | 图片型模版数据 |
| list | object | 否 | 列表型模版数据 |
| webview | object | 否 | webview型模版数据 |

### 请求示例

```json
{
    "agentid":1000005,
    "userid":"test",
    "type":"keydata",
    "keydata":{
        "items":[
            {
                "key":"待审批",
                "data":"2",
                "jump_url":"http://www.qq.com"
            }
        ]
    }
}
```
