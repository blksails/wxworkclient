# 获取应用共享信息

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/96815](https://developer.work.weixin.qq.com/document/path/96815)
- **文档 ID**: `96815`
- **API 名称**: `get_shared_app_info`
- **请求方法**: `GET`
- **接口地址**: `https://wework.qpic.cn/wwpic/754964_lUVf8GFSS12Jijl_1607482186/0`
- **分组信息**: 第 1 个接口，共 6 个

## 接口描述

上级企业的管理员在管理端分享应用给下级企业后，需要通过此接口获取分享后的下级企业的corpid和应用id列表并保存起来。

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| corpid | string | 下级企业的企业ID |
| app_id_list | array | 下级企业的应用ID列表 |
