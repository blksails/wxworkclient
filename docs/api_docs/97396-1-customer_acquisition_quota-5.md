# 查询剩余使用量

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97396](https://developer.work.weixin.qq.com/document/path/97396)
- **文档 ID**: `97396`
- **API 名称**: `customer_acquisition_quota`
- **请求方法**: `GET`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/customer_acquisition_quota?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

企业可通过此接口查询当前剩余的使用量。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |
| total | uint32 | 历史累计使用量 |
| balance | uint32 | 剩余使用量 |
| quota_list | object[] | 额度列表 |
| quota_list[].expire_date | uint32 | 额度过期时间戳，为过期日的零点，实际过期时间取决于额度的购买时间 |
| quota_list[].balance | uint32 | 即将过期额度数量 |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok",
   "total":1000,
   "balance":500,
   "quota_list":
   [
      {
         "expire_date":1689350400,
         "balance":200
      },
      {
         "expire_date":1692028800,
         "balance":300
      }
   ]
}
```
