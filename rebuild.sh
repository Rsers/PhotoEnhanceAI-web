#!/bin/bash

# PhotoEnhanceAI-web 重新构建和部署脚本
# 用于快速重新构建项目并部署到生产环境

echo "🚀 开始重新构建和部署 PhotoEnhanceAI-web..."

# 进入项目目录
cd /home/ubuntu/PhotoEnhanceAI-web/photo-enhancer

# 清理旧的构建文件
echo "🧹 清理旧的构建文件..."
sudo rm -rf dist

# 重新构建项目
echo "🔨 重新构建项目..."
npm run build

# 检查构建是否成功
if [ $? -eq 0 ]; then
    echo "✅ 构建成功！"
    
    # 设置文件权限
    echo "🔐 设置文件权限..."
    sudo chown -R www-data:www-data dist
    sudo chmod -R 755 dist
    
    # 重新加载Nginx
    echo "🔄 重新加载Nginx..."
    sudo systemctl reload nginx
    
    # 测试网站状态
    echo "🌐 测试网站状态..."
    if curl -s -I http://localhost | grep -q "200 OK"; then
        echo "✅ 网站运行正常！"
        echo "🌐 网站地址: http://82.156.98.52"
    else
        echo "❌ 网站状态异常，请检查Nginx配置"
    fi
    
    echo "🎉 重新构建和部署完成！"
else
    echo "❌ 构建失败，请检查错误信息"
    exit 1
fi
