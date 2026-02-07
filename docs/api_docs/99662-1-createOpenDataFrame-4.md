# 会话内容存档

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99662](https://developer.work.weixin.qq.com/document/path/99662)
- **文档 ID**: `99662`
- **API 名称**: `createOpenDataFrame`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/chatdata/create_open_data_frame`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

用于创建展示组件，展示企业的会话记录信息。

## 请求信息

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| el | HTMLElement | string | 是 | 组件容器，可以是实际的 DOM 元素或 CSS 选择器字符串。 |
| data | unknown | 否 | 组件自定义数据，可以在模板中访问。 |
| template | string | 是 | 组件模板，用于自定义组件内的展示内容。 |
| style | string | 否 | 组件模板样式表，语法是 CSS 的子集。 |

### 请求示例

```text
const factory = ww.createOpenDataFrameFactory();
const instance = factory.createOpenDataFrame({
  el: containerElement,
  template: `<view>...</view>`,
  style: `.msg { height: 100%; overflow: auto; }`,
  data: { msgList },
  methods: { handleClickEvent() { instance.setData({ msgList: newMsgList }) }
});
```
