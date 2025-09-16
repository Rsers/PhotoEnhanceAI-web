# PhotoEnhanceAI - 照片超分辨率增强工具

一个基于 AI 技术的照片超分辨率增强工具，可以将低分辨率照片转换为高分辨率版本，提升图片质量和清晰度。

## ✨ 功能特性

- 🖼️ **照片上传**: 支持 JPG 格式图片上传
- 🔍 **超分辨率增强**: 将低分辨率照片提升至高分辨率
- 📊 **对比展示**: 原图与处理后图片的对比显示
- 💾 **结果下载**: 支持下载处理后的高质量图片
- ⚡ **快速处理**: 单张图片处理时间约 1 分钟内
- 📱 **响应式设计**: 适配各种设备屏幕

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
│   ├── components/     # Vue 组件
│   ├── views/         # 页面视图
│   ├── services/      # API 服务
│   └── assets/        # 静态资源
├── public/            # 公共资源
└── dist/              # 构建输出
```

## 🔧 API 接口

### 照片处理接口
```
POST /api/enhance
Content-Type: multipart/form-data

参数:
- file: 图片文件 (JPG 格式)

返回:
- enhanced_image: 处理后的图片 URL
- original_size: 原始图片尺寸
- enhanced_size: 处理后图片尺寸
```

## 🎨 界面设计

采用简洁现代的设计风格，使用 Tailwind CSS 实现响应式布局，确保在各种设备上都有良好的用户体验。

## 📝 开发计划

- [x] 前端界面开发
- [x] 图片上传功能
- [x] 图片对比展示
- [x] 结果下载功能
- [ ] 后端 API 开发
- [ ] 云服务器部署
- [ ] 性能优化

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

---

*让每一张照片都变得更加清晰* ✨