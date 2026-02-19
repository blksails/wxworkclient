# 编辑获客链接

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/97394](https://developer.work.weixin.qq.com/document/path/97394)
- **文档 ID**: `97394`
- **API 名称**: `update_link`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/customer_acquisition/update_link?access_token=ACCESS_TOKEN`
- **分组信息**: 第 4 个接口，共 5 个

## 接口描述

企业可通过此接口编辑获客链接，修改获客链接的关联范围或修改获客链接的名称。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| link_id | string | 是 | 获客链接的id。需要是当前应用创建 |
| link_name | string | 否 | 更新的链接名称,最长为30个字符 |
| range.user_list | string[] | 否 | 此获客链接关联的userid列表，最多可关联500个 |
| range.department_list | int32[] | 否 | 此获客链接关联的部门id列表，部门覆盖总人数最多500个 |
| skip_verify | bool | 否 | 是否无需验证，默认为true |
| priority_option.priority_type | int32 | 否 | 客户与成员关系绑定，1-全企业范围内优先分配给有好友关系的成员；2-指定范围内优先分配有好友关系的成员 |
| priority_option.priority_userid_list | string[] | 否 | priority_type为2时的指定成员列表，最多1000个 |
| mark_source | bool | 否 | 是否标记客户添加来源为该应用创建的获客链接, 默认值为true; 仅对「营销获客」应用生效 |

### 请求示例

```json
{
   "link_id":"LINK_ID",
   "link_name":"获客链接1号",
   "range":
   {
   		"user_list":["zhangsan","lisi"],
		"department_list":[2,3]
   },
   "skip_verify":true,
   "priority_option":
	{
		"priority_type":2,
		"priority_userid_list":["tom","lisi"]
	},
	"mark_source":true
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
