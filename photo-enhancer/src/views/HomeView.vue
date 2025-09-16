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
      <h1 class="main-title">GFPGAN</h1>
      <h1 class="main-title">照片超分辨率增强</h1>
      <h1 class="main-title">人像美化</h1>
      <p class="subtitle">
        使用先进的人工智能技术，将您的低分辨率图片转换为超高清图片，提升图像质量和细节表现
      </p>

      <!-- 模式切换 -->
      <div class="mode-switcher">
        <div class="mode-tabs">
          <button @click="switchMode('single')" :class="{ 'active': currentMode === 'single' }" class="mode-tab">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z">
              </path>
            </svg>
            单张处理
          </button>
          <button @click="switchMode('batch')" :class="{ 'active': currentMode === 'batch' }" class="mode-tab">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10">
              </path>
            </svg>
            批量处理
          </button>
        </div>
      </div>
    </div>

    <!-- 主卡片 -->
    <div class="main-card">
      <!-- 单张处理模式 -->
      <div v-if="currentMode === 'single'">
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
                  <div class="loading-subtitle">{{ processingStatus }}</div>
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
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z">
              </path>
            </svg>
            开始 AI 增强处理
          </button>
        </div>

        <!-- 加载状态 -->
        <div v-if="processing" class="loading-section">
          <div class="loading-spinner"></div>
          <div class="loading-title">AI 正在处理您的图片</div>
          <div class="loading-subtitle">{{ processingStatus }}</div>
        </div>
      </div>

      <!-- 批量处理模式 -->
      <div v-else-if="currentMode === 'batch'" class="batch-mode-container">
        <!-- 批量上传组件 -->
        <div class="batch-upload-section">
          <BatchImageUploader :loading="batchProcessing" @batch-complete="handleBatchComplete" />
        </div>

        <!-- 批量结果展示 -->
        <div v-if="batchResults.length > 0" class="batch-results-section">
          <BatchResultViewer :results="batchResults" @reset="resetBatchMode" @retry="retryBatchImage" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { enhanceImageAPI } from '@/services/api'
  import BatchImageUploader from '@/components/BatchImageUploader.vue'
  import BatchResultViewer from '@/components/BatchResultViewer.vue'

  // 模式切换
  const currentMode = ref < 'single' | 'batch' > ('single')

  // 单张处理相关
  const originalImage = ref < string > ('')
  const enhancedImage = ref < string > ('')
  const processing = ref(false)
  const dragOver = ref(false)
  const processingStatus = ref < string > ('准备中...')

  // 批量处理相关
  const batchProcessing = ref(false)
  const batchResults = ref < any[] > ([])

  // 模式切换
  const switchMode = (mode: 'single' | 'batch') => {
    currentMode.value = mode
    // 切换模式时重置所有状态
    resetImages()
    resetBatchMode()
  }

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
    processingStatus.value = '正在上传图片...'

    try {
      console.log('开始处理图片...')

      // 设置状态更新监听
      const originalLog = console.log
      console.log = (...args) => {
        originalLog(...args)
        const message = args.join(' ')
        if (message.includes('上传进度:')) {
          processingStatus.value = `上传中: ${message.split('上传进度: ')[1]}`
        } else if (message.includes('检测到异步任务')) {
          processingStatus.value = '任务已提交，正在排队处理...'
        } else if (message.includes('开始轮询任务')) {
          processingStatus.value = '任务处理中，正在查询进度...'
        } else if (message.includes('任务状态: queued')) {
          processingStatus.value = '任务排队中，请耐心等待...'
        } else if (message.includes('任务状态: processing')) {
          processingStatus.value = 'AI正在增强图像，请稍候...'
        } else if (message.includes('第') && message.includes('次查询')) {
          const attempt = message.match(/第 (\d+) 次/)?.[1]
          processingStatus.value = `正在查询处理进度 (${attempt}/60)...`
        } else if (message.includes('状态:') && message.includes('%')) {
          // 提取进度信息
          const progressMatch = message.match(/\((\d+\.\d+)%\)/)
          if (progressMatch) {
            processingStatus.value = `AI处理中: ${progressMatch[1]}% 完成`
          }
        } else if (message.includes('任务完成')) {
          processingStatus.value = '处理完成，正在获取结果...'
        }
      }

      // 调用真实的后端API
      const response = await enhanceImageAPI(originalImage.value)

      // 恢复原始console.log
      console.log = originalLog

      console.log('API响应数据:', response.data)

      // 处理各种可能的API响应格式
      let resultImage = null

      if (response.data) {
        // 尝试不同的字段名
        if (response.data.enhanced_image) {
          resultImage = response.data.enhanced_image
        } else if (response.data.result) {
          resultImage = response.data.result
        } else if (response.data.image) {
          resultImage = response.data.image
        } else if (response.data.output) {
          resultImage = response.data.output
        } else if (response.data.url) {
          resultImage = response.data.url
        } else if (typeof response.data === 'string') {
          resultImage = response.data
        } else {
          // 打印完整响应以便调试
          console.log('完整API响应:', response)
          throw new Error(`API返回格式不正确。响应数据: ${JSON.stringify(response.data)}`)
        }
      } else {
        throw new Error('API返回空数据')
      }

      if (resultImage) {
        // 如果返回的不是完整的data URL，需要添加前缀
        if (!resultImage.startsWith('data:')) {
          if (resultImage.startsWith('http')) {
            // 如果是URL，直接使用
            enhancedImage.value = resultImage
          } else {
            // 如果是base64字符串，添加前缀
            enhancedImage.value = `data:image/jpeg;base64,${resultImage}`
          }
        } else {
          enhancedImage.value = resultImage
        }
        console.log('图片增强成功')
      } else {
        throw new Error('未能从API响应中提取图片数据')
      }

    } catch (error) {
      console.error('图片增强失败:', error)
      if (error.response) {
        console.error('错误响应:', error.response.data)
        alert(`图片处理失败：${error.response.data?.message || error.response.data?.detail || '服务器错误'}`)
      } else {
        alert(`图片处理失败：${error.message || '请重试'}`)
      }
    } finally {
      processing.value = false
      processingStatus.value = '准备中...'
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

  // 批量处理相关方法
  const handleBatchComplete = (results: any[]) => {
    batchResults.value = results
    batchProcessing.value = false
  }

  const resetBatchMode = () => {
    batchResults.value = []
    batchProcessing.value = false
  }

  const retryBatchImage = (index: number) => {
    // 重试单张图片的逻辑
    console.log('重试图片:', index)
  }
</script>

<style scoped>
  @import '@/assets/custom.css';

  /* 模式切换样式 */
  .mode-switcher {
    margin-top: 2rem;
    display: flex;
    justify-content: center;
  }

  .mode-tabs {
    display: flex;
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(15px);
    border-radius: 12px;
    padding: 6px;
    border: 1px solid rgba(255, 255, 255, 0.4);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  }

  .mode-tab {
    display: flex;
    align-items: center;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    color: rgba(0, 0, 0, 0.8);
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.5);
    cursor: pointer;
    transition: all 0.3s ease;
    text-shadow: none;
  }

  .mode-tab:hover {
    color: rgba(0, 0, 0, 1);
    background: rgba(255, 255, 255, 1);
    border-color: rgba(255, 255, 255, 0.8);
    text-shadow: none;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .mode-tab.active {
    color: white;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  }

  .mode-tab svg {
    transition: transform 0.2s ease;
  }

  .mode-tab:hover svg {
    transform: scale(1.1);
  }

  /* 批量处理模式样式 - 参考单张处理样式 */
  .batch-mode-container {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
  }

  .batch-upload-section {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px);
    border-radius: 2rem;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 3rem;
    margin-bottom: 2rem;
    overflow: hidden;
  }

  .batch-results-section {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px);
    border-radius: 2rem;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 3rem;
    overflow: hidden;
  }

  /* 响应式设计 */
  @media (max-width: 768px) {

    .batch-upload-section,
    .batch-results-section {
      padding: 1.5rem;
      margin-bottom: 1.5rem;
    }
  }
</style>