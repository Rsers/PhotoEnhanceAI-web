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

## 🚨 重要：前端样式修改不生效问题解决方案

### 问题描述
在开发过程中，经常遇到修改CSS样式后页面没有变化的问题，这是一个常见的前端开发痛点。

### 常见原因和解决方案

#### 1. CSS优先级问题
**问题**：Tailwind CSS 与自定义CSS冲突
```css
/* 错误示例 - Tailwind类可能被覆盖 */
<div class="bg-white text-black custom-style">
```
**解决方案**：
- 使用 `!important` 强制应用样式
- 调整CSS选择器优先级
- 使用Vue的scoped样式

#### 2. 样式缓存问题
**问题**：浏览器缓存导致样式不更新
**解决方案**：
```bash
# 清除浏览器缓存
Ctrl + F5 (Windows) / Cmd + Shift + R (Mac)

# 或者硬刷新
Ctrl + Shift + R (Windows) / Cmd + Shift + R (Mac)
```

#### 3. 热重载失效
**问题**：Vite开发服务器热重载不工作
**解决方案**：
```bash
# 重启开发服务器
npm run dev

# 或者强制重启
pkill -f "npm run dev"
npm run dev
```

#### 4. CSS作用域问题
**问题**：样式没有正确应用到目标元素
**解决方案**：
```vue
<!-- 使用scoped样式 -->
<style scoped>
.custom-style {
  color: red;
}
</style>

<!-- 或者使用深度选择器 -->
<style scoped>
:deep(.nested-element) {
  color: blue;
}
</style>
```

#### 5. 样式文件导入问题
**问题**：CSS文件没有正确导入
**解决方案**：
```vue
<!-- 在组件中导入样式 -->
<style scoped>
@import '@/assets/custom.css';
</style>
```

### 调试技巧

#### 1. 使用浏览器开发者工具
- 按F12打开开发者工具
- 检查Elements面板中的样式
- 查看Computed面板确认最终样式
- 使用Styles面板调试样式

#### 2. 检查样式加载
```bash
# 检查网络面板确认CSS文件加载
Network -> CSS -> 查看状态码
```

#### 3. 使用Vue DevTools
- 安装Vue DevTools浏览器扩展
- 检查组件的样式绑定
- 查看响应式数据变化

### 最佳实践

#### 1. 样式组织
```vue
<template>
  <div class="component-wrapper">
    <!-- 使用语义化的类名 -->
    <div class="header-section">
      <h1 class="main-title">标题</h1>
    </div>
  </div>
</template>

<style scoped>
/* 使用BEM命名规范 */
.component-wrapper {
  /* 组件根样式 */
}

.header-section {
  /* 区块样式 */
}

.main-title {
  /* 元素样式 */
}
</style>
```

#### 2. 样式优先级管理
```css
/* 1. 基础样式 */
.base-style {
  color: black;
}

/* 2. 组件样式 */
.component-style {
  color: blue;
}

/* 3. 状态样式 */
.component-style.active {
  color: red;
}

/* 4. 重要样式 */
.component-style.important {
  color: green !important;
}
```

#### 3. 响应式设计
```css
/* 移动端优先 */
.responsive-element {
  font-size: 14px;
}

/* 平板端 */
@media (min-width: 768px) {
  .responsive-element {
    font-size: 16px;
  }
}

/* 桌面端 */
@media (min-width: 1024px) {
  .responsive-element {
    font-size: 18px;
  }
}
```

### 常见错误示例

#### ❌ 错误做法
```vue
<!-- 1. 样式冲突 -->
<div class="bg-white text-black" style="color: red !important;">

<!-- 2. 作用域混乱 -->
<style>
.global-style { color: blue; }
</style>

<!-- 3. 缓存问题 -->
<!-- 修改样式后不刷新浏览器 -->
```

