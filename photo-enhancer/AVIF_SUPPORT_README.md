# AVIF 格式支持说明

## 新增功能

现在系统支持上传和处理 AVIF 格式的图片！

### 支持的格式

- ✅ **JPG** - 传统JPEG格式
- ✅ **JPEG** - 传统JPEG格式  
- ✅ **AVIF** - 新一代图片格式（自动转换为JPG）

### AVIF 转换流程

1. **检测格式**：系统自动检测上传的文件是否为AVIF格式
2. **本地转换**：在浏览器中将AVIF转换为JPG格式
3. **继续处理**：转换后的JPG图片进入正常的AI增强流程

### 技术实现

#### 转换工具 (`src/utils/imageConverter.ts`)

- `convertAvifToJpg()` - 核心转换函数
- `isAvifFile()` - 检测AVIF格式
- `isSupportedImageFormat()` - 检查支持的格式
- `getFileFormatDisplayName()` - 获取格式显示名称

#### 支持的组件

- **单张处理**：`ImageUploader.vue`
- **批量处理**：`BatchImageUploader.vue`  
- **主页面**：`HomeView.vue`

### 用户体验

#### 单张处理模式
- 上传AVIF文件时显示转换进度
- 转换完成后自动进入处理流程
- 错误处理和用户提示

#### 批量处理模式
- 支持混合格式（JPG + AVIF）
- 自动识别并转换AVIF文件
- 批量转换优化

### 浏览器兼容性

AVIF转换需要浏览器支持：
- ✅ Chrome 85+
- ✅ Firefox 93+
- ✅ Safari 16+
- ❌ 较老版本浏览器可能不支持

### 错误处理

如果AVIF转换失败：
1. 显示详细错误信息
2. 建议用户使用JPG格式
3. 不会影响其他文件的处理

### 性能优化

- **本地转换**：在浏览器中完成，不占用服务器资源
- **批量处理**：支持并发转换多个AVIF文件
- **内存管理**：自动清理临时对象URL

### 使用示例

```typescript
// 检测AVIF格式
if (isAvifFile(file)) {
  const result = await convertAvifToJpg(file)
  if (result.success) {
    // 使用转换后的JPG数据
    processImage(result.dataUrl)
  }
}
```

### 注意事项

1. **文件大小限制**：AVIF文件同样受10MB限制
2. **质量设置**：转换时使用0.9质量（可调整）
3. **格式输出**：所有输出都是JPG格式
4. **浏览器支持**：需要现代浏览器支持AVIF解码

现在您可以上传AVIF格式的图片，系统会自动转换为JPG格式并继续AI增强处理！
