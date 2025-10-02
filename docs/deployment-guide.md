# 部署指南

## 环境要求

- Node.js 16+ 
- npm 或 yarn
- Python 3.8+ (后端服务)
- 服务器端口 8000 已开放

## 前端开发

### 安装依赖
```bash
cd PhotoEnhanceAI-web
npm install
```

### 启动开发服务器
```bash
npm run dev
```

访问 `http://localhost:5173` 查看应用

### 构建生产版本
```bash
npm run build
```

## 后端服务

### 环境准备
```bash
# 安装 Python 依赖
pip install fastapi uvicorn python-multipart pillow opencv-python

# 安装API网关依赖
pip install flask flask-cors requests
```

### 配置环境变量
```bash
# 设置微信支付环境变量
export WECHAT_MCH_ID="你的商户号"
export WECHAT_APPID="你的小程序APPID"
export WECHAT_SECRET="你的小程序Secret"
export WECHAT_API_KEY="你的微信支付API密钥"
export WECHAT_NOTIFY_URL="https://www.gongjuxiang.work/api/wechat/pay/notify/"

# 设置多GPU服务器管理环境变量
export WEBHOOK_SECRET="gpu-server-register-to-api-gateway-2024"
```

### 启动后端服务
```bash
# 启动 FastAPI 服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 启动API网关服务（包含微信支付功能和多GPU服务器管理）
cd api-gateway
python3 app.py
```

## GPU服务器部署

### 1. 安装依赖
```bash
pip install requests psutil
```

### 2. 配置环境变量
```bash
export SERVER_ID="GPU-001"
export GATEWAY_URL="https://www.gongjuxiang.work"
export SHARED_SECRET="gpu-server-register-to-api-gateway-2024"
export PORT="8000"
```

### 3. 运行GPU服务器客户端
```bash
python3 test_b_client.py register --server-id GPU-001 --ip GPU服务器的公网IP地址
```

### 4. 系统服务部署
```bash
# 创建systemd服务
sudo nano /etc/systemd/system/b-server-client.service

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable b-server-client
sudo systemctl start b-server-client
```

## 项目结构

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

## 配置化重构

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

## 性能优化记录

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
