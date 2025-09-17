#!/bin/bash

# 切换到项目目录
cd /Users/caoxinnan/repo/project2-照片超分辨率/photo-enhancer

# 获取本机IP地址
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

# 启动开发服务器
echo "🚀 启动照片超分辨率前端服务器..."
echo "📱 本机IP地址: $LOCAL_IP"
echo "🌐 网络访问地址: http://$LOCAL_IP:5173 (如果端口被占用会自动切换)"
echo "💻 本地访问地址: http://localhost:5173"
echo ""
echo "⚠️  注意：如果5173端口被占用，Vite会自动使用其他端口"
echo "   请查看启动后的实际端口号"
echo ""

# 使用正确的Vite参数格式
npm run dev -- --host