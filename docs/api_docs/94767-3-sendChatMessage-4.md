# 分享消息到当前会话

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/94767](https://developer.work.weixin.qq.com/document/path/94767)
- **文档 ID**: `94767`
- **API 名称**: `sendChatMessage`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/sendChatMessage?access_token=ACCESS_TOKEN`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

分享消息到当前会话，支持不同类型的消息。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 访问令牌 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| msgtype | string | 是 | 消息类型 |
| enterChat | Boolean | 否 | 是否进入会话 |
| msgmenu.head_content | string | 否 | 起始文本 |
| msgmenu.list[].type | string | 是 | 菜单类型 |
| msgmenu.list[].click.id | string | 否 | 菜单ID |
| msgmenu.list[].click.content | string | 是 | 菜单显示内容 |
| msgmenu.list[].view.url | string | 是 | 跳转链接 |
| msgmenu.list[].view.content | string | 是 | 菜单显示内容 |
| msgmenu.list[].miniprogram.appid | string | 是 | 小程序appid |
| msgmenu.list[].miniprogram.page | string | 是 | 小程序路径 |
| msgmenu.list[].miniprogram.content | string | 是 | 菜单显示内容 |
| msgmenu.tail_content | string | 否 | 结束文本 |
| channelsShopProduct.productId | string | 是 | 商品ID |
| channelsShopProduct.shopAppId | string | 是 | 小店ID |
| channelsShopProduct.imgUrl | string | 是 | 商品图像 |
| channelsShopProduct.title | string | 是 | 商品名称 |
| channelsShopProduct.sellingPrice | string | 是 | 价格区间最小值 |
| channelsShopProduct.shopImgUrl | string | 是 | 店铺头像URL |
| channelsShopProduct.shopNickname | string | 是 | 店铺名称 |
| success | Function | 否 | 成功回调函数 |
| fail | Function | 否 | 失败回调函数 |
| complete | Function | 否 | 结束回调函数 |

### 请求示例

```text
wx.qy.sendChatMessage({
    msgtype:"msgmenu",
	enterChat: true,
	msgmenu: {
        head_content: "您对本次服务是否满意呢? ",
        list: [{
            type: "click",
            click: {
                id: "101",
                content: "满意",
            },
        },
        {
            type: "click",
            click: {
                id: "102",
                content: "不满意",
            },
        },
        {
            type: "view",
            view: {
                url: "https://work.weixin.qq.com",
                content: "点击跳转到自助查询页面",
            },
        },
        {
            type: "miniprogram",
            miniprogram: {
                appid: "wx123123123123123",
                page: "pages/index?userid=zhangsan&orderid=123123123",
                content: "点击打开小程序查询更多",
            },
        }],
        tail_content: "欢迎再次光临",
    },
	channelsShopProduct: {
        productId: "10000000000000",
        shopAppId: "wx123123123123123",
        imgUrl: "https://mmecimage.cn/p/xxxxxx",
        title: "aaaaa",
        sellingPrice: "800",
        shopImgUrl: "http://mmbiz.qpic.cn/mmbiz_jpg/xxxx",
        shopNickname: "名称"
	},
	success: function(res) {
         //todo:
    }
});
```

## 其他说明

### 接口使用说明

接口使用说明详见“wx.qy.sendChatMessage”，在客服工具栏里调用该接口，自建应用与第三方应用所需的权限有所不同。

### 参数说明

参数说明详见上文表格。
