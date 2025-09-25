#!/bin/bash
# HTTPS启动脚本

echo "🚀 启动微信支付API网关服务 (HTTPS)"

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then
    echo "❌ 需要root权限运行443端口"
    echo "请使用: sudo ./start_https.sh"
    exit 1
fi

# 检查SSL证书是否存在
SSL_CERT="/etc/letsencrypt/live/www.gongjuxiang.work/fullchain.pem"
SSL_KEY="/etc/letsencrypt/live/www.gongjuxiang.work/privkey.pem"

if [ ! -f "$SSL_CERT" ] || [ ! -f "$SSL_KEY" ]; then
    echo "❌ SSL证书不存在:"
    echo "   证书文件: $SSL_CERT"
    echo "   私钥文件: $SSL_KEY"
    echo ""
    echo "请先配置SSL证书:"
    echo "sudo certbot --nginx -d www.gongjuxiang.work"
    exit 1
fi

echo "✅ SSL证书检查通过"

# 停止现有服务
echo "🛑 停止现有服务..."
pkill -f "python3 app.py" 2>/dev/null || true
sleep 2

# 启动HTTPS服务
echo "🌐 启动HTTPS服务 (端口443)..."
cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway
python3 app.py

echo "✅ 服务启动完成"
echo "📱 小程序API地址: https://www.gongjuxiang.work"
echo "🔍 测试命令: curl https://www.gongjuxiang.work/api/wechat/pay/stats"
