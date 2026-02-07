# 获取任务创建结果

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95095](https://developer.work.weixin.qq.com/document/path/95095)
- **文档 ID**: `95095`
- **API 名称**: `get_moment_task_result`
- **请求方法**: `GET`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_moment_task_result`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

由于发表任务的创建是异步执行的，应用需要再调用该接口以获取创建的结果。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |
| jobid | string | 是 | 异步任务id，最大长度为64字节，由创建发表内容到客户朋友圈任务接口获取 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| status | int32 | 任务状态，整型，1表示开始创建任务，2表示正在创建任务中，3表示创建任务已完成 |
| type | string | 操作类型，字节串，此处固定为add_moment_task |
| result | object | 详细的处理结果。当任务完成后此字段有效 |
| result.errcode | int32 | 返回码 |
| result.errmsg | string | 对返回码的文本描述内容 |
| result.moment_id | string | 朋友圈id，可通过获取客户朋友圈企业发表的列表接口获取朋友圈企业发表的列表 |
| result.invalid_sender_list | object | 不合法的执行者列表，包括不存在的id以及不在应用可见范围内的部门或者成员 |
| result.invalid_sender_list.user_list | array | 不合法的执行者用户列表 |
| result.invalid_sender_list.department_list | array | 不合法的执行者部门列表 |
| result.invalid_external_contact_list | object | 不合法的客户列表 |
| result.invalid_external_contact_list.tag_list | array | 不合法的客户标签列表 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
    "status": 1,
    "type": "add_moment_task",
	"result": {
		"errcode":0,
		"errmsg":"ok",
		"moment_id":"xxxx",
		"invalid_sender_list":{
			"user_list":["zhangshan","lisi"],
			"department_list":[2,3]
		},
		"invalid_external_contact_list":{
			"tag_list":["xxx"]
		}
	}
}
```
