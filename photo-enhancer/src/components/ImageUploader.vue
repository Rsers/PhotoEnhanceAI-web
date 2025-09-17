<template>
  <div class="w-full">
    <div @drop="handleDrop" @dragover.prevent @dragenter.prevent
      class="relative border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 ease-in-out"
      :class="{
        'border-blue-400 bg-blue-50/50 scale-105': dragOver,
        'border-gray-300 hover:border-blue-300 hover:bg-blue-50/30': !dragOver
      }" @dragenter="dragOver = true" @dragleave="dragOver = false">
      <!-- 背景装饰 -->
      <div
        class="absolute inset-0 rounded-2xl bg-gradient-to-br from-blue-50/30 via-transparent to-purple-50/30 pointer-events-none">
      </div>

      <div class="relative z-10 flex flex-col items-center justify-center space-y-6">
        <!-- 图标区域 -->
        <div class="relative">
          <div
            class="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-xl transform transition-transform duration-300"
            :class="{ 'scale-110 rotate-3': dragOver }">
            <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
            </svg>
          </div>
          <!-- 装饰圆环 -->
          <div class="absolute -inset-2 rounded-2xl border-2 border-dashed border-blue-300/50 animate-pulse"
            :class="{ 'border-blue-500': dragOver }"></div>
        </div>

        <!-- 文字内容 -->
        <div class="space-y-4">
          <h3 class="text-2xl font-bold text-gray-800">
            {{ converting ? '正在转换AVIF格式...' : (dragOver ? '释放以上传图片' : '上传您的照片') }}
          </h3>
          <div class="space-y-2">
            <p v-if="converting" class="text-lg text-blue-600 flex items-center justify-center space-x-2">
            <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            <span>正在将AVIF转换为JPG格式，请稍候...</span>
            </p>
            <div v-else>
              <p class="text-lg text-gray-600">
                拖拽图片到此处，或点击下方按钮选择文件
              </p>
              <p class="text-sm text-gray-500 flex items-center justify-center space-x-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>支持 JPG、JPEG、AVIF 格式，建议文件大小不超过 10MB</span>
              </p>
            </div>
          </div>
        </div>

        <!-- 上传按钮 -->
        <label
          class="group relative inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl cursor-pointer shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 ease-in-out overflow-hidden"
          :class="{ 'opacity-50 cursor-not-allowed': loading }">

          <!-- 按钮背景动画 -->
          <div
            class="absolute inset-0 bg-gradient-to-r from-blue-700 to-purple-700 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          </div>

          <!-- 按钮内容 -->
          <div class="relative flex items-center space-x-2">
            <svg class="w-5 h-5 group-hover:animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6">
              </path>
            </svg>
            <span>{{ loading ? '处理中...' : '选择图片文件' }}</span>
          </div>

          <input type="file" class="hidden" accept=".jpg,.jpeg,.avif" @change="handleFileSelect" :disabled="loading" />
        </label>

        <!-- 功能说明 -->
        <div class="flex items-center justify-center space-x-8 text-sm text-gray-500 pt-4">
          <div class="flex items-center space-x-2">
            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>安全上传</span>
          </div>
          <div class="flex items-center space-x-2">
            <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
            <span>快速处理</span>
          </div>
          <div class="flex items-center space-x-2">
            <div class="w-2 h-2 bg-purple-500 rounded-full"></div>
            <span>高质量输出</span>
          </div>
        </div>
      </div>

      <!-- 拖拽遮罩 -->
      <div v-if="dragOver"
        class="absolute inset-0 bg-blue-500/10 rounded-2xl flex items-center justify-center pointer-events-none">
        <div class="bg-white/90 backdrop-blur-sm rounded-xl px-6 py-3 shadow-lg">
          <p class="text-blue-600 font-semibold">释放以上传图片</p>
        </div>
      </div>
    </div>

    <!-- 支持格式提示 -->
    <div class="mt-6 text-center">
      <div
        class="inline-flex items-center space-x-4 px-6 py-3 bg-white/50 backdrop-blur-sm rounded-full border border-white/20 shadow-sm">
        <div class="flex items-center space-x-2">
          <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          <span class="text-sm font-medium text-gray-700">支持格式：</span>
        </div>
        <div class="flex items-center space-x-3">
          <span class="px-2 py-1 bg-orange-100 text-orange-700 text-xs font-medium rounded-md">JPG</span>
          <span class="px-2 py-1 bg-orange-100 text-orange-700 text-xs font-medium rounded-md">JPEG</span>
          <span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded-md">AVIF</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { convertAvifToJpg, isAvifFile, isSupportedImageFormat } from '@/utils/imageConverter'

  interface Props {
    loading?: boolean
  }

  interface Emits {
    (e: 'upload', imageDataUrl: string): void
  }

  defineProps < Props > ()
  const emit = defineEmits < Emits > ()

  const dragOver = ref(false)
  const converting = ref(false)

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

  const handleFile = async (file: File) => {
    // 检查文件类型
    if (!isSupportedImageFormat(file)) {
      alert('请选择 JPG、JPEG 或 AVIF 格式的图片文件')
      return
    }

    // 检查文件大小 (10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert('文件大小不能超过 10MB，请选择更小的图片')
      return
    }

    // 如果是AVIF格式，需要先转换
    if (isAvifFile(file)) {
      converting.value = true
      console.log('🔄 检测到AVIF格式，开始转换为JPG...')

      try {
        const result = await convertAvifToJpg(file)

        if (result.success && result.dataUrl) {
          console.log('✅ AVIF转JPG成功')
          emit('upload', result.dataUrl)
        } else {
          console.error('❌ AVIF转换失败:', result.error)
          alert(`AVIF转换失败: ${result.error}`)
        }
      } catch (error) {
        console.error('❌ AVIF转换过程出错:', error)
        alert(`AVIF转换过程出错: ${error}`)
      } finally {
        converting.value = false
      }
    } else {
      // JPG/JPEG格式直接读取
      const reader = new FileReader()
      reader.onload = (e) => {
        const result = e.target?.result as string
        emit('upload', result)
      }
      reader.readAsDataURL(file)
    }
  }
</script>