<template>
  <div class="main-container">
    <!-- 页面标题 -->
    <div class="title-section">
      <div class="title-icon">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z">
          </path>
        </svg>
      </div>
      <h1 class="main-title">AI 照片超分辨率增强</h1>
      <p class="subtitle">
        使用先进的人工智能技术，将您的低分辨率图片转换为超高清图片，提升图像质量和细节表现
      </p>
    </div>

    <!-- 主卡片 -->
    <div class="main-card">
      <!-- 上传区域 -->
      <div v-if="!originalImage" class="upload-section">
        <div class="upload-area" :class="{ 'drag-over': dragOver }" @drop="handleDrop" @dragover.prevent
          @dragenter.prevent @dragenter="dragOver = true" @dragleave="dragOver = false">
          <div class="upload-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
            </svg>
          </div>
          <h3 class="upload-title">
            {{ dragOver ? '释放以上传图片' : '上传您的照片' }}
          </h3>
          <p class="upload-subtitle">
            拖拽图片到此处，或点击下方按钮选择文件
          </p>
          <label class="upload-button">
            {{ processing ? '处理中...' : '选择图片文件' }}
            <input type="file" style="display: none" accept=".jpg,.jpeg" @change="handleFileSelect"
              :disabled="processing" />
          </label>
        </div>
      </div>

      <!-- 图片对比区域 -->
      <div v-if="originalImage">
        <!-- 操作栏 -->
        <div class="action-bar">
          <div>
            <span style="font-weight: 600; color: #374151;">对比视图</span>
            <span style="margin-left: 1rem; color: #6b7280; font-size: 0.875rem;">
              {{ processing ? '处理中...' : enhancedImage ? '处理完成' : '等待处理' }}
            </span>
          </div>
          <div class="action-buttons">
            <button v-if="enhancedImage && !processing" @click="downloadImage(enhancedImage)"
              class="action-button download-button">
              <svg style="width: 1rem; height: 1rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                </path>
              </svg>
              下载高清图片
            </button>
            <button @click="resetImages" class="action-button reset-button">
              <svg style="width: 1rem; height: 1rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                </path>
              </svg>
              重新上传
            </button>
          </div>
        </div>

        <!-- 左右对比 -->
        <div class="comparison-section">
          <!-- 原图 -->
          <div class="image-panel original-panel">
            <div class="panel-label original-label">原图</div>
            <div class="image-container">
              <img :src="originalImage" alt="原图" />
            </div>
          </div>

          <!-- 分隔线 -->
          <div class="panel-separator"></div>

          <!-- 增强图 -->
          <div class="image-panel enhanced-panel">
            <div class="panel-label enhanced-label">AI 增强</div>
            <div class="image-container">
              <!-- 处理中 -->
              <div v-if="processing" style="text-align: center;">
                <div class="loading-spinner"></div>
                <div class="loading-title">AI 处理中</div>
                <div class="loading-subtitle">正在使用深度学习算法增强图像...</div>
              </div>
              <!-- 等待处理 -->
              <div v-else-if="!enhancedImage" style="text-align: center; color: #6b7280;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
                <div class="loading-title">准备增强</div>
                <div class="loading-subtitle">点击下方按钮开始 AI 处理</div>
              </div>
              <!-- 处理完成 -->
              <img v-else :src="enhancedImage" alt="AI 增强后的图片" />
            </div>
          </div>
        </div>
      </div>

      <!-- 处理按钮 -->
      <div v-if="originalImage && !enhancedImage && !processing" class="process-section">
        <button @click="enhanceImage" class="process-button">
          <svg style="width: 1.25rem; height: 1.25rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
          开始 AI 增强处理
        </button>
      </div>

      <!-- 加载状态 -->
      <div v-if="processing" class="loading-section">
        <div class="loading-spinner"></div>
        <div class="loading-title">AI 正在处理您的图片</div>
        <div class="loading-subtitle">使用深度学习算法增强图像细节，请稍候...</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { mockEnhanceImageAPI } from '@/services/api'

  const originalImage = ref < string > ('')
  const enhancedImage = ref < string > ('')
  const processing = ref(false)
  const dragOver = ref(false)

  const handleImageUpload = (imageDataUrl: string) => {
    originalImage.value = imageDataUrl
    enhancedImage.value = ''
  }

  const handleDrop = (e: DragEvent) => {
    e.preventDefault()
    dragOver.value = false

    const files = e.dataTransfer?.files
    if (files && files.length > 0) {
      handleFile(files[0])
    }
  }

  const handleFileSelect = (e: Event) => {
    const target = e.target as HTMLInputElement
    const files = target.files
    if (files && files.length > 0) {
      handleFile(files[0])
    }
  }

  const handleFile = (file: File) => {
    if (!file.type.startsWith('image/jpeg')) {
      alert('请选择 JPG 格式的图片文件')
      return
    }

    if (file.size > 10 * 1024 * 1024) {
      alert('文件大小不能超过 10MB，请选择更小的图片')
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      const result = e.target?.result as string
      handleImageUpload(result)
    }
    reader.readAsDataURL(file)
  }

  const enhanceImage = async () => {
    if (!originalImage.value) return

    processing.value = true
    try {
      const response = await mockEnhanceImageAPI(originalImage.value)
      enhancedImage.value = response.data.enhanced_image
    } catch (error) {
      console.error('图片增强失败:', error)
      alert('图片处理失败，请重试')
    } finally {
      processing.value = false
    }
  }

  const resetImages = () => {
    originalImage.value = ''
    enhancedImage.value = ''
    processing.value = false
  }

  const downloadImage = (imageUrl: string) => {
    const link = document.createElement('a')
    link.href = imageUrl
    link.download = 'enhanced-image.jpg'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
</script>

<style scoped>
  @import '@/assets/custom.css';
</style>