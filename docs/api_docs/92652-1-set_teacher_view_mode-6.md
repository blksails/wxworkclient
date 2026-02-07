# 设置「老师可查看班级」的模式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/92652](https://developer.work.weixin.qq.com/document/path/92652)
- **文档 ID**: `92652`
- **API 名称**: `set_teacher_view_mode`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/school/set_teacher_view_mode`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

可通过此接口配置教师查看班级的模式：“全部班级”或“仅负责范围内的班级”。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| view_mode | int32 | 是 | 查看模式, 1-全部班级, 2-仅负责范围内的班级 |

### 请求示例

```json
{
   "view_mode":1
}
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | int32 | 返回码 |
| errmsg | string | 对返回码的文本描述内容 |

### 响应示例

```json
{
   "errcode": 0,
   "errmsg": "ok"
}
```

## 其他说明

### 权限说明

调用的应用需要满足如下的权限

- 自建应用：配置到「家校沟通-读取和编辑家校通讯录的应用」中
- 第三方应用：需拥有「家校沟通」使用和编辑 权限

*注：* 从2023年12月1日0点起，不再支持通过系统应用secret调用接口，存量企业暂不受影响 [查看详情](https://developer.work.weixin.qq.com/document/51165)
