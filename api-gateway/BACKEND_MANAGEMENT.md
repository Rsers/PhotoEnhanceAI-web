# 多GPU服务器管理系统

## 概述

实现A服务器（API网关）对多台GPU服务器（GPU服务器）的动态管理，支持：
- GPU服务器通过webhook主动注册IP地址
- 预设密码验证机制
- 顺序负载均衡（B1→B2→B3→B1...）
- 自动健康检测（30秒间隔，3次失败标记为不可用）
- 动态服务器数量管理（0-无上限）

## 系统架构

```
A服务器 (API网关)
├── backend_manager.py - GPU服务器管理核心
├── webhook_routes.py - Webhook路由
├── app.py - 主应用（需添加负载均衡逻辑）
└── config.py - 配置管理

GPU服务器 (GPU服务器)
└── test_b_client.py - 测试客户端示例
```

## 核心功能

### 1. GPU服务器注册
- GPU服务器启动时主动调用A服务器webhook
- 携带服务器ID、IP、端口和预设密码
- A服务器验证密码后添加到服务器列表

### 2. 负载均衡
- 顺序轮询策略（B1→B2→B3→B1...）
- 自动跳过不健康的服务器
- 0个服务器时回退到默认配置

### 3. 健康检测
- 30秒检测间隔
- 3次失败后标记为不可用
- 服务器恢复后自动重新上线
- 0个服务器时停止检测

## 配置

### 设置预设密码

```bash
export WEBHOOK_SECRET="gpu-server-register-to-api-gateway-2024"
```

### 配置文件

服务器列表自动保存在 `backend_servers.json`:

```json
[
  {
    "server_id": "B1",
    "ip": "192.168.1.100",
    "port": 8000,
    "url": "http://192.168.1.100:8000",
    "is_healthy": true,
    "fail_count": 0,
    "last_check_time": "2024-01-01T12:00:00",
    "last_used_time": "2024-01-01T12:00:00"
  }
]
```

## API端点

### 1. 注册GPU服务器

```http
POST /webhook/register
Content-Type: application/json

{
    "server_id": "B1",
    "ip": "192.168.1.100",
    "port": 8000,
    "secret": "gpu-server-register-to-api-gateway-2024"
}
```

响应：
```json
{
    "success": true,
    "message": "服务器 B1 注册成功",
    "server_id": "B1",
    "ip": "192.168.1.100",
    "port": 8000
}
```

### 2. 注销GPU服务器

```http
POST /webhook/unregister
Content-Type: application/json

{
    "server_id": "B1",
    "secret": "gpu-server-register-to-api-gateway-2024"
}
```

### 3. 查询服务器列表

```http
GET /webhook/servers?secret=gpu-server-register-to-api-gateway-2024
```

响应：
```json
{
    "success": true,
    "data": {
        "total_servers": 3,
        "healthy_servers": 2,
        "unhealthy_servers": 1,
        "health_check_running": true,
        "servers": [...]
    }
}
```

## 使用测试客户端

### 注册服务器

```bash
python test_b_client.py register \
  --gateway https://www.gongjuxiang.work \
  --server-id B1 \
  --ip 192.168.1.100 \
  --port 8000 \
  --secret gpu-server-register-to-api-gateway-2024
```

### 注销服务器

```bash
python test_b_client.py unregister \
  --gateway https://www.gongjuxiang.work \
  --server-id B1 \
  --secret gpu-server-register-to-api-gateway-2024
```

### 查看服务器列表

```bash
python test_b_client.py list \
  --gateway https://www.gongjuxiang.work \
  --secret gpu-server-register-to-api-gateway-2024
```

## 部署说明

### 1. 修改app.py

在app.py开头添加导入：

```python
from backend_manager import backend_manager
from webhook_routes import register_webhook_routes
```

在app初始化后添加：

```python
# 注册webhook路由
register_webhook_routes(app)
```

### 2. 修改图片处理API

将`enhance_image`函数中的后端URL选择逻辑修改为：

```python
# 使用负载均衡选择服务器
selected_server = backend_manager.get_next_server()
if selected_server:
    backend_url = selected_server.url
    logger.info(f"使用服务器: {selected_server.server_id} ({selected_server.ip})")
else:
    backend_url = BACKEND_API_BASE
    logger.warning("没有可用的GPU服务器，使用默认配置")
```

同样修改`get_task_status`和`download_result`函数。

### 3. 设置密码

```bash
export WEBHOOK_SECRET="gpu-server-register-to-api-gateway-2024"
```

### 4. 重启服务

```bash
sudo systemctl restart api-gateway
```

## GPU服务器端实现

GPU服务器需要在启动时调用webhook注册：

```python
import requests

def register_to_gateway():
    url = "https://www.gongjuxiang.work/webhook/register"
    data = {
        "server_id": "B1",
        "ip": "your-server-ip",
        "port": 8000,
        "secret": "gpu-server-register-to-api-gateway-2024"
    }
    response = requests.post(url, json=data)
    return response.json()

# 启动时注册
register_to_gateway()
```

## 负载均衡流程

```
用户请求 → A服务器
           ↓
    backend_manager.get_next_server()
           ↓
    选择健康的GPU服务器（顺序轮询）
           ↓
    转发请求到选中的GPU服务器
           ↓
    返回结果给用户
```

## 健康检测流程

```
启动健康检测线程（如果有服务器）
    ↓
每30秒检查所有GPU服务器
    ↓
访问 /health 端点
    ↓
成功：重置失败次数
失败：增加失败次数
    ↓
失败次数≥3：标记为不健康
    ↓
继续循环检测
```

## 故障处理

### GPU服务器故障
- 自动检测并标记为不健康
- 负载均衡自动跳过故障服务器
- 服务器恢复后自动重新上线

### 所有GPU服务器故障
- 回退到默认配置（config.py中的backend_api_base）
- 记录警告日志

### IP地址变化
- GPU服务器重新调用注册接口
- A服务器自动更新IP地址
- 无需重启服务

## 监控和日志

所有操作都会记录日志：
- 服务器注册/注销
- 健康检查结果
- 负载均衡选择
- 故障和恢复

查看日志：
```bash
tail -f /path/to/api-gateway.log
```

## 安全考虑

1. **密码验证**：所有webhook调用需要正确的密码
2. **HTTPS传输**：使用HTTPS加密传输
3. **环境变量**：密码存储在环境变量中，不写入代码
4. **密码存储**：后端不存储明文密码，只做验证

## 扩展功能

后续可以添加：
- 更多负载均衡策略（加权、最少连接等）
- 服务器性能监控
- 告警通知
- 管理界面
- 更复杂的健康检测

## 常见问题

### Q: 如何查看当前有哪些GPU服务器？
A: 使用测试客户端的list命令或访问`/webhook/servers`端点

### Q: GPU服务器IP变化了怎么办？
A: 重新调用注册接口，传入新的IP即可

### Q: 如何暂时禁用某台GPU服务器？
A: 调用注销接口将其移除

### Q: 健康检测失败会怎样？
A: 3次失败后标记为不健康，负载均衡会自动跳过

### Q: 没有GPU服务器时会怎样？
A: 回退到config.py中的默认配置
