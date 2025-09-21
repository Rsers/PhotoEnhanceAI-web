#!/bin/bash

# 快速更新后端服务地址脚本
# 使用方法: ./quick_update.sh <新IP地址> [端口]

if [ $# -eq 0 ]; then
    echo "❌ 请提供新的IP地址"
    echo "💡 使用方法: ./quick_update.sh <IP地址> [端口]"
    echo "💡 示例: ./quick_update.sh 192.168.1.100 8000"
    exit 1
fi

NEW_IP=$1
PORT=${2:-8000}
NEW_URL="http://${NEW_IP}:${PORT}"

echo "🚀 正在更新后端服务地址..."
echo "📍 新地址: $NEW_URL"

# 更新配置
python3 update_backend.py --url "$NEW_URL" --method file

# 重启服务
echo "🔄 重启API网关服务..."
pkill -f "python3 app.py"
sleep 2
cd "$(dirname "$0")"
python3 app.py &

# 等待服务启动
sleep 3

# 验证服务
echo "✅ 验证服务状态..."
curl -s https://gongjuxiang.work/api/v1/health | python3 -m json.tool

echo "🎉 更新完成!"
echo "📋 当前配置:"
python3 update_backend.py --show
