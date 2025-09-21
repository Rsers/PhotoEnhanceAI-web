# PhotoEnhanceAI - 照片超分辨率增强工具

一个基于 AI 技术的照片超分辨率增强工具，可以将低分辨率照片转换为高分辨率版本，提升图片质量和清晰度。支持单张处理和批量处理两种模式。

> **🚨 部署前必读**：
> - 请确保服务器已开放 **8000 端口**，否则前端无法正常连接后端 API 服务
> - 如果使用国内服务器，推送代码到 GitHub 可能遇到网络问题，请参考 [GitHub 访问问题](#github-访问问题) 解决方案
> 
> 详细配置方法请查看 [服务器部署](#服务器部署) 和 [故障排除](#故障排除) 部分。

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

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 快速的前端构建工具
- **TypeScript** - 类型安全的 JavaScript
- **Tailwind CSS** - 实用优先的 CSS 框架

### 后端 (计划中)
- **FastAPI** - 现代、快速的 Python Web 框架
- **Python** - 后端开发语言

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
```

#### 启动后端服务
```bash
# 启动 FastAPI 服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 服务器部署

#### 端口配置
**⚠️ 重要提醒：请确认服务器已开放 8000 端口**

1. **云服务器安全组配置**：
   - 登录云服务器控制台
   - 进入安全组设置
   - 添加入站规则：端口 8000，协议 TCP，来源 0.0.0.0/0

2. **防火墙配置**：
   ```bash
   # Ubuntu/Debian
   sudo ufw allow 8000
   
   # CentOS/RHEL
   sudo firewall-cmd --permanent --add-port=8000/tcp
   sudo firewall-cmd --reload
   ```

3. **验证端口开放**：
   ```bash
   # 检查端口是否监听
   netstat -tlnp | grep 8000
   
   # 测试端口连通性
   telnet your-server-ip 8000
   ```

#### 生产环境部署
```bash
# 1. 构建前端
npm run build

# 2. 启动后端服务（生产模式）
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# 3. 使用 Nginx 反向代理（可选）
# 配置 Nginx 将 80 端口请求转发到 8000 端口
```

## 📁 项目结构

```
PhotoEnhanceAI-web/
├── api-gateway/             # API网关服务
│   ├── app.py              # Flask网关应用
│   ├── config.py           # 配置管理模块
│   ├── requirements.txt    # Python依赖
│   ├── start.sh           # 启动脚本
│   ├── simple_update.py   # 简单更新工具
│   ├── update_backend.py   # 完整更新工具
│   ├── gateway_config.json # 配置文件
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

### API网关服务

本项目实现了API网关服务，为微信小程序等外部应用提供HTTPS API接口。网关服务自动代理到基于IP的后端服务，解决小程序只能调用HTTPS接口的限制。

**网关地址**: `https://gongjuxiang.work/api/v1/`

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
- backend: 后端服务地址
- config_info: 配置信息
```

### 配置管理接口
```
GET /api/v1/config

返回:
- backend_url: 后端服务地址
- timeout: 超时时间
- max_file_size: 最大文件大小
- endpoints: 支持的端点
- config_file: 配置文件路径
```

### 更新后端地址接口
```
POST /api/v1/config/backend
Content-Type: application/json

参数:
- backend_url: 新的后端服务地址

返回:
- message: 更新结果消息
- new_backend_url: 新的后端地址
- timestamp: 更新时间戳
```

### 兼容性说明

- **HTTPS支持**: 所有接口均支持HTTPS访问
- **跨域支持**: 支持CORS跨域请求
- **文件上传**: 支持最大100MB文件上传
- **超时设置**: 处理超时时间5分钟
- **错误处理**: 统一的错误响应格式

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

### 动态配置优化
- **问题**: 后端服务IP地址经常变更，需要手动修改配置
- **解决方案**: 实现动态配置管理系统，支持多种更新方式
- **实现**: 配置文件管理 + API接口更新 + 命令行工具
- **效果**: 可以随时方便地更新后端服务地址，无需重启整个系统

## 📝 开发计划

- [x] 前端界面开发
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
- [x] API配置统一管理
- [x] 后端 API 开发
- [x] 云服务器部署
- [x] GitHub 访问问题解决方案
- [x] API网关服务实现
- [x] HTTPS证书部署
- [x] 微信小程序兼容性支持
- [x] 动态配置管理系统
- [x] 后端地址灵活更新
- [ ] 更多图片格式支持 (PNG, WebP等)
- [ ] 用户认证系统
- [ ] 图片处理历史记录
- [ ] 移动端适配优化
- [ ] API限流和监控
- [ ] 负载均衡优化

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

### 后端服务地址更新

当后端服务IP地址变更时，可以通过多种方式快速更新配置：

#### 方式1：命令行工具更新（推荐）

```bash
# 进入API网关目录
cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway

# 简单更新（非交互式）
python3 simple_update.py 新IP:8000

# 完整更新工具（支持更多选项）
python3 update_backend.py --url http://新IP:8000
python3 update_backend.py --show  # 查看当前配置
python3 update_backend.py --test http://新IP:8000  # 测试连接
```

#### 方式2：API接口更新

```bash
# 通过HTTPS接口更新
curl -X POST https://gongjuxiang.work/api/v1/config/backend \
  -H "Content-Type: application/json" \
  -d '{"backend_url": "http://新IP:8000"}'

# 查看当前配置
curl https://gongjuxiang.work/api/v1/config
```

#### 方式3：直接编辑配置文件

```bash
# 编辑配置文件
nano /home/ubuntu/PhotoEnhanceAI-web/api-gateway/gateway_config.json

# 配置文件内容示例
{
  "backend_api_base": "http://新IP:8000",
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
# 检查当前配置
python3 /home/ubuntu/PhotoEnhanceAI-web/api-gateway/update_backend.py --show

# 测试后端连接
python3 /home/ubuntu/PhotoEnhanceAI-web/api-gateway/update_backend.py --test http://新IP:8000

# 查看API网关信息
curl https://gongjuxiang.work/api/v1/info | python3 -m json.tool
```

### 使用场景

1. **后端服务迁移**：当后端服务更换服务器时
2. **IP地址变更**：云服务器IP地址更新时
3. **负载均衡**：切换到不同的后端服务实例
4. **故障转移**：主服务故障时切换到备用服务

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

---

*让每一张照片都变得更加清晰* ✨