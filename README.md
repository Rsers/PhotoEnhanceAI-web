# PhotoEnhanceAI - 照片超分辨率增强工具

一个基于 AI 技术的照片超分辨率增强工具，可以将低分辨率照片转换为高分辨率版本，提升图片质量和清晰度。支持单张处理和批量处理两种模式。

## 🎯 项目核心功能

本项目实现了四个核心功能模块：

### 1. 🌐 Web前端页面
- **Vue 3 + TypeScript** 构建的现代化Web界面
- **响应式设计**，支持桌面端和移动端访问
- **图片上传、处理、对比展示**等完整用户体验
- **批量处理**和**单张处理**两种模式

### 2. 🔄 GFPGAN面部增强API中转服务
- **API网关服务**：为微信小程序提供HTTPS接口
- **GPU服务器代理**：真正的GFPGAN API部署在GPU服务器上
- **域名合规**：解决微信小程序对API域名的HTTPS和备案要求
- **中转调用**：通过当前服务器进行API中转，满足小程序合规要求

### 3. 💳 微信小程序"喵喵美颜"支付后端
- **完整的微信支付API**：订单创建、支付回调、订单查询
- **用户认证**：微信登录openid获取
- **订单管理**：本地订单存储和状态跟踪
- **支付统计**：订单数据分析和统计功能

### 4. 🔧 多GPU服务器管理系统
- **动态服务器注册**：GPU服务器通过webhook主动注册IP地址
- **负载均衡**：支持多台GPU服务器顺序负载均衡
- **健康检测**：自动检测GPU服务器状态，故障自动切换
- **IP动态更新**：GPU服务器IP变化时自动更新配置

