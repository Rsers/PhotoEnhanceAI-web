# GPU服务器管理系统

## 系统架构

```
A服务器 (API网关)
├── 图片处理API (负载均衡到GPU服务器)
│   ├── /api/v1/enhance - 图片增强
│   ├── /api/v1/status/{task_id} - 查询任务状态
│   └── /api/v1/download/{task_id} - 下载处理结果
├── 微信相关API (直接处理，不涉及GPU服务器)
│   ├── 微信支付API
│   ├── 微信授权API
│   └── 微信小程序接口
├── 网关管理API (直接处理)
│   ├── /api/v1/health - 健康检查
│   ├── /api/v1/info - API信息
│   └── /api/v1/config - 配置管理
└── Webhook管理
    ├── /webhook/register - GPU服务器注册
    ├── /webhook/unregister - GPU服务器注销
    └── /webhook/servers - 查询服务器列表

GPU服务器 (GPU服务器)
└── GPU服务器客户端 (test_b_client.py)
```

## GPU服务器命名规则

### 服务器ID自动分配机制
- **A服务器自动分配**：每台GPU服务器注册时，A服务器自动分配唯一的`server_id`
- **命名格式**：`GPU-001`、`GPU-002`、`GPU-003`...（按注册顺序自动编号）
- **唯一性保证**：A服务器确保每台GPU服务器都有唯一的标识符
- **无需手动配置**：GPU服务器无需知道自己的`server_id`，由A服务器管理

### 部署前准备
1. **确认网络配置**：确保GPU服务器有公网IP地址
2. **准备环境变量**：设置正确的`GATEWAY_URL`、`SHARED_SECRET`等配置
3. **无需server_id**：GPU服务器不需要配置`SERVER_ID`，由A服务器自动分配

## GPU服务器Webhook调用

### 1. 注册GPU服务器

GPU服务器启动时需要主动调用A服务器的注册接口，A服务器会自动分配`server_id`：

```bash
# 使用测试客户端注册（无需指定server-id）
python3 test_b_client.py register \
  --gateway https://www.gongjuxiang.work \
  --ip GPU服务器的公网IP地址 \
  --port 8000 \
  --secret gpu-server-register-to-api-gateway-2024
```

**API调用示例**：
```bash
curl -X POST https://www.gongjuxiang.work/webhook/register \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "GPU服务器的公网IP地址",
    "port": 8000,
    "secret": "gpu-server-register-to-api-gateway-2024"
  }'
```

**响应示例**：
```json
{
  "success": true,
  "message": "服务器 GPU-001 注册成功",
  "server_id": "GPU-001",
  "ip": "GPU服务器的公网IP地址",
  "port": 8000
}
```

### 2. GPU服务器部署配置

**重要说明**：
- `server_id` 由A服务器自动分配，GPU服务器无需配置
- 注册成功后，A服务器会返回分配的`server_id`
- GPU服务器只需要提供自己的IP地址和端口即可

**环境变量设置**：
```bash
export GATEWAY_URL="https://www.gongjuxiang.work"
export SHARED_SECRET="gpu-server-register-to-api-gateway-2024"
export PORT="8000"
# 注意：无需设置SERVER_ID，由A服务器自动分配
```

**Python代码示例**：
```python
import requests
import os

def register_to_gateway():
    """GPU服务器启动时注册到A服务器"""
    url = "https://www.gongjuxiang.work/webhook/register"
    data = {
        "ip": get_current_ip(),  # 获取当前服务器的公网IP地址
        "port": int(os.getenv('PORT', '8000')),
        "secret": os.getenv('SHARED_SECRET', 'gpu-server-register-to-api-gateway-2024')
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                assigned_server_id = result.get('server_id')
                print(f"✓ 服务器 {assigned_server_id} 注册成功")
                return True, assigned_server_id
            else:
                print(f"✗ 注册失败: {result.get('error')}")
                return False, None
        else:
            print(f"✗ 注册请求失败: HTTP {response.status_code}")
            return False, None
    except Exception as e:
        print(f"✗ 注册失败: {e}")
        return False, None

def get_current_ip():
    """获取当前服务器的公网IP地址"""
    import socket
    try:
        # 方法1：通过连接外部服务器获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # 方法2：如果上述方法失败，可以调用外部API获取公网IP
        try:
            import requests
            response = requests.get('https://api.ipify.org', timeout=5)
            return response.text.strip()
        except Exception:
            return "127.0.0.1"  # 最后的回退选项

# GPU服务器启动时调用
if __name__ == '__main__':
    register_to_gateway()
```

### 3. Systemd服务部署

创建systemd服务文件 `/etc/systemd/system/b-server-client.service`：

```ini
[Unit]
Description=B Server Client
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/your/project
# 注意：无需设置SERVER_ID，由A服务器自动分配
Environment=GATEWAY_URL=https://www.gongjuxiang.work
Environment=SHARED_SECRET=gpu-server-register-to-api-gateway-2024
Environment=PORT=8000
ExecStart=/usr/bin/python3 b_server_client.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**启动服务**：
```bash
sudo systemctl daemon-reload
sudo systemctl enable b-server-client
sudo systemctl start b-server-client
```

### 4. IP地址变化处理

当GPU服务器公网IP地址发生变化时，需要重新注册：

```python
def update_ip_on_change():
    """检测公网IP变化并更新注册"""
    current_ip = get_current_ip()  # 获取当前公网IP
    last_ip = load_last_ip()  # 从文件或数据库加载上次的IP
    
    if current_ip != last_ip:
        print(f"检测到公网IP地址变化: {last_ip} -> {current_ip}")
        if register_to_gateway():
            save_last_ip(current_ip)  # 保存新的公网IP
            print("公网IP地址更新成功")
        else:
            print("公网IP地址更新失败")
