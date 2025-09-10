# 照片超分辨率增强工具

一个基于 Vue3 + Vite + TypeScript + Tailwind CSS 的照片超分辨率增强网站前端。

## 功能特性

- 📸 **图片上传**：支持拖拽和点击上传 JPG 格式图片
- 🔍 **超分辨率增强**：将低分辨率图片转换为高清图片（2x增强）
- 👀 **对比显示**：原图与处理后图片并排对比展示
- 💾 **一键下载**：处理完成后可直接下载增强图片
- ⏳ **实时状态**：处理过程中显示加载动画和进度提示
- 📱 **响应式设计**：适配不同屏幕尺寸

## 技术栈

- **前端框架**：Vue 3 (Composition API)
- **构建工具**：Vite
- **类型支持**：TypeScript
- **样式框架**：Tailwind CSS
- **路由管理**：Vue Router
- **HTTP 客户端**：Axios

## 项目结构

```
src/
├── components/           # 组件目录
│   ├── ImageUploader.vue    # 图片上传组件
│   ├── ImageComparison.vue  # 图片对比组件
│   └── LoadingSpinner.vue   # 加载动画组件
├── views/               # 页面视图
│   └── HomeView.vue        # 主页面
├── services/            # 服务层
│   └── api.ts              # API 接口
├── router/              # 路由配置
├── assets/              # 静态资源
└── main.ts              # 应用入口
```

## 开发环境

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## API 接口

### 图片增强接口

**端点**: `POST /enhance`

**请求格式**: `multipart/form-data`

**请求参数**:
- `image`: 图片文件 (JPG格式)

**响应格式**:
```json
{
  "enhanced_image": "data:image/jpeg;base64,..."
}
```

## 部署说明

### 开发模式
- 使用模拟 API 进行开发测试
- 处理时间约 3 秒（模拟）

### 生产模式
- 连接真实的 FastAPI 后端
- 支持实际的图片超分辨率处理

## 浏览器支持

- Chrome (推荐)
- Firefox
- Safari
- Edge

## 许可证

MIT License