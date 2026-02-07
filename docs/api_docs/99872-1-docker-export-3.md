# 准备镜像

## 基本信息

- **文档地址**: [https://developer.work.weixin.qq.com/document/path/99872](https://developer.work.weixin.qq.com/document/path/99872)
- **文档 ID**: `99872`
- **API 名称**: `docker-export`
- **请求方法**: `N/A`
- **接口地址**: `N/A`
- **分组信息**: 第 1 个接口，共 2 个

## 接口描述

使用 docker-export 将运行环境导出`tar`包，用于数据与智能专区的镜像导入。请特别注意不能用 docker-save 命令生成`tar`包，否则可能无法执行启动命令。

## 请求信息

### 请求示例

```text
docker-export [OPTIONS] CONTAINER > file.tar
```

## 其他说明

### 官方文档

docker 的相关使用请参考[官方文档](https://docs.docker.com/reference/)
