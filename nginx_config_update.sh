#!/bin/bash
# 更新Nginx配置脚本

echo "🔧 更新Nginx配置..."

# 备份原配置
sudo cp /etc/nginx/sites-enabled/gongjuxiang.work /etc/nginx/sites-enabled/gongjuxiang.work.backup

# 修改API代理配置
sudo sed -i 's|proxy_pass http://127.0.0.1:5000/api/v1/|proxy_pass https://127.0.0.1:8443/api/v1/|g' /etc/nginx/sites-enabled/gongjuxiang.work

# 在/api/配置之前添加微信支付API配置
sudo sed -i '/location \/api\/ {/i\    # 微信支付API代理配置\n    location /api/wechat/ {\n        proxy_pass https://127.0.0.1:8443/api/wechat/;\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;\n        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n        proxy_set_header X-Forwarded-Proto $scheme;\n        \n        # 处理大文件上传\n        client_max_body_size 100M;\n        proxy_read_timeout 300s;\n        proxy_connect_timeout 300s;\n        proxy_send_timeout 300s;\n        \n        # SSL验证\n        proxy_ssl_verify off;\n    }\n' /etc/nginx/sites-enabled/gongjuxiang.work

# 测试配置
if sudo nginx -t; then
    echo "✅ Nginx配置测试通过"
    sudo systemctl reload nginx
    echo "✅ Nginx配置已重新加载"
else
    echo "❌ Nginx配置测试失败"
    sudo cp /etc/nginx/sites-enabled/gongjuxiang.work.backup /etc/nginx/sites-enabled/gongjuxiang.work
    echo "🔄 已恢复原配置"
fi
