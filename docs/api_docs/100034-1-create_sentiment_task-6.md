# 创建情感分析任务

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100034](https://developer.work.weixin.qq.com/document/path/100034)
- **文档 ID**: `100034`
- **API 名称**: `create_sentiment_task`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/create_sentiment_task`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

通过SDK调用，创建情感分析任务。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| msg_list | object[] | 是 | 消息列表，每次最多1000个。 |
| msg_list[].msgid | string | 是 | 每条消息对应的msgid。多次出现同一个msgid，以首次出现的为准。目前支持文本、语音、音频存档消息 |
| msg_list[].encrypt_info.secret_key | string | 是 | 该消息的密钥，将encrypted_secret_key用RSA私钥解密后得到 |

### 请求示例

```json
{
    "msg_list":[
        {
            "msgid": "MSGID1",
            "encrypt_info":{
                "secret_key": "SECRETKEY1"
            }
        },
        {
            "msgid": "MSGID2",
            "encrypt_info":{
                "secret_key": "SECRETKEY2"
            }
        }
    ]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 错误码 |
| errmsg | string | 错误信息 |
| jobid | string | 任务id。首次提交时返回 |
| fail_list | object[] | 提交出错的消息列表，只有msgid重复项返回至该列表 |
| fail_list[].errcode | int32 | 错误码 |
| fail_list[].errmsg | string | 错误码说明 |
| fail_list[].msgid | string | 每条消息对应的msgid，与入参对应 |
| fail_list[].encrypt_info | object | 每条消息对应的加密信息，与入参对应 |

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
