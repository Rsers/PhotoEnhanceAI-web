<template>
    <div class="batch-result-viewer">
        <!-- 结果标题和统计 -->
        <div class="batch-result-header">
            <div class="batch-result-title-section">
                <div class="batch-result-title">
                    <div class="batch-result-icon">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <div>
                        <h2>批量处理结果</h2>
                        <p>共处理 {{ results.length }} 张图片</p>
                    </div>
                </div>
                <div class="batch-result-actions">
                    <button @click="downloadAllCompleted" :disabled="completedCount === 0"
                        class="batch-result-btn primary">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                            </path>
                        </svg>
                        下载全部 ({{ completedCount }})
                    </button>
                    <button @click="$emit('reset')" class="batch-result-btn secondary">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                            </path>
                        </svg>
                        重新开始
                    </button>
                </div>
            </div>

            <!-- 统计卡片 -->
            <div class="batch-result-stats">
                <div class="stat-card total">
                    <div class="stat-number">{{ results.length }}</div>
                    <div class="stat-label">总数量</div>
                </div>
                <div class="stat-card completed">
                    <div class="stat-number">{{ completedCount }}</div>
                    <div class="stat-label">成功</div>
                </div>
                <div class="stat-card error">
                    <div class="stat-number">{{ errorCount }}</div>
                    <div class="stat-label">失败</div>
                </div>
                <div class="stat-card processing">
                    <div class="stat-number">{{ processingCount }}</div>
                    <div class="stat-label">处理中</div>
                </div>
            </div>
        </div>

        <!-- 结果网格 -->
        <div class="batch-result-grid">
            <div v-for="(result, index) in results" :key="index" class="batch-result-item">
                <!-- 图片对比区域 -->
                <div class="batch-result-images">
                    <!-- 原图 -->
                    <div class="batch-result-original">
                        <img :src="result.preview" :alt="`原图 ${index + 1}`" />
                        <div class="batch-result-label original">原图</div>
                    </div>

                    <!-- 增强图 -->
                    <div class="batch-result-enhanced">
                        <div v-if="result.status === 'processing'" class="batch-result-loading">
                            <div class="batch-result-spinner"></div>
                            <p>处理中...</p>
                        </div>
                        <div v-else-if="result.status === 'completed' && result.enhancedImage"
                            class="batch-result-success">
                            <img :src="result.enhancedImage" :alt="`增强图 ${index + 1}`" />
                            <div class="batch-result-label enhanced">AI增强</div>
                        </div>
                        <div v-else-if="result.status === 'error'" class="batch-result-error">
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                            <p>处理失败</p>
                        </div>
                        <div v-else class="batch-result-pending">
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            <p>等待处理</p>
                        </div>
                    </div>
                </div>


                <!-- 图片信息 -->
                <div class="batch-result-info">
                    <div class="batch-result-meta">
                        <h3>图片 {{ index + 1 }}</h3>
                        <span>{{ formatFileSize(result.file.size) }}</span>
                    </div>

                    <!-- 错误信息 -->
                    <div v-if="result.status === 'error' && result.error" class="batch-result-error-message">
                        {{ result.error }}
                    </div>

                    <!-- 操作按钮 -->
                    <div class="batch-result-item-actions">
                        <button v-if="result.status === 'completed' && result.enhancedImage"
                            @click="downloadSingleImage(result.enhancedImage, index)"
                            class="batch-result-item-btn primary">
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 10v6m0 0l-3-3m3 3l3-3"></path>
                            </svg>
                            下载
                        </button>
                        <button v-if="result.status === 'completed' && result.enhancedImage"
                            @click="viewFullSize(result.enhancedImage, result.preview)"
                            class="batch-result-item-btn secondary">
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"></path>
                            </svg>
                            查看
                        </button>
                        <button v-if="result.status === 'error'" @click="retryImage(index)"
                            class="batch-result-item-btn retry">
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                                </path>
                            </svg>
                            重试
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 空状态 -->
        <div v-if="results.length === 0" class="batch-result-empty">
            <div class="batch-result-empty-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z">
                    </path>
                </svg>
            </div>
            <h3>暂无处理结果</h3>
            <p>请先上传图片并进行批量处理</p>
        </div>

        <!-- 全屏查看模态框 -->
        <div v-if="showFullSizeModal" class="batch-result-modal" @click="closeFullSizeModal">
            <div class="batch-result-modal-content" @click.stop>
                <div class="batch-result-modal-images">
                    <!-- 原图 -->
                    <div class="batch-result-modal-original">
                        <h4>原图</h4>
                        <img :src="fullSizeOriginal" alt="原图" />
                    </div>

                    <!-- 分隔线 -->
                    <div class="batch-result-modal-separator"></div>

                    <!-- 增强图 -->
                    <div class="batch-result-modal-enhanced">
                        <h4>AI 增强</h4>
                        <img :src="fullSizeEnhanced" alt="增强图" />
                    </div>
                </div>

                <!-- 关闭按钮 -->
                <button @click="closeFullSizeModal" class="batch-result-modal-close">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                        </path>
                    </svg>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, computed } from 'vue'
    import { getDownloadBatchSize, getDownloadDelay, getBatchDelay } from '@/config/batchProcessing'

    interface ImageResult {
        file: File
        preview: string
        status: 'pending' | 'processing' | 'completed' | 'error'
        enhancedImage?: string
        error?: string
    }

    interface Props {
        results: ImageResult[]
    }

    interface Emits {
        (e: 'reset'): void
        (e: 'retry', index: number): void
    }

    const props = defineProps < Props > ()
    const emit = defineEmits < Emits > ()

    // 全屏查看相关
    const showFullSizeModal = ref(false)
    const fullSizeOriginal = ref('')
    const fullSizeEnhanced = ref('')

    // 计算属性
    const completedCount = computed(() =>
        props.results.filter(r => r.status === 'completed').length
    )

    const errorCount = computed(() =>
        props.results.filter(r => r.status === 'error').length
    )

    const processingCount = computed(() =>
        props.results.filter(r => r.status === 'processing').length
    )

    // 获取状态文本
    const getStatusText = (status: string): string => {
        const statusMap = {
            'pending': '等待中',
            'processing': '处理中',
            'completed': '已完成',
            'error': '失败'
        }
        return statusMap[status as keyof typeof statusMap] || status
    }

    // 格式化文件大小
    const formatFileSize = (bytes: number): string => {
        if (bytes === 0) return '0 Bytes'
        const k = 1024
        const sizes = ['Bytes', 'KB', 'MB', 'GB']
        const i = Math.floor(Math.log(bytes) / Math.log(k))
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    // 从浏览器缓存获取图片数据（缓存优化）
    const getImageFromCache = async (imageUrl: string): Promise<Blob> => {
        return new Promise((resolve, reject) => {
            const img = new Image()
            img.crossOrigin = 'anonymous'

            img.onload = () => {
                const canvas = document.createElement('canvas')
                const ctx = canvas.getContext('2d')

                canvas.width = img.width
                canvas.height = img.height

                ctx!.drawImage(img, 0, 0)

                canvas.toBlob((blob) => {
                    if (blob) {
                        resolve(blob)
                    } else {
                        reject(new Error('Canvas to blob failed'))
                    }
                }, 'image/jpeg', 0.9)
            }

            img.onerror = () => reject(new Error('Image load failed'))
            img.src = imageUrl  // 这里会使用浏览器缓存！
        })
    }

    // Base64转Blob（缓存优化）
    const base64ToBlob = (base64Data: string): Blob => {
        const base64String = base64Data.split(',')[1]
        const binaryString = atob(base64String)
        const bytes = new Uint8Array(binaryString.length)
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i)
        }
        return new Blob([bytes], { type: 'image/jpeg' })
    }

    // 下载单张图片
    const downloadSingleImage = (imageUrl: string, index: number) => {
        const link = document.createElement('a')
        link.href = imageUrl
        link.download = `enhanced-image-${index + 1}.jpg`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }

    // 下载所有完成的图片（缓存优化版：从浏览器缓存下载）
    const downloadAllCompleted = async () => {
        const completedResults = props.results.filter(r => r.status === 'completed' && r.enhancedImage)

        console.log(`开始批量下载 ${completedResults.length} 张图片（从浏览器缓存）...`)

        // 批量下载配置
        const BATCH_SIZE = getDownloadBatchSize() // 从配置文件获取批次大小
        const DOWNLOAD_DELAY = getDownloadDelay() // 从配置文件获取下载延迟

        // 将图片分批处理
        const batches = []
        for (let i = 0; i < completedResults.length; i += BATCH_SIZE) {
            batches.push(completedResults.slice(i, i + BATCH_SIZE))
        }

        console.log(`分 ${batches.length} 批下载，每批 ${BATCH_SIZE} 张图片`)

        // 顺序处理每批
        for (let batchIndex = 0; batchIndex < batches.length; batchIndex++) {
            const batch = batches[batchIndex]
            console.log(`开始下载第 ${batchIndex + 1}/${batches.length} 批...`)

            // 并发下载当前批次的所有图片
            const downloadPromises = batch.map(async (result, index) => {
                const globalIndex = batchIndex * BATCH_SIZE + index

                try {
                    let imageBlob: Blob

                    if (result.enhancedImage!.startsWith('http')) {
                        // 从浏览器缓存获取图片数据（避免二次服务器请求）
                        console.log(`从缓存获取图片 ${globalIndex + 1}...`)
                        imageBlob = await getImageFromCache(result.enhancedImage!)
                    } else {
                        // Base64直接转换，不需要fetch
                        console.log(`解析Base64图片 ${globalIndex + 1}...`)
                        imageBlob = base64ToBlob(result.enhancedImage!)
                    }

                    // 创建本地下载链接
                    const url = URL.createObjectURL(imageBlob)
                    const link = document.createElement('a')
                    link.href = url
                    link.download = `enhanced-image-${globalIndex + 1}.jpg`
                    document.body.appendChild(link)

                    // 延迟点击，避免浏览器阻止
                    await new Promise(resolve => setTimeout(resolve, index * DOWNLOAD_DELAY))

                    link.click()
                    document.body.removeChild(link)

                    // 清理URL对象，释放内存
                    URL.revokeObjectURL(url)

                    console.log(`图片 ${globalIndex + 1} 下载完成（从缓存）`)
                    return { success: true, index: globalIndex }

                } catch (error) {
                    console.error(`下载图片 ${globalIndex + 1} 失败:`, error)
                    // 如果缓存下载失败，回退到原来的方式
                    const link = document.createElement('a')
                    link.href = result.enhancedImage!
                    link.download = `enhanced-image-${globalIndex + 1}.jpg`
                    document.body.appendChild(link)
                    link.click()
                    document.body.removeChild(link)
                    return { success: false, index: globalIndex, error }
                }
            })

            // 等待当前批次完成
            const batchResults = await Promise.allSettled(downloadPromises)
            const successCount = batchResults.filter(r => r.status === 'fulfilled' && r.value.success).length
            const failCount = batchResults.length - successCount

            console.log(`第 ${batchIndex + 1} 批下载完成: 成功 ${successCount} 张，失败 ${failCount} 张`)

            // 批次间延迟，避免浏览器压力过大
            if (batchIndex < batches.length - 1) {
                await new Promise(resolve => setTimeout(resolve, getBatchDelay()))
            }
        }

        console.log(`批量下载完成，共下载 ${completedResults.length} 张图片（从浏览器缓存）`)
    }

    // 查看全尺寸图片
    const viewFullSize = (enhancedImage: string, originalImage: string) => {
        fullSizeOriginal.value = originalImage
        fullSizeEnhanced.value = enhancedImage
        showFullSizeModal.value = true
    }

    // 关闭全尺寸查看
    const closeFullSizeModal = () => {
        showFullSizeModal.value = false
        fullSizeOriginal.value = ''
        fullSizeEnhanced.value = ''
    }

    // 重试单张图片
    const retryImage = (index: number) => {
        emit('retry', index)
    }
