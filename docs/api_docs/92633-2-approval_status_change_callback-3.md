# 事件格式

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/92633](https://developer.work.weixin.qq.com/document/path/92633)
- **文档 ID**: `92633`
- **API 名称**: `approval_status_change_callback`
- **请求方法**: `POST`
- **分组信息**: 第 2 个接口，共 2 个

## 接口描述

当指定类型的审批申请发生状态变化时，企业微信将向回调地址发送相应的通知事件。状态变化包括但不限于：催办、撤销、同意、驳回、转审、添加备注等情况。

## 请求信息

### 请求示例

```xml
<xml>
  <ToUserName><![CDATA[ww1cSD21f1e9c0caaa]]></ToUserName>
  <FromUserName><![CDATA[sys]]></FromUserName>
  <CreateTime>1571732272</CreateTime>
  <MsgType><![CDATA[event]]></MsgType>
  <Event><![CDATA[sys_approval_change]]></Event>
  <AgentID>3010040</AgentID>
  <ApprovalInfo>
    ...
  </ApprovalInfo>
</xml>
```

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| Event | string | 事件名称：sys_approval_change |
| SpNoStr | string | 审批编号（字符串类型） |
| SpName | string | 审批申请类型名称（审批模板名称） |
| SpStatus | int32 | 申请单状态：1-审批中；2-已通过；3-已驳回；4-已撤销；6-通过后撤销；7-已删除；10-已支付 |
| TemplateId | string | 审批模板id。可在“获取审批申请详情”、“审批状态变化回调通知”中获得，也可在审批模板的模板编辑页面链接中获得。 |
| ApplyTime | int32 | 审批申请提交时间,Unix时间戳 |
| Applyer.UserId | string | 申请人userid |
| Applyer.Party | string | 申请人所在部门pid |
| SpRecord[].SpStatus | int32 | 审批节点状态：1-审批中；2-已同意；3-已驳回；4-已转审 |
| SpRecord[].ApproverAttr | int32 | 节点审批方式：1-或签；2-会签 |
| SpRecord[].Details[].Approver.UserId | string | 分支审批人userid |
| SpRecord[].Details[].Speech | string | 审批意见字段 |
| SpRecord[].Details[].SpStatus | int32 | 分支审批人审批状态：1-审批中；2-已同意；3-已驳回；4-已转审 |
| SpRecord[].Details[].SpTime | int32 | 节点分支审批人审批操作时间，0为尚未操作 |
| Notifyer.UserId | string | 节点抄送人userid |
| Comments[].CommentUserInfo.UserId | string | 备注人userid |
| Comments[].CommentTime | int32 | 备注提交时间 |
| Comments[].CommentContent | string | 备注文本内容 |
| Comments[].CommentId | string | 备注id |
| ProcessList[].NodeList[].NodeType | int32 | 节点类型 1 审批人 2 抄送人 3办理人 |
| ProcessList[].NodeList[].SpStatus | int32 | 节点状态 1-审批中；2-同意；3-驳回；4-转审；11-退回给指定审批人；12-加签；13-同意并加签；14-办理；15-转交 |
| ProcessList[].NodeList[].ApvRel | int32 | 多人办理方式 1-会签；2-或签 3-依次审批 |
| ProcessList[].NodeList[].SubNodeList[].UserInfo.UserId | string | 处理人userid |
| ProcessList[].NodeList[].SubNodeList[].Speech | string | 审批/办理意见 |
| ProcessList[].NodeList[].SubNodeList[].SpYj | int32 | 子节点状态 1-审批中；2-同意；3-驳回；4-转审；11-退回给指定审批人；12-加签；13-同意并加签；14-办理；15-转交 |
| ProcessList[].NodeList[].SubNodeList[].Sptime | int32 | 操作时间 |
| StatuChangeEvent | int32 | 审批申请状态变化类型：1-提单；2-同意；3-驳回；4-转审；5-催办；6-撤销；8-通过后撤销；10-添加备注；11-回退给指定审批人；12-添加审批人；13-加签并同意 |
| SpNo | string | 审批编号 |

## 其他说明

### 参数说明

详细参数说明见上方表格
