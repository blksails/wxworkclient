# 查询链接使用详情

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97396](https://developer.work.weixin.qq.com/document/path/97396)
- **文档 ID**: `97396`
- **API 名称**: `customer_acquisition_statistic`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/customer_acquisition/statistic?access_token=ACCESS_TOKEN`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

企业可通过此接口查询指定获客链接在指定时间范围内的访问情况。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| link_id | string | 是 | 获客链接的id |
| start_time | uint32 | 是 | 统计起始时间戳 |
| end_time | uint32 | 是 | 统计结束时间戳 |

### 请求示例

```json
{
   "link_id":"caxxxxxxx",
   "start_time":1688140800,
   "end_time":1688486400
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| click_link_customer_cnt | uint32 | 点击链接客户数 |
| new_customer_cnt | uint32 | 新增客户数 |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok",
   "click_link_customer_cnt":1000,
   "new_customer_cnt":500
}
```
