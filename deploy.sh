#!/bin/bash

# PhotoEnhanceAI-web 部署脚本
# 用于更新前端应用

echo "🚀 开始部署 PhotoEnhanceAI-web..."

# 进入项目目录
cd /home/ubuntu/PhotoEnhanceAI-web/photo-enhancer

# 拉取最新代码
echo "📥 拉取最新代码..."
git pull origin main

# 安装依赖
echo "📦 安装依赖..."
npm install

# 构建生产版本
echo "🔨 构建生产版本..."
npm run build

# 设置权限
echo "🔐 设置文件权限..."
sudo chown -R www-data:www-data dist
sudo chmod -R 755 dist

# 重启Nginx
echo "🔄 重启Nginx..."
sudo systemctl reload nginx

echo "✅ 部署完成！"
echo "🌐 网站地址: http://82.156.98.52"
echo "📊 Nginx状态:"
sudo systemctl status nginx --no-pager -l
