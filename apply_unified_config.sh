#!/bin/bash
# 应用统一配置架构
# 将所有API请求统一通过API网关，后端IP只在gateway_config.json配置

echo "=========================================="
echo "  统一后端IP配置架构"
echo "=========================================="
echo ""
echo "📝 架构说明："
echo "- 所有 /api/* 请求通过API网关转发"
echo "- 后端GPU服务器IP只需在一个文件配置："
echo "  /home/ubuntu/PhotoEnhanceAI-web/api-gateway/gateway_config.json"
echo ""

# 备份当前配置
echo "🔄 备份当前Nginx配置..."
sudo cp /etc/nginx/sites-enabled/gongjuxiang.work /etc/nginx/sites-enabled/gongjuxiang.work.backup.$(date +%Y%m%d_%H%M%S)

# 应用新配置
echo "📋 应用统一配置..."
sudo cp /home/ubuntu/PhotoEnhanceAI-web/gongjuxiang.work.unified /etc/nginx/sites-enabled/gongjuxiang.work

# 测试Nginx配置
echo ""
echo "🧪 测试Nginx配置..."
if sudo nginx -t; then
    echo ""
    echo "✅ Nginx配置测试通过"
    
    # 重载Nginx
    echo ""
    echo "🔄 重载Nginx..."
    sudo systemctl reload nginx
    
    if [ $? -eq 0 ]; then
        echo "✅ Nginx重载成功"
        echo ""
        echo "=========================================="
        echo "  配置应用完成！"
        echo "=========================================="
        echo ""
        echo "📍 后端IP配置位置（唯一）："
        echo "   /home/ubuntu/PhotoEnhanceAI-web/api-gateway/gateway_config.json"
        echo ""
        echo "📖 查看当前后端IP："
        cat /home/ubuntu/PhotoEnhanceAI-web/api-gateway/gateway_config.json | grep backend_api_base
        echo ""
        echo "📚 详细说明文档："
        echo "   /home/ubuntu/PhotoEnhanceAI-web/BACKEND_CONFIG.md"
        echo ""
        echo "🔧 以后修改后端IP只需："
        echo "   1. 编辑 gateway_config.json"
        echo "   2. 重启API网关服务"
        echo "   3. 无需修改Nginx配置"
        echo ""
    else
        echo "❌ Nginx重载失败"
        exit 1
    fi
else
    echo "❌ Nginx配置测试失败，未应用新配置"
    echo "旧配置仍然有效"
    exit 1
fi



