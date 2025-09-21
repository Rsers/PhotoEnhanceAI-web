#!/bin/bash

# API网关启动脚本

echo "🚀 启动API网关服务..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 未安装"
    exit 1
fi

# 进入API网关目录
cd "$(dirname "$0")"

# 安装依赖
echo "📦 安装依赖包..."
pip3 install -r requirements.txt

# 启动服务
echo "🌐 启动API网关服务..."
echo "📍 服务地址: http://localhost:5000"
echo "🔗 API文档: http://localhost:5000/api/v1/info"
echo "💚 健康检查: http://localhost:5000/api/v1/health"

python3 app.py
