# PhotoEnhanceAI - 照片超分辨率增强工具

一个基于 AI 技术的照片超分辨率增强工具，可以将低分辨率照片转换为高分辨率版本，提升图片质量和清晰度。支持单张处理和批量处理两种模式。

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

### 安装依赖
```bash
cd photo-enhancer
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

## 📁 项目结构

```
photo-enhancer/
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
└── dist/                    # 构建输出
```

## 🔧 API 接口

### 单张照片处理接口
```
POST /api/enhance
Content-Type: multipart/form-data

参数:
- file: 图片文件 (JPG、JPEG、AVIF 格式)

返回:
- enhanced_image: 处理后的图片 URL
- original_size: 原始图片尺寸
- enhanced_size: 处理后图片尺寸
```

### 批量照片处理接口
```
POST /api/batch/enhance
Content-Type: multipart/form-data

参数:
- files: 图片文件数组 (JPG、JPEG、AVIF 格式)

返回:
- task_ids: 任务ID数组
- status: 处理状态
```

### 任务状态查询接口
```
GET /api/v1/status/{taskId}

返回:
- status: 任务状态 (queued/processing/completed/failed)
- progress: 处理进度 (0-1)
- download_url: 下载链接 (完成时)
```

## 🎨 界面设计

采用简洁现代的设计风格，使用 Tailwind CSS 实现响应式布局，确保在各种设备上都有良好的用户体验。

## 🚨 重要：前端样式修改不生效问题解决方案

### 常见原因及解决方法

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
- [ ] 后端 API 开发
- [ ] 云服务器部署
- [ ] 更多图片格式支持 (PNG, WebP等)

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
    // 服务器地址 - 可以根据需要修改
    BASE_URL: 'http://139.186.166.51:8000',
    
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

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

---

*让每一张照片都变得更加清晰* ✨