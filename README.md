# PhotoEnhanceAI - 照片超分辨率增强工具

一个基于 AI 技术的照片超分辨率增强工具，可以将低分辨率照片转换为高分辨率版本，提升图片质量和清晰度。支持单张处理和批量处理两种模式。

## 🎯 项目概述

PhotoEnhanceAI 是一个完整的照片增强解决方案，包含：

- **🌐 Web前端页面** - Vue 3 + TypeScript 构建的现代化界面
- **🔄 API网关服务** - 为微信小程序提供HTTPS接口和负载均衡
- **💳 微信支付集成** - 完整的微信小程序支付后端
- **🔧 多GPU服务器管理** - 动态注册、负载均衡、健康检测

## 🚀 快速开始

### 环境要求
- Node.js 16+ 
- Python 3.8+
- 服务器端口 8000 已开放

### 快速部署
```bash
# 克隆项目
git clone https://github.com/Rsers/PhotoEnhanceAI-web.git
cd PhotoEnhanceAI-web

# 安装前端依赖
npm install

# 安装后端依赖
pip install -r api-gateway/requirements.txt

# 启动开发服务器
npm run dev
```

访问 `http://localhost:5173` 查看应用

## 📚 文档导航

### 📖 详细文档
- **[功能特性](docs/features.md)** - 项目功能详细介绍
- **[部署指南](docs/deployment-guide.md)** - 完整的部署和配置说明
- **[API接口文档](docs/api-reference.md)** - 所有API接口的详细说明
- **[GPU服务器管理](docs/gpu-server-management.md)** - 多GPU服务器管理系统
- **[故障排除](docs/troubleshooting.md)** - 常见问题和解决方案
- **[开发计划](docs/development-roadmap.md)** - 已完成功能和未来规划

### 🔧 核心功能
- **图片增强处理** - 支持JPG、JPEG、AVIF格式，批量处理
- **实时进度显示** - 处理进度实时更新，用户体验优化
- **智能下载管理** - 分批下载，避免浏览器阻塞
- **多GPU负载均衡** - 自动分发请求，故障自动切换
- **微信支付集成** - 完整的支付流程和订单管理

### 🛠️ 技术栈
- **前端**: Vue 3 + TypeScript + Tailwind CSS
- **后端**: Flask (API网关) + FastAPI (GPU服务)
- **部署**: Nginx + Let's Encrypt + Systemd

## ⚠️ 部署前必读

> **重要提醒**：
> - 请确保服务器已开放 **8000 端口**
> - 如果使用国内服务器，推送代码到 GitHub 可能遇到网络问题
> - 详细配置方法请查看 [部署指南](docs/deployment-guide.md)
> - 遇到问题请参考 [故障排除](docs/troubleshooting.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 📄 许可证

MIT License

---

*让每一张照片都变得更加清晰* ✨
