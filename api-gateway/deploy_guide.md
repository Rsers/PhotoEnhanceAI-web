# 微信支付部署指南

## 1. 配置环境变量（推荐方式）

```bash
export WECHAT_MCH_ID="你的商户号"
export WECHAT_APPID="你的小程序APPID"
export WECHAT_SECRET="你的小程序Secret"
export WECHAT_API_KEY="你的微信支付API密钥"
export WECHAT_NOTIFY_URL="https://your-domain.com/api/wechat/pay/notify/"
```

## 2. 或使用配置文件

1. 复制 `wechat_config_template.json` 为 `wechat_config.json`
2. 填入真实的配置信息
3. 设置环境变量 `WECHAT_CONFIG_FILE=/path/to/wechat_config.json`

## 3. 证书文件

将微信支付证书文件放到以下任一目录：
- `certificates/` (项目根目录)
- `api-gateway/certs/` (API网关目录)
- 或通过环境变量 `WECHAT_CERT_DIR` 指定

必需文件：
- `apiclient_cert.pem` - 微信支付证书
- `apiclient_key.pem` - 微信支付私钥

## 4. 部署步骤

### 方式1：环境变量部署（推荐）
```bash
# 设置环境变量
export WECHAT_MCH_ID="你的商户号"
export WECHAT_APPID="你的小程序APPID"
export WECHAT_SECRET="你的小程序Secret"
export WECHAT_API_KEY="你的微信支付API密钥"
export WECHAT_NOTIFY_URL="https://your-domain.com/api/wechat/pay/notify/"

# 启动服务
cd api-gateway
python3 app.py
```

### 方式2：配置文件部署
```bash
# 复制配置模板
cp wechat_config_template.json wechat_config.json

# 编辑配置文件
nano wechat_config.json

# 设置配置文件路径
export WECHAT_CONFIG_FILE="/path/to/wechat_config.json"

# 启动服务
python3 app.py
```

## 5. 验证配置

```bash
# 测试配置是否正确
python3 test_config.py
```

## 6. 安全提醒

- 配置文件包含敏感信息，不要提交到版本控制
- 证书文件已添加到 `.gitignore`
- 生产环境建议使用环境变量而非配置文件
- 定期轮换API密钥和证书