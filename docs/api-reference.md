# API接口文档

## 系统架构

```
微信小程序"喵喵美颜" 
    ↓ HTTPS API调用
A服务器 (API网关)
    ↓ 负载均衡
GPU服务器集群 (FastAPI + GFPGAN)
    ├── GPU-001: GPU服务器的公网IP地址:8000
    ├── GPU-002: GPU服务器的公网IP地址:8000
    └── GPU-003: GPU服务器的公网IP地址:8000
```

## API网关服务

本项目实现了API网关服务，为微信小程序等外部应用提供HTTPS API接口。网关服务支持多GPU服务器负载均衡，解决小程序只能调用HTTPS接口的限制。

**网关地址**: `https://gongjuxiang.work/api/v1/`

**核心作用**：
- **HTTPS合规**：为小程序提供HTTPS接口
- **域名备案**：使用已备案的域名
- **负载均衡**：自动分发请求到多个GPU服务器
- **支付集成**：集成微信支付功能
- **动态管理**：支持GPU服务器动态注册和管理

## 微信支付API接口

本项目集成了微信小程序支付功能，提供完整的支付流程API。

**微信支付网关地址**: `https://gongjuxiang.work/api/wechat/`

### 环境变量配置

微信支付功能需要配置以下环境变量：

```bash
# 微信支付配置
export WECHAT_MCH_ID="你的商户号"
export WECHAT_APPID="你的小程序APPID"
export WECHAT_SECRET="你的小程序Secret"
export WECHAT_API_KEY="你的微信支付API密钥"
export WECHAT_NOTIFY_URL="https://www.gongjuxiang.work/api/wechat/pay/notify/"

# 多GPU服务器管理配置
export WEBHOOK_SECRET="gpu-server-register-to-api-gateway-2024"
```

### 证书文件配置

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

## 图片增强处理接口

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

## 任务状态查询接口

```
GET /api/v1/status/{taskId}

返回:
- status: 任务状态 (queued/processing/completed/failed)
- progress: 处理进度 (0-1)
- download_url: 下载链接 (完成时)
- error: 错误信息 (失败时)
```

## 结果下载接口

```
GET /api/v1/download/{taskId}

返回:
- 直接返回处理后的图片文件
- Content-Type: image/jpeg
- Content-Disposition: attachment
```

## 健康检查接口

```
GET /api/v1/health

返回:
- status: 服务状态 (healthy/unhealthy)
- backend_status: 后端连接状态
- timestamp: 检查时间戳
```

## API信息接口

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

## 配置管理接口

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

## 更新后端地址接口

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

## 多GPU服务器配置接口

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

## Webhook接口

### GPU服务器注册接口

```
POST /webhook/register
Content-Type: application/json

参数:
- ip: 服务器公网IP地址
- port: 服务器端口
- secret: 预设密码

返回:
- success: 是否成功
- message: 结果消息
- server_id: A服务器自动分配的服务器ID
- ip: 服务器IP
- port: 服务器端口
```

### GPU服务器注销接口

```
POST /webhook/unregister
Content-Type: application/json

参数:
- ip: 服务器公网IP地址
- port: 服务器端口
- secret: 预设密码

返回:
- success: 是否成功
- message: 结果消息
- server_id: 被注销的服务器ID
```

### 查询服务器列表接口

```
GET /webhook/servers?secret=gpu-server-register-to-api-gateway-2024

返回:
- success: 是否成功
- data: 服务器统计信息
  - total_servers: 总服务器数
  - healthy_servers: 健康服务器数
  - unhealthy_servers: 不健康服务器数
  - health_check_running: 健康检查是否运行
  - servers: 服务器详细信息列表
```

## 兼容性说明

- **HTTPS支持**: 所有接口均支持HTTPS访问
- **跨域支持**: 支持CORS跨域请求
- **文件上传**: 支持最大100MB文件上传
- **超时设置**: 处理超时时间5分钟
- **错误处理**: 统一的错误响应格式
- **负载均衡**: 自动在多个GPU服务器间分发请求
