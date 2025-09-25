# API网关服务

API网关服务为微信小程序等外部应用提供HTTPS API接口，自动代理到基于IP的后端服务。

## 功能特性

- **HTTPS支持**: 提供HTTPS接口，满足小程序合规要求
- **自动代理**: 自动转发请求到后端服务
- **动态配置**: 支持运行时修改后端服务地址
- **错误处理**: 统一的错误响应格式
- **日志记录**: 完整的请求日志记录

## 快速开始

### 1. 安装依赖

```bash
pip install flask flask-cors requests
```

### 2. 启动服务

```bash
python3 app.py
```

### 3. 测试服务

```bash
curl https://gongjuxiang.work/api/v1/health
curl https://gongjuxiang.work/api/v1/info
```

## API接口

### 健康检查
```
GET /api/v1/health
```

### API信息
```
GET /api/v1/info
```

### 配置管理
```
GET /api/v1/config
POST /api/v1/config/backend
```

## 配置管理

### 更新后端地址

#### 方式1：API接口
```bash
curl -X POST https://gongjuxiang.work/api/v1/config/backend \
  -H "Content-Type: application/json" \
  -d '{"backend_url": "http://新IP:8000"}'
```

#### 方式2：命令行工具
```bash
python3 update_backend.py --url http://新IP:8000
python3 simple_update.py 新IP:8000
```

#### 方式3：直接编辑配置文件
```bash
curl https://gongjuxiang.work/api/v1/config
```

## 配置文件

配置文件位置: `/home/ubuntu/PhotoEnhanceAI-web/api-gateway/gateway_config.json`

```json
{
  "backend_api_base": "http://your-backend-server:8000",
  "backend_timeout": 300,
  "gateway_port": 5000,
  "max_file_size": 104857600,
  "supported_endpoints": {
    "enhance": "/api/v1/enhance",
    "status": "/api/v1/status",
    "download": "/api/v1/download"
  }
}
```

## 部署说明

### HTTPS配置

服务默认使用HTTPS，需要配置SSL证书：

```bash
# 证书路径
SSL_CERT="/etc/letsencrypt/live/www.gongjuxiang.work/fullchain.pem"
SSL_KEY="/etc/letsencrypt/live/www.gongjuxiang.work/privkey.pem"
```

### Nginx反向代理

```nginx
location /api/v1/ {
    proxy_pass https://127.0.0.1:8443/api/v1/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # 处理大文件上传
    client_max_body_size 100M;
    proxy_read_timeout 300s;
    proxy_connect_timeout 300s;
    proxy_send_timeout 300s;
    
    # SSL验证
    proxy_ssl_verify off;
}
```

## 微信支付集成

API网关集成了微信小程序支付功能：

### 环境变量配置
```bash
export WECHAT_MCH_ID="你的商户号"
export WECHAT_APPID="你的小程序APPID"
export WECHAT_SECRET="你的小程序Secret"
export WECHAT_API_KEY="你的微信支付API密钥"
export WECHAT_NOTIFY_URL="https://your-domain.com/api/wechat/pay/notify/"
```

### API接口
- `POST /api/wechat/pay/create` - 创建支付订单
- `POST /api/wechat/pay/notify` - 支付回调
- `GET /api/wechat/pay/query/<out_trade_no>` - 查询订单
- `GET /api/wechat/pay/orders/<openid>` - 获取用户订单
- `GET /api/wechat/pay/stats` - 支付统计
- `POST /api/wechat/auth/openid` - 获取openid

### 证书文件
将微信支付证书文件放到以下目录：
- `certificates/` (项目根目录)
- `api-gateway/certs/` (API网关目录)

必需文件：
- `apiclient_cert.pem` - 微信支付证书
- `apiclient_key.pem` - 微信支付私钥

## 使用示例

### JavaScript调用示例

```javascript
// 图片增强
const response = await fetch('https://gongjuxiang.work/api/v1/enhance', {
  method: 'POST',
  body: formData
});

// 查询状态
const status = await fetch(`https://gongjuxiang.work/api/v1/status/${taskId}`);

// 下载结果
const download = await fetch(`https://gongjuxiang.work/api/v1/download/${taskId}`);
```

## 故障排除

### 常见问题

1. **502 Bad Gateway**
   - 检查后端服务是否运行
   - 检查后端服务地址配置

2. **SSL证书错误**
   - 检查证书文件路径
   - 确保证书文件权限正确

3. **连接超时**
   - 检查网络连接
   - 调整超时配置

### 日志查看

```bash
# 查看服务日志
tail -f /var/log/nginx/error.log
```

## 安全提醒

- 定期更新SSL证书
- 监控API访问日志
- 使用HTTPS传输敏感数据
- 定期轮换API密钥