# 更新企业已配置的「联系我」方式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/95724](https://developer.work.weixin.qq.com/document/path/95724)
- **文档 ID**: `95724`
- **API 名称**: `update_contact_way`
- **请求方法**: `POST`
- **接口地址**: `https://qyapi.weixin.qq.com/cgi-bin/externalcontact/update_contact_way?access_token=ACCESS_TOKEN`
- **分组信息**: 第 4 个接口，共 4 个

## 接口描述

更新企业配置的「联系我」二维码和「联系我」小程序按钮中的信息，如使用人员和备注等。

## 请求信息

### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | string | 是 | 调用接口凭证 |

### Body 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| config_id | string | 是 | 企业联系方式的配置id |
| remark | string | 否 | 联系方式的备注信息，不超过30个字符，将覆盖之前的备注 |
| skip_verify | bool | 否 | 外部客户添加时是否无需验证 |
| style | int32 | 否 | 样式，只针对“在小程序中联系”的配置生效 |
| state | string | 否 | 企业自定义的state参数，用于区分不同的添加渠道，在调用“获取客户详情”时会返回该参数值 |
| user | string[] | 否 | 使用该联系方式的用户列表，将覆盖原有用户列表 |
| party | int32[] | 否 | 使用该联系方式的部门列表，将覆盖原有部门列表，只在配置的type为2时有效 |
| expires_in | int32 | 否 | 临时会话二维码有效期，以秒为单位，该参数仅在临时会话模式下有效 |
| chat_expires_in | int32 | 否 | 临时会话有效期，以秒为单位，该参数仅在临时会话模式下有效 |
| unionid | string | 否 | 可进行临时会话的客户unionid，该参数仅在临时会话模式有效，如不指定则不进行限制 |
| mark_source | bool | 否 | 是否标记客户添加来源为该应用创建的「联系我」, 默认为true; 仅对「 |