#### ✅ 正确做法
```vue
<!-- 1. 清晰的样式层次 -->
<div class="component-wrapper">
  <div class="content-section">
    <h1 class="title">标题</h1>
  </div>
</div>

<!-- 2. 使用scoped样式 -->
<style scoped>
.component-wrapper {
  background: white;
}

.content-section {
  padding: 20px;
}

.title {
  color: black;
  font-size: 24px;
}
</style>
```

### 故障排除清单

- [ ] 检查浏览器缓存（硬刷新）
- [ ] 重启开发服务器
- [ ] 检查CSS文件是否正确导入
- [ ] 使用浏览器开发者工具检查样式
- [ ] 确认CSS选择器优先级
- [ ] 检查Vue组件的作用域
- [ ] 验证样式语法是否正确
- [ ] 检查是否有JavaScript错误影响渲染

### 项目中的实际案例

#### 案例1：批量处理组件样式问题
**问题**：批量处理组件的样式与单张处理不一致
**解决方案**：
- 移除所有Tailwind CSS类
- 使用自定义CSS类
- 导入统一的样式文件

#### 案例2：模式切换组件颜色对比度问题
**问题**：未选中状态的文字几乎看不见
**解决方案**：
- 改用深色文字 + 浅色背景
- 增加背景透明度
- 添加边框增强可见性

#### 案例3：标签重叠问题
**问题**：批量处理结果中的标签重叠
**解决方案**：
- 调整标签位置（left/right）
- 使用z-index控制层级
- 优化标签尺寸和间距

#### 案例4：批量下载重复请求问题
**问题**：批量下载功能重复从服务器下载图片
**解决方案**：
- 实现本地缓存下载机制
- 使用fetch + URL.createObjectURL
- 添加错误处理和回退机制

#### 案例5：批量处理并发数优化
**问题**：并发数过高导致服务器压力大
**解决方案**：
- 将并发数从3改为1
- 实现顺序处理，避免服务器过载
- 提高处理稳定性和成功率

### 性能优化记录

#### 批量下载优化
- **问题**：每张图片被下载两次（处理时一次，用户下载时一次）
- **影响**：服务器压力大，网络浪费，用户体验差
- **解决**：实现本地缓存下载，避免重复请求
- **效果**：减少50%网络传输，提升下载速度和稳定性

#### 并发数优化
- **问题**：并发数3导致服务器压力大
- **影响**：可能造成服务器过载，处理失败率高
- **解决**：将并发数改为1，实现顺序处理
- **效果**：服务器压力显著降低，处理稳定性提升

#### 配置化重构
- **问题**：硬编码的并发数分散在多个文件中
- **影响**：维护困难，容易出错，配置不统一
- **解决**：创建统一配置文件，消除硬编码
- **效果**：配置集中管理，提高可维护性和可配置性

### 配置文件说明

#### 批量处理配置
**文件位置**：`src/config/batchProcessing.ts`

```typescript
/**
 * 批量处理配置
 */
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
    SUPPORTED_FORMATS: ['.jpg', '.jpeg'],
    
    // 最大文件大小（字节）
    MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
    
    // 最大批量数量
    MAX_BATCH_SIZE: 20
} as const
```

#### 配置项说明
- **CONCURRENCY**: 并发处理数量，控制同时处理的图片数量
- **TIMEOUT**: 处理超时时间，防止处理时间过长
- **MAX_RETRIES**: 最大重试次数，处理失败时的重试次数
- **RETRY_DELAY**: 重试延迟时间，重试之间的等待时间
- **SUPPORTED_FORMATS**: 支持的图片格式列表
- **MAX_FILE_SIZE**: 最大文件大小限制
- **MAX_BATCH_SIZE**: 最大批量处理数量

#### 使用方法
```typescript
// 导入配置
import { getConcurrency } from '@/config/batchProcessing'

// 使用配置
const concurrency = getConcurrency()
```

#### 配置优势
- **集中管理**：所有配置在一个文件中
- **类型安全**：使用TypeScript确保类型安全
- **易于维护**：修改配置只需要改一个地方
- **避免遗漏**：不会忘记同步修改
- **支持扩展**：可以轻松添加新的配置项

## 许可证

MIT License

MIT License

MIT License