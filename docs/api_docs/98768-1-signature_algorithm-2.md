# 签名算法

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/98768](https://developer.work.weixin.qq.com/document/path/98768)
- **文档 ID**: `98768`
- **API 名称**: `signature_algorithm`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

为保证调用者不可伪造，数据不可被篡改、重放等，支付相关接口需要做签名处理。

## 其他说明

### 签名生成的通用步骤

第一步，将所有非空参数构造成键值对（即key=value）集合，按照ASCII码从小到大排序（字典序），最后拼接成字符串stringA。以下重要规则：
将“键值对”整体按照ASCII码从小到大排序（字典序）；
如果参数的值为空不参与签名；
传送的sig参数不参与签名，将生成的签名与该sig值作校验；
区分大小写；
接口可能增加字段，验证签名时必须支持增加的扩展字段；

第二步，对stringA以服务商的支付密钥为key进行HMAC-SHA256运算，并进行base64编码，得到sig。
第三步，将计算得到的sig与请求中的sig对比，如果不相同，表示该请求可能被篡改。

### 示例1： (适用于简单JSON结构的API请求)

假设服务商的支付密钥为：
secret = "at23pxnPBNQY3JiA8N5U1gabiQqxZwqH_Gihg7a_wrULmlOPVP-iiRjv9JWYPrDk"

需要POST的参数如下：
{
        "orderid" : "ord7",
        "buyer_corpid": "ww66302cfadbdd3c64",
        "buyer_userid" : "invitetest",
        "product_id": "product_id_xxx",
        "product_name": "product_name_xxx",
        "product_detail": "product_detail_xxx",
        "unit_name": "台",
        "unit_price": 1,
        "num": 3,
        "nonce_str" : "129031823",
        "ts": 1548302135,
        "sig": "mPOwVW/vQ74xN+b+Yu1KMa9RrmhKJaJjAtXHTof+EpU="
}

### 举例2： (适用于复杂JSON结构的API请求)

如果节点是元组，那么不直接参与签名，而是递归地用其子节点进行签名。假设需要POST的参数如下：
{
	"orderid": "i3khJ4dMv3",
	"order_type": 1,
	"credit_order_list": [...],
	"appid": 2,
	"buyer_corpid": "wwfedd7e5292d63a35",
	"buyer_userid": "zhangsan",
	"product_id": "xxxxxxxxxxx",
	"product_name": "xxxxxxxxxxxxx",
	"product_detail": "xxxxxxxxxxxx",
	"unit_name": "台",
	"nonce_str": "1287319372",
	"ts": 1547719184,
	"sig": "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