</script>

<style scoped>
    /* 批量结果查看器样式 - 参考单张处理样式 */
    .batch-result-viewer {
        width: 100%;
    }

    /* 结果标题区域 */
    .batch-result-header {
        margin-bottom: 2rem;
    }

    .batch-result-title-section {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .batch-result-title {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .batch-result-icon {
        width: 3rem;
        height: 3rem;
        background: linear-gradient(135deg, #10b981, #3b82f6);
        border-radius: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }

    .batch-result-icon svg {
        width: 1.5rem;
        height: 1.5rem;
        color: white;
    }

    .batch-result-title h2 {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }

    .batch-result-title p {
        color: #6b7280;
        font-size: 1rem;
    }

    .batch-result-actions {
        display: flex;
        gap: 0.75rem;
    }

    .batch-result-btn {
        padding: 0.75rem 1.5rem;
        border-radius: 0.75rem;
        font-size: 1rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .batch-result-btn.primary {
        background: linear-gradient(135deg, #10b981, #3b82f6);
        color: white;
    }

    .batch-result-btn.primary:hover:not(:disabled) {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
    }

    .batch-result-btn.secondary {
        background: #6b7280;
        color: white;
    }

    .batch-result-btn.secondary:hover {
        background: #4b5563;
        transform: translateY(-2px) scale(1.05);
    }

    .batch-result-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
    }

    .batch-result-btn svg {
        width: 1.25rem;
        height: 1.25rem;
    }

    /* 统计卡片 */
    .batch-result-stats {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
    }

    .stat-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 1rem;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .stat-card.total {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        border-color: rgba(59, 130, 246, 0.3);
    }

    .stat-card.completed {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border-color: rgba(16, 185, 129, 0.3);
    }

    .stat-card.error {
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        border-color: rgba(239, 68, 68, 0.3);
    }

    .stat-card.processing {
        background: linear-gradient(135deg, #f9fafb, #f3f4f6);
        border-color: rgba(107, 114, 128, 0.3);
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .stat-card.total .stat-number {
        color: #3b82f6;
    }

    .stat-card.completed .stat-number {
        color: #10b981;
    }

    .stat-card.error .stat-number {
        color: #ef4444;
    }

    .stat-card.processing .stat-number {
        color: #6b7280;
    }

    .stat-label {
        font-size: 0.875rem;
        font-weight: 600;
    }

    .stat-card.total .stat-label {
        color: #3b82f6;
    }

    .stat-card.completed .stat-label {
        color: #10b981;
    }

    .stat-card.error .stat-label {
        color: #ef4444;
    }

    .stat-card.processing .stat-label {
        color: #6b7280;
    }

    /* 结果网格 */
    .batch-result-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    .batch-result-item {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 1.5rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        overflow: hidden;
        transition: transform 0.3s ease;
    }

    .batch-result-item:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }

    /* 图片对比区域 */
    .batch-result-images {
        display: grid;
        grid-template-columns: 1fr 1fr;
        height: 200px;
    }

    .batch-result-original,
    .batch-result-enhanced {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .batch-result-original {
        background: linear-gradient(135deg, #f9fafb, #f3f4f6);
    }

    .batch-result-enhanced {
        background: linear-gradient(135deg, #eff6ff, #f0f9ff);
    }

    .batch-result-original img,
    .batch-result-enhanced img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .batch-result-label {
        position: absolute;
        top: 0.5rem;
        padding: 0.25rem 0.5rem;
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 1rem;
        font-size: 0.625rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .batch-result-label.original {
        left: 0.5rem;
        top: 0.5rem;
        color: #f59e0b;
    }

    .batch-result-label.enhanced {
        right: 0.5rem;
        top: 0.5rem;
        color: #3b82f6;
    }

    /* 状态显示 */
    .batch-result-loading,
    .batch-result-success,
    .batch-result-error,
    .batch-result-pending {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        text-align: center;
    }

    .batch-result-spinner {
        width: 2rem;
        height: 2rem;
        border: 3px solid rgba(59, 130, 246, 0.3);
        border-top: 3px solid #3b82f6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 0.5rem;
    }

    .batch-result-success svg,
    .batch-result-error svg,
    .batch-result-pending svg {
        width: 2rem;
        height: 2rem;
        margin-bottom: 0.5rem;
    }

    .batch-result-success svg {
        color: #10b981;
    }

    .batch-result-error svg {
        color: #ef4444;
    }

    .batch-result-pending svg {
        color: #6b7280;
    }

    .batch-result-loading p,
    .batch-result-success p,
    .batch-result-error p,
    .batch-result-pending p {
        font-size: 0.875rem;
        font-weight: 600;
    }

    .batch-result-loading p {
        color: #3b82f6;
    }

    .batch-result-success p {
        color: #10b981;
    }

    .batch-result-error p {
        color: #ef4444;
    }

    .batch-result-pending p {
        color: #6b7280;
    }


    /* 图片信息 */
    .batch-result-info {
        padding: 1.5rem;
    }

    .batch-result-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .batch-result-meta h3 {
        font-weight: 600;
        color: #1f2937;
    }

    .batch-result-meta span {
        font-size: 0.875rem;
        color: #6b7280;
    }

    /* 错误信息 */
    .batch-result-error-message {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: 0.5rem;
        padding: 0.75rem;
        margin-bottom: 1rem;
        font-size: 0.875rem;
        color: #ef4444;
    }

    /* 操作按钮 */
    .batch-result-item-actions {
        display: flex;
        gap: 0.5rem;
    }

    .batch-result-item-btn {
        flex: 1;
        padding: 0.5rem 0.75rem;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.25rem;
    }

    .batch-result-item-btn.primary {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
    }

    .batch-result-item-btn.primary:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }

    .batch-result-item-btn.secondary {
        background: #6b7280;
        color: white;
    }

    .batch-result-item-btn.secondary:hover {
        background: #4b5563;
        transform: translateY(-1px);
    }

    .batch-result-item-btn.retry {
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        color: white;
    }

    .batch-result-item-btn.retry:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    }

    .batch-result-item-btn svg {
        width: 1rem;
        height: 1rem;
    }

    /* 空状态 */
    .batch-result-empty {
        text-align: center;
        padding: 4rem 2rem;
    }

    .batch-result-empty-icon {
        width: 6rem;
        height: 6rem;
        background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
        border-radius: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
    }

    .batch-result-empty-icon svg {
        width: 3rem;
        height: 3rem;
        color: #9ca3af;
    }

    .batch-result-empty h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }

    .batch-result-empty p {
        color: #6b7280;
    }

    /* 全屏查看模态框 */
    .batch-result-modal {
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 50;
        padding: 1rem;
    }

    .batch-result-modal-content {
        position: relative;
        max-width: 90vw;
        max-height: 90vh;
        width: 80rem;
        background: white;
        border-radius: 1rem;
        overflow: hidden;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
    }

    .batch-result-modal-images {
        display: flex;
    }

    .batch-result-modal-original,
    .batch-result-modal-enhanced {
        flex: 1;
        padding: 2rem;
    }

    .batch-result-modal-original h4,
    .batch-result-modal-enhanced h4 {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1rem;
        text-align: center;
    }

    .batch-result-modal-original img,
    .batch-result-modal-enhanced img {
        width: 100%;
        height: auto;
        max-height: 50vh;
        object-fit: contain;
        border-radius: 0.5rem;
    }

    .batch-result-modal-separator {
        width: 1px;
        background: linear-gradient(to bottom, transparent, #e5e7eb, transparent);
    }

    .batch-result-modal-close {
        position: absolute;
        top: 1rem;
        right: 1rem;
        width: 2rem;
        height: 2rem;
        background: rgba(0, 0, 0, 0.5);
        color: white;
        border: none;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: background 0.2s ease;
    }

    .batch-result-modal-close:hover {
        background: rgba(0, 0, 0, 0.7);
    }

    .batch-result-modal-close svg {
        width: 1.25rem;
        height: 1.25rem;
    }

    /* 响应式设计 */
    @media (max-width: 1024px) {
        .batch-result-grid {
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        }

        .batch-result-stats {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 768px) {
        .batch-result-title-section {
            flex-direction: column;
            gap: 1rem;
            align-items: flex-start;
        }

        .batch-result-actions {
            width: 100%;
            justify-content: stretch;
        }

        .batch-result-btn {
            flex: 1;
        }

        .batch-result-grid {
            grid-template-columns: 1fr;
        }

        .batch-result-stats {
            grid-template-columns: repeat(2, 1fr);
        }

        .batch-result-modal-content {
            max-width: 95vw;
            width: 100%;
        }

        .batch-result-modal-images {
            flex-direction: column;
        }

        .batch-result-modal-separator {
            width: 100%;
            height: 1px;
            background: linear-gradient(to right, transparent, #e5e7eb, transparent);
        }

        .batch-result-modal-original,
        .batch-result-modal-enhanced {
            padding: 1rem;
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