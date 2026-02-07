# 拉起电子发票列表

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/90526](https://developer.work.weixin.qq.com/document/path/90526)
- **文档 ID**: `90526`
- **API 名称**: `chooseInvoice`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

拉起电子发票列表。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| params.timestamp | number | 是 | 签名时间戳 |
| params.nonceStr | string | 是 | 签名随机串 |
| params.cardSign | string | 是 | 签名 |
| params.signType | string | 否 | 签名类型 |
| params.success | Function | 否 | 成功回调 |
| params.fail | Function | 否 | 失败回调 |
| params.cancel | Function | 否 | 取消回调 |
| params.complete | Function | 否 | 完成回调 |

### 请求示例

```text
ww.chooseInvoice({
  timestamp: timestamp,
  nonceStr: nonceStr,
  signType: signType,
  cardSign: cardSign
})
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errMsg | string | 通用错误信息 |
| errCode | number | 通用错误码 |
| choose_invoice_info | Object[] | 用户选中的发票列表 |
| choose_invoice_info[].card_id | string |  |
| choose_invoice_info[].encrypt_code | string |  |
| choose_invoice_info[].app_id | string |  |
