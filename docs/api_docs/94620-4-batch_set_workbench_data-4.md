# 批量设置应用在用户工作台展示的数据

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/94620](https://developer.work.weixin.qq.com/document/path/94620)
- **文档 ID**: `94620`
- **API 名称**: `batch_set_workbench_data`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/agent/batch_set_workbench_data?access_token=ACCESS_TOKEN`
- **分组信息**: 第 4 个接口，共 4 个

## 接口描述

批量设置应用在用户工作台展示的数据

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| agentid | uint32 | 是 | 应用id |
| userid_list | string[] | 是 | 需要设置的用户userid列表，最多1000个 |
| data | object | 是 | 用户设置的数据 |

### 请求示例

```json
{
    "agentid": 1000005,
	"userid_list":["userid1","userid2"],
    "data": {
        "type": "keydata",
        "keydata": {
            "items": [
                {
                    "key": "待审批",
                    "data": "0",
                    "jump_url": "http://www.qq.com"
                }
            ]
        }
    }
}
```
