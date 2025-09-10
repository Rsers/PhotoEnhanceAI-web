<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 页面标题 -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">照片超分辨率增强</h1>
        <p class="text-lg text-gray-600">将您的低分辨率图片转换为高清图片</p>
      </div>

      <!-- 主要功能区域 -->
      <div class="bg-white rounded-xl shadow-lg p-8">
        <!-- 上传区域 -->
        <div v-if="!originalImage" class="mb-8">
          <ImageUploader @upload="handleImageUpload" :loading="processing" />
        </div>

        <!-- 图片对比区域 -->
        <div v-if="originalImage" class="mb-8">
          <ImageComparison :originalImage="originalImage" :enhancedImage="enhancedImage" :processing="processing"
            @reset="resetImages" @download="downloadImage" />
        </div>

        <!-- 处理按钮 -->
        <div v-if="originalImage && !enhancedImage && !processing" class="text-center">
          <button @click="enhanceImage"
            class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition duration-200 ease-in-out transform hover:scale-105">
            开始增强图片
          </button>
        </div>

        <!-- 加载状态 -->
        <div v-if="processing" class="text-center py-8">
          <LoadingSpinner />
          <p class="text-gray-600 mt-4">正在处理您的图片，请稍候...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import ImageUploader from '@/components/ImageUploader.vue'
  import ImageComparison from '@/components/ImageComparison.vue'
  import LoadingSpinner from '@/components/LoadingSpinner.vue'
  import { enhanceImageAPI, mockEnhanceImageAPI } from '@/services/api'

  const originalImage = ref < string > ('')
  const enhancedImage = ref < string > ('')
  const processing = ref(false)

  const handleImageUpload = (imageDataUrl: string) => {
    originalImage.value = imageDataUrl
    enhancedImage.value = ''
  }

  const enhanceImage = async () => {
    if (!originalImage.value) return

    processing.value = true
    try {
      // 开发环境使用模拟 API，生产环境使用真实 API
      const response = process.env.NODE_ENV === 'development'
        ? await mockEnhanceImageAPI(originalImage.value)
        : await enhanceImageAPI(originalImage.value)
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