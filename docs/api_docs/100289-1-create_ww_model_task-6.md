# 创建企微通用模型任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100289](https://developer.work.weixin.qq.com/document/path/100289)
- **文档 ID**: `100289`
- **API 名称**: `create_ww_model_task`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/create_ww_model_task`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

应用在专区中的程序可调用本接口传入会话内容，使用企业微信通用的大语言模型进行会话分析。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ability_id | string | 是 | 模型能力id |
| tag_group_list[].group_id | string | 否 | 客户标签组列表 |
| kb_id | string | 否 | 知识集id |
| kb_retrieval_words | string | 否 | 用于从知识集中检索相关内容 |
| msg_list[].msgid | string | 否 | 每条消息对应的msgid |
| msg_list[].encrypt_info.secret_key | string | 否 | 该消息的密钥 |
| model_id | string | 否 | 调用的模型id |
| need_think_result | bool | 否 | 是否返回模型的思考过程部分 |
| var_args[].name | string | 否 | 自定义变量名 |
| var_args[].value | string | 否 | 自定义变量值 |

### 请求示例

```json
{
	"ability_id": "ABILITY_ID",
	"tag_group_list": [{
		"group_id": "GROUP_ID1"
	},{
		"group_id": "GROUP_ID2"
	}],
	"kb_id": "KBID",
	"kb_retrieval_words": "KB_RECALL_STRING",
	"msg_list": [{
		"msgid": "MSGID1",
		"encrypt_info": {
			"secret_key": "SECRETKEY1"
		}
	},{
		"msgid": "MSGID2",
		"encrypt_info": {
			"secret_key": "SECRETKEY2"
		}
	}],
	"model_id": "MODEL_ID",
	"need_think_result": false,
	"var_args": [{
		"name": "VAR_ARGS_NAME1",
		"value": "VAR_ARGS_VALUE1"
	},{
		"name": "VAR_ARGS_NAME2",
		"value": "VAR_ARGS_VALUE2"
	}]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
| jobid | string | 任务id |
| fail_list | object[] | 提交出错的消息列表 |

### 响应示例

```json
{
    "errcode": 0,
    "errmsg": "ok",
    "jobid": "JOBID",
    "fail_list":[
        {
            "errcode": 710601,
            "errmsg": "xxx",
            "msgid": "MSGID2",
            "encrypt_info":{
                "secret_key": "SECRETKEY2"
            }
        }
    ]
}
```
