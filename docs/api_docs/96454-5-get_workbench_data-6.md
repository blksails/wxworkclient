# 获取应用在用户工作台展示的数据

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96454](https://developer.work.weixin.qq.com/document/path/96454)
- **文档 ID**: `96454`
- **API 名称**: `get_workbench_data`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/agent/get_workbench_data?access_token=ACCESS_TOKEN`
- **分组信息**: 第 5 个接口，共 6 个

## 接口描述

获取应用在用户工作台展示的数据

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| agentid | uint32 | 是 | 应用id |
| userid | string | 是 | 用户userid |

### 请求示例

```json
{
    "agentid": 1000005,
    "userid": "userid1"
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误描述 |
| data | object | 用户设置的数据列表，具体的结构参考UserData结构说明 |

### 响应示例

```json
{
    "errcode": 0,
	"errmsg":"ok",
    "data": {
        "type": "keydata",
        "keydata": {
            "items": [
                {
                    "key": "待审批",
                    "data": "2",
                    "jump_url": "http://www.qq.com/"
                },
                {
                    "key": "带批阅作业",
                    "data": "4",
                    "jump_url": "http://www.qq.com"
                },
                {
                    "key": "成绩录入",
                    "data": "45",
                    "jump_url": "http://www.qq.com"
                },
                {
                    "key": "综合评价",
                    "data": "98",
                    "jump_url": "http://www.qq.com"
                }
            ]
        }
    }
}
```
