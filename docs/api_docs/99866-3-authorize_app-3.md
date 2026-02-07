# 如何接入

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99866#23-%E4%B8%93%E5%8C%BA%E7%A8%8B%E5%BA%8F%E6%8E%A5%E6%94%B6%E4%BA%8B%E4%BB%B6%E4%BB%A5%E5%8F%8A%E5%BA%94%E7%94%A8%E6%8E%A5%E6%94%B6%E4%B8%93%E5%8C%BA%E9%80%9A%E7%9F%A5](https://developer.work.weixin.qq.com/document/path/99866#23-%E4%B8%93%E5%8C%BA%E7%A8%8B%E5%BA%8F%E6%8E%A5%E6%94%B6%E4%BA%8B%E4%BB%B6%E4%BB%A5%E5%8F%8A%E5%BA%94%E7%94%A8%E6%8E%A5%E6%94%B6%E4%B8%93%E5%8C%BA%E9%80%9A%E7%9F%A5)
- **文档 ID**: `99866`
- **API 名称**: `authorize_app`
- **请求方法**: `POST`
- **接口地址**: `https://yourdomain.com/authorize_app`
- **分组信息**: 第 3 个接口，共 5 个

## 接口描述

企业安装服务商的第三方应用或代开发应用后，进行二次授权。

## 请求信息

### 请求示例

```json
{
  "app_id": "your_app_id",
  "permissions": ["data_intelligence"]
}
```

## 其他说明

### 注意

应用安装时默认不授权「数据与智能专区权限」，企业需要在安装后进行二次授权。
