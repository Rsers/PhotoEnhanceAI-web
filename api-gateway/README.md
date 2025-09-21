# API网关服务

为微信小程序提供HTTPS API接口，自动代理到基于IP的后端服务。

## 功能特性

- ✅ HTTPS支持，满足小程序合规要求
- ✅ 动态配置后端服务地址
- ✅ 支持多种更新方式（配置文件/API接口）
- ✅ 健康检查和状态监控
- ✅ 错误处理和日志记录

## 快速开始

### 启动服务

```bash
cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway
./start.sh
```

### 检查服务状态

```bash
curl https://gongjuxiang.work/api/v1/health
curl https://gongjuxiang.work/api/v1/info
```

## 配置管理

### 查看当前配置

```bash
python3 update_backend.py --show
```

### 更新后端服务地址

#### 方式1: 通过配置文件更新

```bash
# 更新为新的IP地址
python3 update_backend.py --url http://新IP:8000

# 示例
python3 update_backend.py --url http://192.168.1.100:8000
```

#### 方式2: 通过API接口更新

```bash
# 通过API更新（需要服务运行中）
python3 update_backend.py --url http://新IP:8000 --method api

# 指定网关地址
python3 update_backend.py --url http://新IP:8000 --method api --gateway http://127.0.0.1:5000
```

### 测试后端连接

```bash
# 测试指定URL的连接
python3 update_backend.py --test http://新IP:8000
```

## API接口

### 获取配置信息

```bash
curl https://gongjuxiang.work/api/v1/config
```

### 更新后端地址（API方式）

```bash
curl -X POST https://gongjuxiang.work/api/v1/config/backend \
  -H "Content-Type: application/json" \
  -d '{"backend_url": "http://新IP:8000"}'
```

## 配置文件

配置文件位置: `/home/ubuntu/PhotoEnhanceAI-web/api-gateway/gateway_config.json`

```json
{
  "backend_api_base": "http://43.143.246.112:8000",
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

## 服务管理

### 重启服务

```bash
# 停止服务
pkill -f "python3 app.py"

# 启动服务
cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway
python3 app.py &
```

### 查看服务状态

```bash
# 查看进程
ps aux | grep python3 | grep app.py

# 查看端口
netstat -tlnp | grep 5000
```

## 故障排除

### 1. 服务无法启动

```bash
# 检查Python依赖
pip3 install -r requirements.txt

# 检查端口占用
netstat -tlnp | grep 5000
```

### 2. 后端服务连接失败

```bash
# 测试后端连接
python3 update_backend.py --test http://后端IP:8000

# 检查防火墙
sudo ufw status
```

### 3. 配置更新不生效

```bash
# 重启服务应用新配置
pkill -f "python3 app.py"
cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway
python3 app.py &
```

## 使用场景

### 微信小程序调用

```javascript
// 小程序中调用API
wx.request({
  url: 'https://gongjuxiang.work/api/v1/enhance',
  method: 'POST',
  data: formData,
  success: function(res) {
    console.log(res.data);
  }
});
```

### 后端服务迁移

当后端服务IP地址变更时：

1. 使用更新工具修改配置
2. 重启API网关服务
3. 验证服务正常

```bash
# 一键更新并重启
python3 update_backend.py --url http://新IP:8000
pkill -f "python3 app.py" && cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway && python3 app.py &
```
