# 示例程序-更新日志

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/100247](https://developer.work.weixin.qq.com/document/path/100247)
- **文档 ID**: `100247`
- **API 名称**: `demo_update_log`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 3 个接口，共 3 个

## 接口描述

包含示例程序不同版本的更新日志。

## 响应信息

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| 更新内容 | string | 更新内容描述 |
| 涉及语言 | string | 更新涉及的编程语言 |

## 其他说明

### 2025年7月17日

1.重构任务处理框架，提高并发处理能力。  2.启动命令行参数优化：新增支持配置io进程数、worker线程数、异步线程检查间隔等（一般使用默认值即可）。可在启动命令增加-h参数查看具体的启动参数说明。 3.日志优化：支持打印io进程数、worker线程数、繁忙的worker线程数、队列长度，以及请求耗时等。 | Python `2.1.1`

### 2024年12月10日

新增SDK接口使用示例 | `全部` | 请求队列长度`request_queue_size`改为`2048` | Python | 支持debug模式启动 | Java

### 2024年9月20日

新增SDK接口使用示例 | `全部` | 专区回调逻辑调整，由专区生成notify_id，写本地文件后再通过`spec_notify_app`通知应用 | `全部` | `start.sh` 内启动程序时指定utf-8编码方式：`PYTHONIOENCODING=utf-8` | Python
