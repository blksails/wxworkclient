# 接口创建空间表现

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95850](https://developer.work.weixin.qq.com/document/path/95850)
- **文档 ID**: `95850`
- **API 名称**: `create_shared_space`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/wedrive/create_shared_space?access_token=ACCESS_TOKEN`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

企业和开发者通过微盘接口可以新建共享空间，用于企业内资料共享、文件公示等场景。调用接口的应用自动成为空间的超级管理员，也可指定成员作为管理员辅助管理。

## 请求信息

### 请求示例

```json
{
  "name": "Shared Space",
  "members": ["user1", "user2"],
  "notify_range": ["user3", "user4"]
}
```
