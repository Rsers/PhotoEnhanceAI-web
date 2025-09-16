<template>
    <div class="batch-uploader">
        <!-- 批量上传区域 -->
        <div @drop="handleDrop" @dragover.prevent @dragenter.prevent class="batch-upload-area"
            :class="{ 'drag-over': dragOver }" @dragenter="dragOver = true" @dragleave="dragOver = false">
            <!-- 背景装饰 -->
            <div class="batch-upload-bg"></div>

            <div class="batch-upload-content">
                <!-- 图标区域 -->
                <div class="batch-upload-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10">
                        </path>
                    </svg>
                </div>

                <!-- 文字内容 -->
                <div class="batch-upload-text">
                    <h3 class="batch-upload-title">
                        {{ dragOver ? '释放以上传图片' : '批量上传照片' }}
                    </h3>
                    <p class="batch-upload-subtitle">
                        拖拽多张图片到此处，或点击下方按钮选择文件
                    </p>
                    <p class="batch-upload-tip">
                        支持多选，仅支持 JPG 格式，每张图片不超过 10MB
                    </p>
                </div>

                <!-- 上传按钮 -->
                <label class="batch-upload-button" :class="{ 'loading': loading }">
                    <span>{{ loading ? '处理中...' : '选择多张图片' }}</span>
                    <input type="file" class="hidden" accept=".jpg,.jpeg" multiple @change="handleFileSelect"
                        :disabled="loading" />
                </label>

                <!-- 功能说明 -->
                <div class="batch-upload-features">
                    <div class="feature-item">
                        <div class="feature-dot green"></div>
                        <span>批量处理</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-dot blue"></div>
                        <span>并行上传</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-dot purple"></div>
                        <span>批量下载</span>
                    </div>
                </div>
            </div>

            <!-- 拖拽遮罩 -->
            <div v-if="dragOver" class="batch-drag-overlay">
                <div class="batch-drag-message">
                    <p>释放以上传多张图片</p>
                </div>
            </div>
        </div>

        <!-- 已选择的图片列表 -->
        <div v-if="selectedImages.length > 0" class="batch-images-section">
            <div class="batch-images-header">
                <div class="batch-images-title">
                    <div class="batch-images-icon">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10">
                            </path>
                        </svg>
                    </div>
                    <h4>已选择 {{ selectedImages.length }} 张图片</h4>
                </div>
                <div class="batch-images-actions">
                    <button @click="clearAllImages" class="batch-action-btn secondary">
                        清空全部
                    </button>
                    <button @click="startBatchProcessing" :disabled="processing || selectedImages.length === 0"
                        class="batch-action-btn primary">
                        {{ processing ? `处理中 (${processingCount}/${selectedImages.length})` : '开始批量处理' }}
                    </button>
                </div>
            </div>

            <!-- 图片网格 -->
            <div class="batch-images-grid">
                <div v-for="(image, index) in selectedImages" :key="index" class="batch-image-item">
                    <!-- 图片预览 -->
                    <div class="batch-image-preview">
                        <img :src="image.preview" :alt="`图片 ${index + 1}`" />

                        <!-- 处理状态覆盖层 -->
                        <div v-if="image.status !== 'pending'" class="batch-image-overlay">
                            <div class="batch-image-status">
                                <div v-if="image.status === 'processing'" class="status-processing">
                                    <div class="status-spinner"></div>
                                    <p>处理中...</p>
                                </div>
                                <div v-else-if="image.status === 'completed'" class="status-completed">
                                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M5 13l4 4L19 7"></path>
                                    </svg>
                                    <p>完成</p>
                                </div>
                                <div v-else-if="image.status === 'error'" class="status-error">
                                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M6 18L18 6M6 6l12 12"></path>
                                    </svg>
                                    <p>失败</p>
                                </div>
                            </div>
                        </div>

                        <!-- 删除按钮 -->
                        <button @click="removeImage(index)" class="batch-image-remove">
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </div>

                    <!-- 图片信息 -->
                    <div class="batch-image-info">
                        <p class="batch-image-name">图片 {{ index + 1 }}</p>
                        <p class="batch-image-size">{{ formatFileSize(image.file.size) }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 批量处理进度 -->
        <div v-if="processing" class="batch-progress-section">
            <div class="batch-progress-header">
                <div class="batch-progress-title">
                    <div class="batch-progress-icon">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                            </path>
                        </svg>
                    </div>
                    <h4>批量处理进度</h4>
                </div>
                <div class="batch-progress-count">
                    {{ processingCount }} / {{ selectedImages.length }}
                </div>
            </div>

            <!-- 进度条 -->
            <div class="batch-progress-bar">
                <div class="batch-progress-fill"
                    :style="{ width: `${(processingCount / selectedImages.length) * 100}%` }"></div>
            </div>

            <!-- 处理状态统计 -->
            <div class="batch-progress-stats">
                <div class="stat-item processing">
                    <div class="stat-number">{{ processingCount }}</div>
                    <div class="stat-label">处理中</div>
                </div>
                <div class="stat-item completed">
                    <div class="stat-number">{{ completedCount }}</div>
                    <div class="stat-label">已完成</div>
                </div>
                <div class="stat-item error">
                    <div class="stat-number">{{ errorCount }}</div>
                    <div class="stat-label">失败</div>
                </div>
                <div class="stat-item pending">
                    <div class="stat-number">{{ pendingCount }}</div>
                    <div class="stat-label">等待中</div>
                </div>
            </div>
        </div>

        <!-- 批量下载按钮 -->
        <div v-if="completedCount > 0" class="batch-download-section">
            <div class="batch-download-card">
                <div class="batch-download-header">
                    <div class="batch-download-icon">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7">
                            </path>
                        </svg>
                    </div>
                    <h3>处理完成！</h3>
                </div>
                <p class="batch-download-text">共有 {{ completedCount }} 张图片处理成功</p>
                <button @click="downloadAllCompleted" class="batch-download-button">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                        </path>
                    </svg>
                    下载所有完成的图片
                </button>
            </div>
        </div>

        <!-- 支持格式提示 -->
        <div class="batch-format-tip">
            <div class="format-tip-content">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <span>支持格式：</span>
                <span class="format-tag">JPG</span>
                <span class="format-tag">JPEG</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, computed } from 'vue'
    import { enhanceImageAPI } from '@/services/api'

    interface ImageItem {
        file: File
        preview: string
        status: 'pending' | 'processing' | 'completed' | 'error'
        enhancedImage?: string
        error?: string
    }

    interface Props {
        loading?: boolean
    }

    interface Emits {
        (e: 'batchComplete', results: ImageItem[]): void
    }

    defineProps < Props > ()
    const emit = defineEmits < Emits > ()

    const selectedImages = ref < ImageItem[] > ([])
    const dragOver = ref(false)
    const processing = ref(false)
    const processingCount = ref(0)

    // 计算属性
    const completedCount = computed(() =>
        selectedImages.value.filter(img => img.status === 'completed').length
    )

    const errorCount = computed(() =>
        selectedImages.value.filter(img => img.status === 'error').length
    )

    const pendingCount = computed(() =>
        selectedImages.value.filter(img => img.status === 'pending').length
    )

    // 处理拖拽
    const handleDrop = (e: DragEvent) => {
        e.preventDefault()
        dragOver.value = false

        const files = e.dataTransfer?.files
        if (files && files.length > 0) {
            handleFiles(Array.from(files))
        }
    }

    // 处理文件选择
    const handleFileSelect = (e: Event) => {
        const target = e.target as HTMLInputElement
        const files = target.files
        if (files && files.length > 0) {
            handleFiles(Array.from(files))
        }
    }

    // 处理多个文件
    const handleFiles = (files: File[]) => {
        const validFiles = files.filter(file => {
            // 检查文件类型
            if (!file.type.startsWith('image/jpeg')) {
                alert(`文件 ${file.name} 不是 JPG 格式，已跳过`)
                return false
            }

            // 检查文件大小
            if (file.size > 10 * 1024 * 1024) {
                alert(`文件 ${file.name} 超过 10MB，已跳过`)
                return false
            }

            return true
        })

        // 为每个有效文件创建预览
        validFiles.forEach(file => {
            const reader = new FileReader()
            reader.onload = (e) => {
                const preview = e.target?.result as string
                selectedImages.value.push({
                    file,
                    preview,
                    status: 'pending'
                })
            }
            reader.readAsDataURL(file)
        })
    }

    // 移除单张图片
    const removeImage = (index: number) => {
        selectedImages.value.splice(index, 1)
    }

    // 清空所有图片
    const clearAllImages = () => {
        selectedImages.value = []
        processing.value = false
        processingCount.value = 0
    }

    // 格式化文件大小
    const formatFileSize = (bytes: number): string => {
        if (bytes === 0) return '0 Bytes'
        const k = 1024
        const sizes = ['Bytes', 'KB', 'MB', 'GB']
        const i = Math.floor(Math.log(bytes) / Math.log(k))
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    // 开始批量处理
    const startBatchProcessing = async () => {
        if (selectedImages.value.length === 0) return

        processing.value = true
        processingCount.value = 0

        // 重置所有图片状态
        selectedImages.value.forEach(img => {
            img.status = 'pending'
            img.enhancedImage = undefined
            img.error = undefined
        })

        // 并发处理所有图片（限制并发数）
        const concurrency = 3 // 同时处理3张图片
        const chunks = []
        for (let i = 0; i < selectedImages.value.length; i += concurrency) {
            chunks.push(selectedImages.value.slice(i, i + concurrency))
        }

        for (const chunk of chunks) {
            await Promise.all(chunk.map(processImage))
        }

        processing.value = false
        emit('batchComplete', selectedImages.value)
    }

    // 处理单张图片
    const processImage = async (imageItem: ImageItem) => {
        try {
            imageItem.status = 'processing'
            processingCount.value++

            // 调用API处理图片
            const response = await enhanceImageAPI(imageItem.preview)

            // 处理API响应
            let resultImage = null
            if (response.data) {
                if (response.data.enhanced_image) {
                    resultImage = response.data.enhanced_image
                } else if (response.data.download_url) {
                    resultImage = response.data.download_url
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
                }
            }

            if (resultImage) {
                // 如果返回的不是完整的data URL，需要添加前缀
                if (!resultImage.startsWith('data:')) {
                    if (resultImage.startsWith('http')) {
                        imageItem.enhancedImage = resultImage
                    } else {
                        imageItem.enhancedImage = `data:image/jpeg;base64,${resultImage}`
                    }
                } else {
                    imageItem.enhancedImage = resultImage
                }
                imageItem.status = 'completed'
            } else {
                throw new Error('未能从API响应中提取图片数据')
            }

        } catch (error: any) {
            console.error('图片处理失败:', error)
            imageItem.status = 'error'
            imageItem.error = error.message || '处理失败'
        }
    }

    // 下载所有完成的图片
    const downloadAllCompleted = () => {
        const completedImages = selectedImages.value.filter(img => img.status === 'completed' && img.enhancedImage)

        completedImages.forEach((imageItem, index) => {
            setTimeout(() => {
                const link = document.createElement('a')
                link.href = imageItem.enhancedImage!
                link.download = `enhanced-image-${index + 1}.jpg`
                document.body.appendChild(link)
                link.click()
                document.body.removeChild(link)
            }, index * 500) // 每500ms下载一张，避免浏览器阻止
        })
    }
</script>

<style scoped>
    /* 批量上传器样式 - 参考单张处理样式 */
    .batch-uploader {
        width: 100%;
    }

    /* 批量上传区域 */
    .batch-upload-area {
        border: 2px dashed #d1d5db;
        border-radius: 1.5rem;
        padding: 3rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        background: linear-gradient(135deg, #f8fafc, #f1f5f9);
    }

    .batch-upload-area:hover {
        border-color: #3b82f6;
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        transform: scale(1.02);
    }

    .batch-upload-area.drag-over {
        border-color: #3b82f6;
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        transform: scale(1.05);
    }

    .batch-upload-bg {
        position: absolute;
        inset: 0;
        border-radius: 1.5rem;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), transparent, rgba(139, 92, 246, 0.1));
        pointer-events: none;
    }

    .batch-upload-content {
        position: relative;
        z-index: 10;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.5rem;
    }

    /* 上传图标 */
    .batch-upload-icon {
        width: 6rem;
        height: 6rem;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        transition: transform 0.3s ease;
    }

    .batch-upload-area:hover .batch-upload-icon {
        transform: rotate(3deg) scale(1.1);
    }

    .batch-upload-icon svg {
        width: 3rem;
        height: 3rem;
        color: white;
    }

    /* 文字内容 */
    .batch-upload-text {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .batch-upload-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
    }

    .batch-upload-subtitle {
        font-size: 1.125rem;
        color: #6b7280;
    }

    .batch-upload-tip {
        font-size: 0.875rem;
        color: #9ca3af;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    /* 上传按钮 */
    .batch-upload-button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 0.75rem;
        font-size: 1.125rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }

    .batch-upload-button:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.6);
    }

    .batch-upload-button.loading {
        opacity: 0.7;
        cursor: not-allowed;
    }

    .batch-upload-button input {
        display: none;
    }

    /* 功能说明 */
    .batch-upload-features {
        display: flex;
        align-items: center;
        gap: 2rem;
        font-size: 0.875rem;
        color: #6b7280;
    }

    .feature-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .feature-dot {
        width: 0.5rem;
        height: 0.5rem;
        border-radius: 50%;
    }

    .feature-dot.green {
        background: #10b981;
    }

    .feature-dot.blue {
        background: #3b82f6;
    }

    .feature-dot.purple {
        background: #8b5cf6;
    }

    /* 拖拽遮罩 */
    .batch-drag-overlay {
        position: absolute;
        inset: 0;
        background: rgba(59, 130, 246, 0.1);
        border-radius: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        pointer-events: none;
    }

    .batch-drag-message {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 0.75rem;
        padding: 1.5rem 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .batch-drag-message p {
        color: #3b82f6;
        font-weight: 600;
    }

    /* 图片列表区域 */
    .batch-images-section {
        margin-top: 2rem;
    }

    .batch-images-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .batch-images-title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .batch-images-icon {
        width: 2rem;
        height: 2rem;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .batch-images-icon svg {
        width: 1.25rem;
        height: 1.25rem;
        color: white;
    }

    .batch-images-title h4 {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1f2937;
    }

    .batch-images-actions {
        display: flex;
        gap: 0.75rem;
    }

    .batch-action-btn {
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .batch-action-btn.primary {
        background: linear-gradient(135deg, #10b981, #3b82f6);
        color: white;
    }

    .batch-action-btn.primary:hover:not(:disabled) {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }

    .batch-action-btn.secondary {
        background: #6b7280;
        color: white;
    }

    .batch-action-btn.secondary:hover {
        background: #4b5563;
        transform: translateY(-1px);
    }

    .batch-action-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    /* 图片网格 */
    .batch-images-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
    }

    .batch-image-item {
        background: white;
        border-radius: 0.75rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        overflow: hidden;
        transition: transform 0.2s ease;
    }

    .batch-image-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }

    .batch-image-preview {
        position: relative;
        aspect-ratio: 1;
    }

    .batch-image-preview img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .batch-image-overlay {
        position: absolute;
        inset: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .batch-image-status {
        text-align: center;
        color: white;
    }

    .status-spinner {
        width: 2rem;
        height: 2rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top: 2px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 0.5rem;
    }

    .status-completed svg,
    .status-error svg {
        width: 2rem;
        height: 2rem;
        margin: 0 auto 0.5rem;
    }

    .status-completed svg {
        color: #10b981;
    }

    .status-error svg {
        color: #ef4444;
    }

    .batch-image-status p {
        font-size: 0.875rem;
        font-weight: 600;
    }

    .batch-image-remove {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        width: 1.5rem;
        height: 1.5rem;
        background: #ef4444;
        color: white;
        border: none;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        opacity: 0;
        transition: opacity 0.2s ease;
    }

    .batch-image-item:hover .batch-image-remove {
        opacity: 1;
    }

    .batch-image-remove svg {
        width: 1rem;
        height: 1rem;
    }

    .batch-image-info {
        padding: 0.75rem;
    }

    .batch-image-name {
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }

    .batch-image-size {
        font-size: 0.75rem;
        color: #6b7280;
    }

    /* 进度区域 */
    .batch-progress-section {
        margin-top: 2rem;
        background: linear-gradient(135deg, #eff6ff, #f0f9ff);
        border-radius: 1.5rem;
        padding: 2rem;
        border: 1px solid #dbeafe;
    }

    .batch-progress-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .batch-progress-title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .batch-progress-icon {
        width: 2.5rem;
        height: 2.5rem;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .batch-progress-icon svg {
        width: 1.5rem;
        height: 1.5rem;
        color: white;
        animation: spin 1s linear infinite;
    }

    .batch-progress-title h4 {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1f2937;
    }

    .batch-progress-count {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 0.75rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        color: #1f2937;
    }

    /* 进度条 */
    .batch-progress-bar {
        width: 100%;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 1rem;
        height: 0.75rem;
        margin-bottom: 1.5rem;
        overflow: hidden;
    }

    .batch-progress-fill {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        height: 100%;
        border-radius: 1rem;
        transition: width 0.5s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }

    /* 统计卡片 */
    .batch-progress-stats {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
    }

    .stat-item {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 0.75rem;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .stat-item.processing {
        border-color: rgba(59, 130, 246, 0.3);
    }

    .stat-item.completed {
        border-color: rgba(16, 185, 129, 0.3);
    }

    .stat-item.error {
        border-color: rgba(239, 68, 68, 0.3);
    }

    .stat-item.pending {
        border-color: rgba(107, 114, 128, 0.3);
    }

    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .stat-item.processing .stat-number {
        color: #3b82f6;
    }

    .stat-item.completed .stat-number {
        color: #10b981;
    }

    .stat-item.error .stat-number {
        color: #ef4444;
    }

    .stat-item.pending .stat-number {
        color: #6b7280;
    }

    .stat-label {
        font-size: 0.875rem;
        font-weight: 600;
    }

    .stat-item.processing .stat-label {
        color: #3b82f6;
    }

    .stat-item.completed .stat-label {
        color: #10b981;
    }

    .stat-item.error .stat-label {
        color: #ef4444;
    }

    .stat-item.pending .stat-label {
        color: #6b7280;
    }

    /* 下载区域 */
    .batch-download-section {
        margin-top: 2rem;
        text-align: center;
    }

    .batch-download-card {
        background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
        border-radius: 1.5rem;
        padding: 2rem;
        border: 1px solid #bbf7d0;
    }

    .batch-download-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }

    .batch-download-icon {
        width: 2.5rem;
        height: 2.5rem;
        background: linear-gradient(135deg, #10b981, #3b82f6);
        border-radius: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .batch-download-icon svg {
        width: 1.5rem;
        height: 1.5rem;
        color: white;
    }

    .batch-download-header h3 {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1f2937;
    }

    .batch-download-text {
        color: #6b7280;
        margin-bottom: 1.5rem;
    }

    .batch-download-button {
        background: linear-gradient(135deg, #10b981, #3b82f6);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 0.75rem;
        font-size: 1.125rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
    }

    .batch-download-button:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.6);
    }

    .batch-download-button svg {
        width: 1.5rem;
        height: 1.5rem;
    }

    /* 格式提示 */
    .batch-format-tip {
        margin-top: 1.5rem;
        text-align: center;
    }

    .format-tip-content {
        display: inline-flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem 1.5rem;
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .format-tip-content svg {
        width: 1rem;
        height: 1rem;
        color: #10b981;
    }

    .format-tip-content span {
        font-size: 0.875rem;
        font-weight: 600;
        color: #374151;
    }

    .format-tag {
        padding: 0.25rem 0.5rem;
        background: #fef3c7;
        color: #92400e;
        border-radius: 0.375rem;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .batch-images-grid {
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        }

        .batch-progress-stats {
            grid-template-columns: repeat(2, 1fr);
        }

        .batch-upload-features {
            flex-direction: column;
            gap: 0.75rem;
        }
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }

        100% {
            transform: rotate(360deg);
        }
    }
</style>