```

### 5. 注销GPU服务器

GPU服务器关闭时需要注销（通过IP地址注销）：

```bash
# 使用测试客户端注销
python3 test_b_client.py unregister \
  --gateway https://www.gongjuxiang.work \
  --ip GPU服务器的公网IP地址 \
  --port 8000 \
  --secret gpu-server-register-to-api-gateway-2024
```

**API调用示例**：
```bash
curl -X POST https://www.gongjuxiang.work/webhook/unregister \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "GPU服务器的公网IP地址",
    "port": 8000,
    "secret": "gpu-server-register-to-api-gateway-2024"
  }'
```

## 负载均衡机制

### 顺序轮询策略
- **GPU-001 → GPU-002 → GPU-003 → GPU-001**：按顺序轮流分配请求
- **故障跳过**：自动跳过不健康的服务器
- **动态调整**：服务器上线/下线时自动调整

### 健康检测
- **检测间隔**：30秒
- **失败阈值**：3次失败后标记为不可用
- **自动恢复**：服务器恢复后自动重新上线

## 配置管理

### A服务器配置
```bash
# 设置共享密钥
export WEBHOOK_SECRET="gpu-server-register-to-api-gateway-2024"

# 启用多GPU服务器模式
curl -X POST https://www.gongjuxiang.work/api/v1/config/multi-backend \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'
```

### 查看GPU服务器状态
```bash
# 查看所有GPU服务器
python3 test_b_client.py list \
  --gateway https://www.gongjuxiang.work \
  --secret gpu-server-register-to-api-gateway-2024

# 通过API查看
curl "https://www.gongjuxiang.work/webhook/servers?secret=gpu-server-register-to-api-gateway-2024"
```

## 故障处理

### GPU服务器故障
- **自动检测**：30秒内检测到服务器离线
- **负载转移**：自动停止向故障服务器分发请求
- **自动恢复**：服务器恢复后自动重新加入负载均衡

### 所有GPU服务器故障
- **服务降级**：返回503错误"服务暂时不可用"
- **用户提示**：提示用户稍后重试
- **自动恢复**：GPU服务器上线后立即恢复服务

## 安全机制

### 身份验证
- **预设密码**：GPU服务器调用时在请求体中携带密码
- **HTTPS传输**：所有通信都通过HTTPS加密
- **密码验证**：A服务器验证密码后才允许注册

### 访问控制
- **Webhook端点**：只有知道密码的GPU服务器可以调用
- **管理端点**：支持可选的密码验证
- **日志记录**：记录所有注册和注销操作

## 动态配置管理

### 多GPU服务器管理

当需要添加或管理GPU服务器时，可以通过以下方式：

#### 方式1：使用测试客户端（推荐）

```bash
# 进入API网关目录
cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway

# 注册GPU服务器（无需指定server-id）
python3 test_b_client.py register \
  --ip GPU服务器的公网IP地址 \
  --port 8000 \
  --secret gpu-server-register-to-api-gateway-2024

# 查看GPU服务器状态
python3 test_b_client.py list \
  --secret gpu-server-register-to-api-gateway-2024

# 注销GPU服务器（通过IP注销）
python3 test_b_client.py unregister \
  --ip GPU服务器的公网IP地址 \
  --port 8000 \
  --secret gpu-server-register-to-api-gateway-2024
```

#### 方式2：API接口管理

```bash
# 注册GPU服务器
curl -X POST https://www.gongjuxiang.work/webhook/register \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "GPU服务器的公网IP地址",
    "port": 8000,
    "secret": "gpu-server-register-to-api-gateway-2024"
  }'

# 查看GPU服务器状态
curl "https://www.gongjuxiang.work/webhook/servers?secret=gpu-server-register-to-api-gateway-2024"

# 启用多GPU服务器模式
curl -X POST https://www.gongjuxiang.work/api/v1/config/multi-backend \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'
```

#### 方式3：GPU服务器自动注册

GPU服务器启动时自动注册：

```python
import requests
import os

def register_to_gateway():
    """GPU服务器启动时注册到A服务器"""
    url = "https://www.gongjuxiang.work/webhook/register"
    data = {
        # 注意：无需设置server_id，由A服务器自动分配
        "ip": get_current_ip(),
        "port": int(os.getenv('PORT', '8000')),
        "secret": os.getenv('SHARED_SECRET', 'gpu-server-register-to-api-gateway-2024')
    }
    
    response = requests.post(url, json=data, timeout=10)
    return response.json()

# GPU服务器启动时调用
register_to_gateway()
```

### 更新后重启服务

```bash
# 停止API网关服务
pkill -f "python3 app.py"

# 重新启动服务
cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway
python3 app.py &

# 验证服务状态
curl https://gongjuxiang.work/api/v1/health
```

### 配置验证

```bash
# 检查GPU服务器状态
python3 test_b_client.py list --secret gpu-server-register-to-api-gateway-2024

# 查看API网关信息
curl https://gongjuxiang.work/api/v1/info | python3 -m json.tool

# 测试负载均衡
curl -X POST https://gongjuxiang.work/api/v1/enhance \
  -F "file=@test.jpg"
```

### 使用场景

1. **GPU服务器部署**：新部署GPU服务器时自动注册
2. **IP地址变更**：GPU服务器IP变化时自动更新
3. **负载均衡**：多台GPU服务器分担处理压力
4. **故障转移**：GPU服务器故障时自动切换
5. **动态扩容**：根据需要动态添加GPU服务器
