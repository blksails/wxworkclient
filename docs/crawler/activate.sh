#!/bin/bash
# Python 虚拟环境激活脚本
# 使用方法: source activate.sh

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 激活虚拟环境
if [ -f "${SCRIPT_DIR}/venv/bin/activate" ]; then
    source "${SCRIPT_DIR}/venv/bin/activate"
    echo "✓ Python 虚拟环境已激活"
    echo "  Python: $(which python3)"
    echo "  版本: $(python3 --version)"
    echo ""
    echo "可用命令："
    echo "  python3 crawler.py       - 运行爬虫"
    echo "  python3 test_crawler.py  - 运行测试"
    echo "  python3 example.py       - 运行示例"
    echo "  deactivate              - 退出虚拟环境"
else
    echo "✗ 错误: 虚拟环境不存在"
    echo "请先运行: python3 -m venv venv"
    return 1
fi

# 设置环境变量（可选）
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH}"
export PROJECT_ROOT="${SCRIPT_DIR}/.."