> **🚨 部署前必读**：
> - 请确保服务器已开放 **8000 端口**，否则前端无法正常连接后端 API 服务
> - 如果使用国内服务器，推送代码到 GitHub 可能遇到网络问题，请参考 [GitHub 访问问题](#github-访问问题) 解决方案
> 
> 详细配置方法请查看 [服务器部署](#服务器部署) 和 [故障排除](#故障排除) 部分。

## 🔧 多GPU服务器管理系统

### 系统架构

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

### GPU服务器Webhook调用

#### 1. 注册GPU服务器

GPU服务器启动时需要主动调用A服务器的注册接口：

```bash
# 使用测试客户端注册
python3 test_b_client.py register \
  --gateway https://www.gongjuxiang.work \
  --server-id B1 \
  --ip 192.168.1.100 \
  --port 8000 \
  --secret your-secret-password-2024
```

**API调用示例**：
```bash
curl -X POST https://www.gongjuxiang.work/webhook/register \
  -H "Content-Type: application/json" \
  -d '{
    "server_id": "B1",
    "ip": "192.168.1.100",
    "port": 8000,
    "secret": "your-secret-password-2024"
  }'
```

**响应示例**：
```json
{
  "success": true,
  "message": "服务器 B1 注册成功",
  "server_id": "B1",
  "ip": "192.168.1.100",
  "port": 8000
}
```

#### 2. GPU服务器部署配置

**环境变量设置**：
```bash
export SERVER_ID="B1"
export GATEWAY_URL="https://www.gongjuxiang.work"
export SHARED_SECRET="your-secret-password-2024"
export PORT="8000"
```

**Python代码示例**：
```python
import requests
import os

def register_to_gateway():
    """GPU服务器启动时注册到A服务器"""
    url = "https://www.gongjuxiang.work/webhook/register"
    data = {
        "server_id": os.getenv('SERVER_ID', 'B1'),
        "ip": get_current_ip(),  # 获取当前服务器IP
        "port": int(os.getenv('PORT', '8000')),
        "secret": os.getenv('SHARED_SECRET', 'your-secret-password-2024')
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✓ 服务器 {data['server_id']} 注册成功")
                return True
            else:
                print(f"✗ 注册失败: {result.get('error')}")
                return False
        else:
            print(f"✗ 注册请求失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 注册失败: {e}")
        return False

def get_current_ip():
    """获取当前服务器IP地址"""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# GPU服务器启动时调用
if __name__ == '__main__':
    register_to_gateway()
```

#### 3. Systemd服务部署

创建systemd服务文件 `/etc/systemd/system/b-server-client.service`：

```ini
[Unit]
Description=B Server Client
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/your/project
Environment=SERVER_ID=B1
Environment=GATEWAY_URL=https://www.gongjuxiang.work
Environment=SHARED_SECRET=your-secret-password-2024
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

#### 4. IP地址变化处理

当GPU服务器IP地址发生变化时，需要重新注册：

```python
def update_ip_on_change():
    """检测IP变化并更新注册"""
    current_ip = get_current_ip()
    last_ip = load_last_ip()  # 从文件或数据库加载上次的IP
    
    if current_ip != last_ip:
        print(f"检测到IP地址变化: {last_ip} -> {current_ip}")
        if register_to_gateway():
            save_last_ip(current_ip)  # 保存新的IP
            print("IP地址更新成功")
        else:
            print("IP地址更新失败")
```

#### 5. 注销GPU服务器

GPU服务器关闭时需要注销：

```bash
# 使用测试客户端注销
python3 test_b_client.py unregister \
  --gateway https://www.gongjuxiang.work \
  --server-id B1 \
  --secret your-secret-password-2024
```

**API调用示例**：
```bash
curl -X POST https://www.gongjuxiang.work/webhook/unregister \
  -H "Content-Type: application/json" \
  -d '{
    "server_id": "B1",
    "secret": "your-secret-password-2024"
  }'
```

### 负载均衡机制

#### 顺序轮询策略
- **B1 → B2 → B3 → B1**：按顺序轮流分配请求
- **故障跳过**：自动跳过不健康的服务器
- **动态调整**：服务器上线/下线时自动调整

#### 健康检测
- **检测间隔**：30秒
- **失败阈值**：3次失败后标记为不可用
- **自动恢复**：服务器恢复后自动重新上线

### 配置管理

#### A服务器配置
```bash
# 设置共享密钥
export WEBHOOK_SECRET="your-secret-password-2024"

# 启用多GPU服务器模式
curl -X POST https://www.gongjuxiang.work/api/v1/config/multi-backend \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'
```

#### 查看GPU服务器状态
```bash
# 查看所有GPU服务器
python3 test_b_client.py list \
  --gateway https://www.gongjuxiang.work \
  --secret your-secret-password-2024

# 通过API查看
curl "https://www.gongjuxiang.work/webhook/servers?secret=your-secret-password-2024"
```

### 故障处理

#### GPU服务器故障
- **自动检测**：30秒内检测到服务器离线
- **负载转移**：自动停止向故障服务器分发请求
- **自动恢复**：服务器恢复后自动重新加入负载均衡

#### 所有GPU服务器故障
- **服务降级**：返回503错误"服务暂时不可用"
- **用户提示**：提示用户稍后重试
- **自动恢复**：GPU服务器上线后立即恢复服务

### 安全机制

#### 身份验证
- **预设密码**：GPU服务器调用时在请求体中携带密码
- **HTTPS传输**：所有通信都通过HTTPS加密
- **密码验证**：A服务器验证密码后才允许注册

#### 访问控制
- **Webhook端点**：只有知道密码的GPU服务器可以调用
- **管理端点**：支持可选的密码验证
- **日志记录**：记录所有注册和注销操作

## ✨ 功能特性

### 🖼️ 图片处理
- **多格式支持**: 支持 JPG、JPEG、AVIF 格式图片上传和增强
- **AVIF转换**: 自动将AVIF格式转换为JPG格式进行处理
- **单张处理**: 支持单张图片上传和增强
- **批量处理**: 支持同时上传多张图片进行批量增强
- **超分辨率增强**: 将低分辨率照片提升至高分辨率
- **实时进度**: 显示处理进度和状态
- **实时显示**: 批量处理时每张图片完成立即显示结果

### 📊 用户体验
- **对比展示**: 原图与处理后图片的对比显示
- **全屏查看**: 支持全屏模式查看处理结果
- **拖拽上传**: 支持拖拽文件到上传区域
- **响应式设计**: 适配各种设备屏幕

### 💾 下载功能
- **单张下载**: 支持下载单张处理后的图片
- **批量下载**: 支持一键下载所有处理完成的图片
- **真正缓存下载**: 从浏览器内存下载，避免二次服务器请求
- **分批下载**: 智能分批下载，避免浏览器阻塞
- **文件大小显示**: 显示处理后的图片大小而非原图大小

### ⚡ 性能优化
- **Base64编码优化**: 分批编码预览，解决CPU压力问题
- **并发控制**: 可配置的并发处理数量
- **内存管理**: 智能内存释放，避免内存泄漏
- **快速处理**: 单张图片处理时间约 1 分钟内
- **实时显示**: 批量处理时每张图片完成立即显示，无需等待全部完成
- **服务器图片缓存**: 处理完成后立即下载并转换为Base64存储

### 🔧 配置管理
- **统一API配置**: 集中管理服务器地址和API端点
- **动态配置**: 支持运行时修改服务器地址
- **环境适配**: 支持开发和生产环境配置
- **无硬编码**: 移除所有硬编码的IP地址和URL
- **灵活更新**: 支持多种方式动态更新后端服务地址

## 🛠️ 技术栈

### 前端 (Web页面)
- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 快速的前端构建工具
- **TypeScript** - 类型安全的 JavaScript
- **Tailwind CSS** - 实用优先的 CSS 框架

### 后端服务
- **Flask** - Python Web框架 (API网关服务)
- **FastAPI** - 现代、快速的 Python Web 框架 (GPU服务器)
- **Python** - 后端开发语言
- **Nginx** - 反向代理和HTTPS支持

### 微信小程序
- **微信小程序原生开发** - "喵喵美颜"小程序
- **微信支付API** - 完整的支付流程集成
- **HTTPS API调用** - 通过API网关服务

## 🚀 快速开始

### 环境要求
- Node.js 16+ 
- npm 或 yarn
- Python 3.8+ (后端服务)
- 服务器端口 8000 已开放

### 前端开发

#### 安装依赖
```bash
cd PhotoEnhanceAI-web
npm install
```

#### 启动开发服务器
```bash
npm run dev
```

访问 `http://localhost:5173` 查看应用

#### 构建生产版本
```bash
npm run build
```

### 后端服务

#### 环境准备
```bash
# 安装 Python 依赖
pip install fastapi uvicorn python-multipart pillow opencv-python

# 安装API网关依赖
pip install flask flask-cors requests
```

#### 配置环境变量
```bash
# 设置微信支付环境变量
export WECHAT_MCH_ID="你的商户号"
export WECHAT_APPID="你的小程序APPID"
export WECHAT_SECRET="你的小程序Secret"
export WECHAT_API_KEY="你的微信支付API密钥"
export WECHAT_NOTIFY_URL="https://www.gongjuxiang.work/api/wechat/pay/notify/"

# 设置多GPU服务器管理环境变量
export WEBHOOK_SECRET="your-secret-password-2024"
```

#### 启动后端服务
```bash
# 启动 FastAPI 服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 启动API网关服务（包含微信支付功能和多GPU服务器管理）
cd api-gateway
python3 app.py
```

### GPU服务器部署

#### 1. 安装依赖
```bash
pip install requests psutil
```

#### 2. 配置环境变量
```bash
export SERVER_ID="B1"
export GATEWAY_URL="https://www.gongjuxiang.work"
export SHARED_SECRET="your-secret-password-2024"
export PORT="8000"
```

#### 3. 运行GPU服务器客户端
```bash
python3 test_b_client.py register --server-id B1 --ip 192.168.1.100
```

#### 4. 系统服务部署
```bash
# 创建systemd服务
sudo nano /etc/systemd/system/b-server-client.service

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable b-server-client
sudo systemctl start b-server-client
```

## 📁 项目结构

```
PhotoEnhanceAI-web/
├── api-gateway/             # API网关服务 (Flask)
│   ├── app.py              # Flask网关应用主文件
│   ├── config.py           # 配置管理模块
│   ├── backend_manager.py  # GPU服务器管理核心
│   ├── webhook_routes.py   # Webhook路由处理
│   ├── test_b_client.py    # GPU服务器测试客户端
│   ├── wechat_pay_config.py # 微信支付配置
│   ├── wechat_pay_api.py   # 微信支付API路由
│   ├── wechat_pay_utils.py # 微信支付工具类
│   ├── wechat_auth.py      # 微信登录认证
│   ├── order_manager.py    # 订单管理
│   ├── requirements.txt    # Python依赖
│   ├── deploy_guide.md     # 部署指南
│   ├── wechat_config_template.json # 配置模板
│   └── README.md          # API网关文档
├── src/
│   ├── components/           # Vue 组件
│   │   ├── BatchImageUploader.vue    # 批量图片上传组件
│   │   ├── BatchResultViewer.vue     # 批量结果查看组件
│   │   ├── ImageComparison.vue       # 图片对比组件
│   │   ├── ImageUploader.vue         # 单张图片上传组件
│   │   └── LoadingSpinner.vue        # 加载动画组件
│   ├── views/               # 页面视图
│   │   ├── HomeView.vue             # 主页视图
│   │   └── AboutView.vue            # 关于页面
│   ├── services/            # API 服务
│   │   └── api.ts                  # API 接口封装
│   ├── config/              # 配置文件
│   │   ├── api.ts                  # API 配置管理
│   │   └── batchProcessing.ts      # 批量处理配置
│   ├── utils/               # 工具函数
│   │   ├── imageConverter.ts        # 图片格式转换工具
│   │   ├── imageDownloader.ts       # 图片下载工具
│   │   └── imageSize.ts            # 图片大小计算工具
│   ├── assets/              # 静态资源
│   │   ├── custom.css              # 自定义样式
│   │   └── main.css                # 主样式文件
│   └── router/              # 路由配置
├── public/                  # 公共资源
├── dist/                    # 构建输出
├── package.json             # 项目依赖配置
├── vite.config.ts           # Vite 构建配置
├── tsconfig.json            # TypeScript 配置
└── README.md                # 项目说明文档
```

## 🔧 API 接口

### 系统架构

```
微信小程序"喵喵美颜" 
    ↓ HTTPS API调用
A服务器 (API网关)
    ↓ 负载均衡
GPU服务器集群 (FastAPI + GFPGAN)
    ├── B1: 192.168.1.100:8000
    ├── B2: 192.168.1.101:8000
    └── B3: 192.168.1.102:8000
```

### API网关服务

本项目实现了API网关服务，为微信小程序等外部应用提供HTTPS API接口。网关服务支持多GPU服务器负载均衡，解决小程序只能调用HTTPS接口的限制。

**网关地址**: `https://gongjuxiang.work/api/v1/`

**核心作用**：
- **HTTPS合规**：为小程序提供HTTPS接口
- **域名备案**：使用已备案的域名
- **负载均衡**：自动分发请求到多个GPU服务器
- **支付集成**：集成微信支付功能
- **动态管理**：支持GPU服务器动态注册和管理

### 微信支付API接口

本项目集成了微信小程序支付功能，提供完整的支付流程API。

**微信支付网关地址**: `https://gongjuxiang.work/api/wechat/`

#### 环境变量配置

微信支付功能需要配置以下环境变量：

```bash
# 微信支付配置
export WECHAT_MCH_ID="你的商户号"
export WECHAT_APPID="你的小程序APPID"
export WECHAT_SECRET="你的小程序Secret"
export WECHAT_API_KEY="你的微信支付API密钥"
export WECHAT_NOTIFY_URL="https://www.gongjuxiang.work/api/wechat/pay/notify/"

# 多GPU服务器管理配置
export WEBHOOK_SECRET="your-secret-password-2024"
```

#### 证书文件配置

微信支付需要以下证书文件，请放置在指定路径：

**证书文件路径**：
- 项目根目录：`certificates/`
- API网关目录：`api-gateway/certs/`

**必需证书文件**：
- `apiclient_cert.pem` - 微信支付证书
- `apiclient_key.pem` - 微信支付私钥
- `wechatpay_*.pem` - 微信支付平台证书（可选）

**证书文件获取**：
1. 登录微信商户平台
2. 进入"账户中心" -> "API安全"
3. 下载API证书和私钥
4. 将证书文件放置在上述路径中

**安全提醒**：
- 证书文件已添加到 `.gitignore`，不会提交到版本控制
- 请妥善保管证书文件，不要泄露给他人
- 生产环境建议使用环境变量管理敏感信息

### 图片增强处理接口
```
POST /api/v1/enhance
Content-Type: multipart/form-data

参数:
- file: 图片文件 (JPG、JPEG、AVIF 格式)
- tile_size: 瓦片大小 (可选，默认400)
- quality_level: 质量等级 (可选，默认high)

返回:
- task_id: 任务ID (异步处理)
- status: 任务状态
```

### 任务状态查询接口
```
GET /api/v1/status/{taskId}

返回:
- status: 任务状态 (queued/processing/completed/failed)
- progress: 处理进度 (0-1)
- download_url: 下载链接 (完成时)
- error: 错误信息 (失败时)
```

### 结果下载接口
```
GET /api/v1/download/{taskId}

返回:
- 直接返回处理后的图片文件
- Content-Type: image/jpeg
- Content-Disposition: attachment
```

### 健康检查接口
```
GET /api/v1/health

返回:
- status: 服务状态 (healthy/unhealthy)
- backend_status: 后端连接状态
- timestamp: 检查时间戳
```

### API信息接口
```
GET /api/v1/info

返回:
- name: API网关名称
- version: 版本号
- description: 描述信息
- endpoints: 支持的接口列表
- backend_servers: GPU服务器统计信息
- config_info: 配置信息
```

### 配置管理接口
```
GET /api/v1/config

返回:
- backend_url: 当前使用的后端服务地址
- default_backend_url: 默认后端服务地址
- timeout: 超时时间
- max_file_size: 最大文件大小
- endpoints: 支持的端点
- multi_backend: 多GPU服务器配置
- backend_servers: GPU服务器统计信息
```

### 更新后端地址接口
```
POST /api/v1/config/backend
Content-Type: application/json

参数:
- backend_url: 新的默认后端服务地址

返回:
- message: 更新结果消息
- new_backend_url: 新的后端地址
- timestamp: 更新时间戳
```

### 多GPU服务器配置接口
```
POST /api/v1/config/multi-backend
Content-Type: application/json

参数:
- enabled: 是否启用多GPU服务器模式
- fallback_to_default: 是否回退到默认配置

返回:
- message: 配置更新结果
- details: 详细更新信息
- config: 当前配置信息
- timestamp: 更新时间戳
```

### Webhook接口

#### GPU服务器注册接口
```
POST /webhook/register
Content-Type: application/json

参数:
- server_id: 服务器ID (例如: B1, B2, B3)
- ip: 服务器IP地址
- port: 服务器端口
- secret: 预设密码

返回:
- success: 是否成功
- message: 结果消息
- server_id: 服务器ID
- ip: 服务器IP
- port: 服务器端口
```

#### GPU服务器注销接口
```
POST /webhook/unregister
Content-Type: application/json

参数:
- server_id: 服务器ID
- secret: 预设密码

返回:
- success: 是否成功
- message: 结果消息
- server_id: 服务器ID
```

#### 查询服务器列表接口
```
GET /webhook/servers?secret=your-secret-password-2024

返回:
- success: 是否成功
- data: 服务器统计信息
  - total_servers: 总服务器数
  - healthy_servers: 健康服务器数
  - unhealthy_servers: 不健康服务器数
  - health_check_running: 健康检查是否运行
  - servers: 服务器详细信息列表
```

### 兼容性说明

- **HTTPS支持**: 所有接口均支持HTTPS访问
- **跨域支持**: 支持CORS跨域请求
- **文件上传**: 支持最大100MB文件上传
- **超时设置**: 处理超时时间5分钟
- **错误处理**: 统一的错误响应格式
- **负载均衡**: 自动在多个GPU服务器间分发请求

## 🎨 界面设计

采用简洁现代的设计风格，使用 Tailwind CSS 实现响应式布局，确保在各种设备上都有良好的用户体验。

## 🚨 故障排除

### GitHub 访问问题

#### 问题：无法推送代码到 GitHub
**症状**：`git push` 时出现连接超时、SSL错误或网络错误

**解决方案**：

1. **修改 Hosts 文件 (推荐)**：
   ```bash
   # 备份原始 hosts 文件
   sudo cp /etc/hosts /etc/hosts.backup
   
   # 添加 GitHub IP 地址
   sudo tee -a /etc/hosts << 'EOF'
   
   # GitHub IP addresses (2025)
   140.82.113.4 github.com
   185.199.108.153 assets-cdn.github.com
   199.232.69.194 github.global.ssl.fastly.net
   140.82.112.3 api.github.com
   EOF
   
   # 刷新 DNS 缓存
   sudo systemctl restart systemd-resolved
   ```

2. **使用 GitHub CLI**：
   ```bash
   # 安装 GitHub CLI
   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
   sudo apt update
   sudo apt install gh
   
   # 登录 GitHub
   gh auth login
   
   # 推送代码
   gh repo sync
   ```

3. **配置 SSH 访问**：
   ```bash
   # 生成 SSH 密钥
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   
   # 查看公钥
   cat ~/.ssh/id_rsa.pub
   
   # 将公钥添加到 GitHub 账户
   # 访问: https://github.com/settings/keys
   
   # 切换到 SSH 方式
   git remote set-url origin git@github.com:Rsers/PhotoEnhanceAI-web.git
   ```

4. **使用镜像站 (备选)**：
   ```bash
   # 尝试不同的镜像站
   git remote set-url origin https://github.com.cnpmjs.org/Rsers/PhotoEnhanceAI-web.git
   # 或
   git remote set-url origin https://hub.fastgit.xyz/Rsers/PhotoEnhanceAI-web.git
   # 或
   git remote set-url origin https://ghproxy.com/https://github.com/Rsers/PhotoEnhanceAI-web.git
   ```

### 端口连接问题

#### 问题：前端无法连接后端 API
**症状**：上传图片后显示"连接失败"或"网络错误"

**解决方案**：
1. **检查 8000 端口是否开放**：
   ```bash
   # 检查端口监听状态
   netstat -tlnp | grep 8000
   
   # 如果显示 "tcp 0.0.0.0:8000"，说明端口已监听
   ```

2. **检查防火墙设置**：
   ```bash
   # Ubuntu/Debian
   sudo ufw status
   sudo ufw allow 8000
   
   # CentOS/RHEL
   sudo firewall-cmd --list-ports
   sudo firewall-cmd --permanent --add-port=8000/tcp
   sudo firewall-cmd --reload
   ```

3. **检查云服务器安全组**：
   - 登录云服务器控制台
   - 进入安全组/防火墙设置
   - 确保 8000 端口已开放，来源为 0.0.0.0/0

4. **测试端口连通性**：
   ```bash
   # 从外部测试端口
   telnet your-server-ip 8000
   
   # 或使用 curl 测试
   curl http://your-server-ip:8000/api/v1/status/test
   ```

### GPU服务器管理问题

#### 问题：GPU服务器注册失败
**症状**：调用注册接口返回401错误或注册失败

**解决方案**：
1. **检查密码设置**：
   ```bash
   # 检查A服务器密码设置
   echo $WEBHOOK_SECRET
   
   # 检查GPU服务器密码设置
   echo $SHARED_SECRET
   ```

2. **测试网络连通性**：
   ```bash
   # 测试A服务器连通性
   curl -X POST https://www.gongjuxiang.work/webhook/register \
     -H "Content-Type: application/json" \
     -d '{"server_id":"test","ip":"127.0.0.1","port":8000,"secret":"your-secret"}'
   ```

3. **检查服务器ID冲突**：
   ```bash
   # 查看已注册的服务器
   curl "https://www.gongjuxiang.work/webhook/servers?secret=your-secret"
   ```

#### 问题：负载均衡不工作
**症状**：请求总是转发到同一台服务器

**解决方案**：
1. **检查多GPU服务器模式**：
   ```bash
   # 启用多GPU服务器模式
   curl -X POST https://www.gongjuxiang.work/api/v1/config/multi-backend \
     -H "Content-Type: application/json" \
     -d '{"enabled": true}'
   ```

2. **检查GPU服务器状态**：
   ```bash
   # 查看GPU服务器健康状态
   python3 test_b_client.py list --secret your-secret
   ```

3. **检查健康检测**：
   ```bash
   # 查看健康检测状态
   curl https://www.gongjuxiang.work/api/v1/info | grep health_check
   ```

### 前端样式修改不生效问题

#### 常见原因及解决方法

1. **CSS 优先级问题**
   - 检查是否有 `!important` 冲突
   - 确认选择器优先级是否正确

2. **浏览器缓存问题**
   - 强制刷新：`Ctrl+F5` (Windows) 或 `Cmd+Shift+R` (Mac)
   - 清除浏览器缓存

3. **热重载问题**
   - 重启开发服务器：`npm run dev`
   - 检查 Vite 配置是否正确

4. **作用域问题**
   - 检查 `<style scoped>` 是否正确应用
   - 确认组件选择器是否匹配

5. **导入问题**
   - 检查 CSS 文件是否正确导入
   - 确认路径是否正确

### 调试技巧
- 使用浏览器开发者工具检查样式是否被应用
- 检查控制台是否有错误信息
- 使用 `console.log` 调试组件状态
- 检查网络面板中的 API 请求状态

## ⚡ 性能优化记录

### 批量下载优化
- **问题**: 下载大量图片时浏览器阻塞
- **解决方案**: 实现分批下载机制
- **配置**: `DOWNLOAD_BATCH_SIZE: 10` (每批10张)
- **效果**: 避免浏览器阻塞，提升用户体验

### 并发控制优化
- **问题**: 服务器压力过大
- **解决方案**: 可配置的并发处理数量
- **配置**: `CONCURRENCY: 1` (并发数1)
- **效果**: 平衡服务器负载和用户体验

### Base64编码优化
- **问题**: 大量图片同时编码导致CPU压力大，风扇加速
- **解决方案**: 分批编码预览
- **配置**: `PREVIEW_BATCH_SIZE: 2` (每批2张)
- **效果**: CPU使用率平稳，解决风扇加速问题

### 缓存优化
- **问题**: 重复从服务器下载已缓存的图片
- **解决方案**: 处理完成后立即下载并转换为Base64存储
- **实现**: 使用 `fetch` + `FileReader` 技术
- **效果**: 避免二次服务器请求，显著减少网络流量

### 实时显示优化
- **问题**: 批量处理时所有图片完成后才显示结果
- **解决方案**: 每张图片处理完成后立即emit更新事件
- **实现**: 添加 `imageProcessed` 事件机制
- **效果**: 用户可以看到图片一张一张地完成处理

### 文件大小显示优化
- **问题**: 显示原图大小而非处理后的图片大小
- **解决方案**: 计算并存储处理后图片的实际大小
- **实现**: Base64图片大小计算算法
- **效果**: 用户看到的是真实的处理后图片大小

### GitHub 访问优化
- **问题**: 国内服务器无法正常推送代码到 GitHub
- **解决方案**: 修改 hosts 文件，直接解析 GitHub IP 地址
- **实现**: 添加 GitHub 官方 IP 地址到 `/etc/hosts`
- **效果**: 成功绕过 DNS 污染，稳定访问 GitHub

### API网关优化
- **问题**: 微信小程序只能调用HTTPS接口，无法直接调用基于IP的API
- **解决方案**: 实现API网关服务，提供HTTPS接口代理
- **实现**: Flask网关 + nginx反向代理 + Let's Encrypt证书
- **效果**: 小程序可以合规调用 `https://gongjuxiang.work/api/v1/` 接口

### 多GPU服务器管理优化
- **问题**: 后端服务IP地址经常变更，需要手动修改配置
- **解决方案**: 实现多GPU服务器管理系统，支持动态注册和负载均衡
- **实现**: Webhook注册 + 负载均衡 + 健康检测 + 动态配置
- **效果**: GPU服务器可以动态注册IP地址，A服务器自动负载均衡，无需手动配置

## 📝 开发计划

### ✅ 已完成功能

#### Web前端
- [x] 前端界面开发 (Vue 3 + TypeScript)
- [x] 图片上传功能
- [x] 图片对比展示
- [x] 结果下载功能
- [x] 批量处理功能
- [x] 性能优化
- [x] 缓存优化
- [x] Base64编码优化
- [x] AVIF格式支持
- [x] 实时显示功能
- [x] 文件大小显示优化

#### API网关服务
- [x] API网关服务实现 (Flask)
- [x] HTTPS证书部署
- [x] 微信小程序兼容性支持
- [x] 动态配置管理系统
- [x] 后端地址灵活更新
- [x] GFPGAN API中转服务
- [x] 多GPU服务器管理系统
- [x] 负载均衡功能
- [x] 健康检测机制
- [x] Webhook注册管理

#### 微信支付集成
- [x] 微信支付API开发
- [x] 订单管理系统
- [x] 支付回调处理
- [x] 用户认证 (openid获取)
- [x] 支付统计功能
- [x] 安全配置管理

#### 部署运维
- [x] 云服务器部署
- [x] GitHub 访问问题解决方案
- [x] Nginx反向代理配置
- [x] SSL证书管理
- [x] 多GPU服务器部署方案

### 🚀 未来计划

#### 功能扩展
- [ ] 更多图片格式支持 (PNG, WebP等)
- [ ] 用户认证系统
- [ ] 图片处理历史记录
- [ ] 移动端适配优化
- [ ] API限流和监控
- [ ] 负载均衡优化

#### 微信小程序"喵喵美颜"
- [ ] 小程序UI优化
- [ ] 更多美颜功能集成
- [ ] 用户使用统计
- [ ] 会员系统开发

#### 技术优化
- [ ] 数据库迁移 (MySQL/PostgreSQL)
- [ ] Redis缓存集成
- [ ] 微服务架构改造
- [ ] Docker容器化部署

## ⚙️ 配置化重构

### 批量处理配置文件 (`src/config/batchProcessing.ts`)

```typescript
export const BATCH_PROCESSING_CONFIG = {
    // 并发处理数量
    CONCURRENCY: 1,
    
    // 处理超时时间（毫秒）
    TIMEOUT: 300000, // 5分钟
    
    // 重试次数
    MAX_RETRIES: 3,
    
    // 重试延迟（毫秒）
    RETRY_DELAY: 1000,
    
    // 支持的图片格式
    SUPPORTED_FORMATS: ['.jpg', '.jpeg', '.avif'],
    
    // 最大文件大小（字节）
    MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
    
    // 最大批量数量
    MAX_BATCH_SIZE: 20,
    
    // 批量下载配置
    DOWNLOAD_BATCH_SIZE: 10, // 每批下载的图片数量
    DOWNLOAD_DELAY: 100, // 每张图片下载间隔（毫秒）
    BATCH_DELAY: 1000, // 批次间延迟（毫秒）
    
    // Base64编码配置
    PREVIEW_BATCH_SIZE: 2, // 预览分批大小（每批2张图片）
} as const
```

### 配置说明

- **CONCURRENCY**: 控制同时处理的图片数量，避免服务器压力过大
- **TIMEOUT**: 单张图片处理超时时间
- **MAX_RETRIES**: 处理失败时的重试次数
- **DOWNLOAD_BATCH_SIZE**: 批量下载时每批的图片数量
- **PREVIEW_BATCH_SIZE**: Base64编码时每批的图片数量，解决CPU压力问题

### API配置文件 (`src/config/api.ts`)

```typescript
export const API_CONFIG = {
    // 服务器地址 - 使用HTTPS网关地址
    BASE_URL: 'https://gongjuxiang.work',
    
    // API 端点
    ENDPOINTS: {
        ENHANCE: '/api/v1/enhance',
        STATUS: '/api/v1/status',
        DOWNLOAD: '/api/v1/download'
    },
    
    // 超时设置
    TIMEOUT: 300000, // 5分钟
    
    // 轮询设置
    POLLING: {
        MAX_ATTEMPTS: 60,
        INTERVAL: 5000 // 5秒
    }
}
```

### 使用方式

```typescript
import { getConcurrency, getDownloadBatchSize } from '@/config/batchProcessing'
import { API_CONFIG, getApiUrl } from '@/config/api'

const concurrency = getConcurrency() // 获取并发数
const batchSize = getDownloadBatchSize() // 获取下载批次大小
const apiUrl = getApiUrl(API_CONFIG.ENDPOINTS.ENHANCE) // 获取完整API URL
```

## 🔧 动态配置管理

### 多GPU服务器管理

当需要添加或管理GPU服务器时，可以通过以下方式：

#### 方式1：使用测试客户端（推荐）

```bash
# 进入API网关目录
cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway

# 注册GPU服务器
python3 test_b_client.py register \
  --server-id B1 \
  --ip 192.168.1.100 \
  --port 8000 \
  --secret your-secret-password-2024

# 查看GPU服务器状态
python3 test_b_client.py list \
  --secret your-secret-password-2024

# 注销GPU服务器
python3 test_b_client.py unregister \
  --server-id B1 \
  --secret your-secret-password-2024
```

#### 方式2：API接口管理

```bash
# 注册GPU服务器
curl -X POST https://www.gongjuxiang.work/webhook/register \
  -H "Content-Type: application/json" \
  -d '{
    "server_id": "B1",
    "ip": "192.168.1.100",
    "port": 8000,
    "secret": "your-secret-password-2024"
  }'

# 查看GPU服务器状态
curl "https://www.gongjuxiang.work/webhook/servers?secret=your-secret-password-2024"

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
        "server_id": os.getenv('SERVER_ID', 'B1'),
        "ip": get_current_ip(),
        "port": int(os.getenv('PORT', '8000')),
        "secret": os.getenv('SHARED_SECRET', 'your-secret-password-2024')
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
python3 test_b_client.py list --secret your-secret-password-2024

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

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

---

*让每一张照片都变得更加清晰* ✨
