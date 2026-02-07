# 企业员工userid的升级方案

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96516](https://developer.work.weixin.qq.com/document/path/96516)
- **文档 ID**: `96516`
- **API 名称**: `userid_to_openuserid`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/batch/userid_to_openuserid?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 4 个

## 接口描述

将自建应用获取的userid转换为第三方应用获取的userid

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userid_list | string[] | 是 | 获取到的成员ID列表，最多不超过1000个 |

### 请求示例

```json
{
  "userid_list":["aaa", "bbb"]
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| open_userid_list | object[] | 该服务商第三方应用下的成员ID |
| open_userid_list.userid | string | 转换成功的userid |
| open_userid_list.open_userid | string | 转换成功的userid对应的该服务商应用下的成员ID |
| invalid_userid_list | string[] | 转换失败的userid列表 |

### 响应示例

```json
{
 "errcode": 0,
 "errmsg": "",
 "open_userid_list": [
     {
         "userid": "aaa",
         "open_userid": "sdflajsldjflad"
     }
 ],
 "invalid_userid_list":["bbb"]
}
```
