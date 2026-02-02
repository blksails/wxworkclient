#!/bin/bash

# 企业微信 API 文档爬虫启动脚本

set -e

echo "==================================="
echo "企业微信 API 文档爬虫"
echo "==================================="
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: Python 3 未安装"
    exit 1
fi

echo "Python 版本: $(python3 --version)"
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
    echo "✓ 虚拟环境已创建"
    echo ""
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖包..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ 依赖包已安装"
echo ""

# 运行爬虫
echo "开始运行爬虫..."
echo "==================================="
echo ""
python3 crawler.py

echo ""
echo "==================================="
echo "爬虫运行完成！"
echo "生成的文档保存在: ../api_docs/"
echo "==================================="
