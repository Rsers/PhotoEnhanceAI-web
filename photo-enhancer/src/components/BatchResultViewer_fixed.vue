<template>
    <div class="batch-result-viewer">
        <!-- 结果标题区域 -->
        <div class="batch-result-header">
            <div class="batch-result-title-section">
                <div class="batch-result-title">
                    <div class="batch-result-icon">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z">
                            </path>
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
                    <div class="stat-label">总计</div>
                </div>
                <div class="stat-card completed">
                    <div class="stat-number">{{ completedCount }}</div>
                    <div class="stat-label">已完成</div>
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
                <!-- 图片预览 -->
                <div class="batch-result-preview">
                    <div v-if="result.status === 'pending'" class="batch-result-pending">
                        <div class="batch-result-spinner"></div>
                        <p>等待中...</p>
                    </div>
                    <div v-else-if="result.status === 'processing'" class="batch-result-processing">
                        <div class="batch-result-spinner"></div>
                        <p>处理中...</p>
                    </div>
                    <div v-else-if="result.status === 'error'" class="batch-result-error">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z">
                            </path>
                        </svg>
                        <p>处理失败</p>
                    </div>
                    <div v-else-if="result.status === 'completed' && result.enhancedImage" class="batch-result-success">
                        <img :src="result.enhancedImage" :alt="`增强图 ${index + 1}`" />
                        <div class="batch-result-label enhanced">AI增强</div>
                    </div>
                </div>

                <!-- 图片信息 -->
                <div class="batch-result-info">
                    <div class="batch-result-filename">
                        <span class="batch-result-index">#{{ index + 1 }}</span>
                        <span class="batch-result-name">{{ result.file?.name || `图片 ${index + 1}` }}</span>
                    </div>
                    <div class="batch-result-details">
                        <span class="batch-result-size">{{ formatFileSize(result.file?.size || 0) }}</span>
                        <span class="batch-result-status" :class="result.status">
                            {{ getStatusText(result.status) }}
                        </span>
                    </div>
                </div>

                <!-- 操作按钮 -->
                <div class="batch-result-item-actions">
                    <button v-if="result.status === 'completed' && result.enhancedImage"
                        @click="downloadSingleImage(result.enhancedImage, index)" class="batch-result-item-btn primary">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                            </path>
                        </svg>
                        下载
                    </button>
                    <button v-if="result.status === 'completed' && result.enhancedImage"
                        @click="viewFullSize(result.enhancedImage, result.preview)"
                        class="batch-result-item-btn secondary">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z">
                            </path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z">
                            </path>
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

        <!-- 全尺寸查看模态框 -->
        <div v-if="showFullSizeModal" class="batch-result-modal" @click="closeFullSizeModal">
            <div class="batch-result-modal-content" @click.stop>
                <div class="batch-result-modal-header">
                    <h3>图片对比</h3>
                    <button @click="closeFullSizeModal" class="batch-result-modal-close">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12">
                            </path>
                        </svg>
                    </button>
                </div>
                <div class="batch-result-modal-body">
                    <div class="batch-result-modal-original">
                        <h4>原图</h4>
                        <img :src="fullSizeOriginal" alt="原图" />
                    </div>
                    <div class="batch-result-modal-enhanced">
                        <h4>AI增强</h4>
                        <img :src="fullSizeEnhanced" alt="增强图" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, computed } from 'vue'
    import { getDownloadBatchSize, getDownloadDelay, getBatchDelay } from '@/config/batchProcessing'

    interface ImageItem {
        file: File
        preview: string
        status: 'pending' | 'processing' | 'completed' | 'error'
        enhancedImage?: string
        error?: string
    }

    interface Props {
        results: ImageItem[]
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

    // 从浏览器缓存获取图片数据（修复版：移除crossOrigin避免跨域问题）
    const getImageFromCache = async (imageUrl: string): Promise<Blob> => {
        return new Promise((resolve, reject) => {
            const img = new Image()
            // 移除 crossOrigin 设置，避免跨域问题

            img.onload = () => {
                try {
                    const canvas = document.createElement('canvas')
                    const ctx = canvas.getContext('2d')

                    canvas.width = img.width
                    canvas.height = img.height

                    ctx!.drawImage(img, 0, 0)

                    canvas.toBlob((blob) => {
                        if (blob) {
                            console.log(`✅ 成功从缓存获取图片: ${imageUrl}`)
                            resolve(blob)
                        } else {
                            console.error('❌ Canvas to blob failed')
                            reject(new Error('Canvas to blob failed'))
                        }
                    }, 'image/jpeg', 0.9)
                } catch (error) {
                    console.error('❌ Canvas 操作失败:', error)
                    reject(error)
                }
            }

            img.onerror = (error) => {
                console.error('❌ 图片加载失败:', imageUrl, error)
                reject(new Error(`Image load failed: ${imageUrl}`))
            }

            console.log(`🔄 尝试从缓存加载图片: ${imageUrl}`)
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

    // 下载所有完成的图片（修复版：更好的错误处理和调试信息）
    const downloadAllCompleted = async () => {
        const completedResults = props.results.filter(r => r.status === 'completed' && r.enhancedImage)

        console.log(`🚀 开始批量下载 ${completedResults.length} 张图片...`)

        if (completedResults.length === 0) {
            console.log('❌ 没有完成的图片可以下载')
            return
        }

        // 批量下载配置
        const BATCH_SIZE = getDownloadBatchSize() // 从配置文件获取批次大小
        const DOWNLOAD_DELAY = getDownloadDelay() // 从配置文件获取下载延迟

        // 将图片分批处理
        const batches = []
        for (let i = 0; i < completedResults.length; i += BATCH_SIZE) {
            batches.push(completedResults.slice(i, i + BATCH_SIZE))
        }

        console.log(`📦 分 ${batches.length} 批下载，每批 ${BATCH_SIZE} 张图片`)

        let totalSuccess = 0
        let totalFailed = 0

        // 顺序处理每批
        for (let batchIndex = 0; batchIndex < batches.length; batchIndex++) {
            const batch = batches[batchIndex]
            console.log(`📥 开始下载第 ${batchIndex + 1}/${batches.length} 批...`)

            // 并发下载当前批次的所有图片
            const downloadPromises = batch.map(async (result, index) => {
                const globalIndex = batchIndex * BATCH_SIZE + index

                try {
                    let imageBlob: Blob

                    if (result.enhancedImage!.startsWith('http')) {
                        // 从浏览器缓存获取图片数据（避免二次服务器请求）
                        console.log(`🔄 从缓存获取图片 ${globalIndex + 1}...`)
                        imageBlob = await getImageFromCache(result.enhancedImage!)
                    } else {
                        // Base64直接转换，不需要fetch
                        console.log(`🔄 解析Base64图片 ${globalIndex + 1}...`)
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

                    console.log(`✅ 图片 ${globalIndex + 1} 下载完成`)
                    return { success: true, index: globalIndex }

                } catch (error) {
                    console.error(`❌ 下载图片 ${globalIndex + 1} 失败:`, error)
                    // 如果缓存下载失败，回退到原来的方式
                    try {
                        const link = document.createElement('a')
                        link.href = result.enhancedImage!
                        link.download = `enhanced-image-${globalIndex + 1}.jpg`
                        document.body.appendChild(link)
                        link.click()
                        document.body.removeChild(link)
                        console.log(`⚠️ 图片 ${globalIndex + 1} 使用回退方式下载完成`)
                        return { success: true, index: globalIndex, fallback: true }
                    } catch (fallbackError) {
                        console.error(`❌ 回退下载也失败:`, fallbackError)
                        return { success: false, index: globalIndex, error: fallbackError }
                    }
                }
            })

            // 等待当前批次完成
            const batchResults = await Promise.allSettled(downloadPromises)
            const successCount = batchResults.filter(r => r.status === 'fulfilled' && r.value.success).length
            const failCount = batchResults.length - successCount

            totalSuccess += successCount
            totalFailed += failCount

            console.log(`📊 第 ${batchIndex + 1} 批下载完成: 成功 ${successCount} 张，失败 ${failCount} 张`)

            // 批次间延迟，避免浏览器压力过大
            if (batchIndex < batches.length - 1) {
                console.log(`⏳ 等待 ${getBatchDelay()}ms 后开始下一批...`)
                await new Promise(resolve => setTimeout(resolve, getBatchDelay()))
            }
        }

        console.log(`🎉 批量下载完成！总计: 成功 ${totalSuccess} 张，失败 ${totalFailed} 张`)
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
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.5rem;
    }

    .batch-result-item {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 1rem;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .batch-result-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }

    /* 图片预览 */
    .batch-result-preview {
        position: relative;
        width: 100%;
        height: 200px;
        border-radius: 0.75rem;
        overflow: hidden;
        margin-bottom: 1rem;
        background: #f3f4f6;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .batch-result-preview img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .batch-result-pending,
    .batch-result-processing,
    .batch-result-error {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: #6b7280;
    }

    .batch-result-pending svg,
    .batch-result-processing svg,
    .batch-result-error svg {
        width: 3rem;
        height: 3rem;
        margin-bottom: 0.5rem;
    }

    .batch-result-error {
        color: #ef4444;
    }

    .batch-result-spinner {
        width: 3rem;
        height: 3rem;
        border: 3px solid #e5e7eb;
        border-top: 3px solid #3b82f6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 0.5rem;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }

        100% {
            transform: rotate(360deg);
        }
    }

    .batch-result-success {
        position: relative;
        width: 100%;
        height: 100%;
    }

    .batch-result-label {
        position: absolute;
        background: rgba(255, 255, 255, 0.6);
        padding: 0.25rem 0.5rem;
        font-size: 0.625rem;
        font-weight: 600;
        border-radius: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .batch-result-label.enhanced {
        top: 0.5rem;
        right: 0.5rem;
        color: #10b981;
    }

    /* 图片信息 */
    .batch-result-info {
        margin-bottom: 1rem;
    }

    .batch-result-filename {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .batch-result-index {
        background: #3b82f6;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.375rem;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .batch-result-name {
        font-weight: 600;
        color: #1f2937;
        flex: 1;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .batch-result-details {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.875rem;
        color: #6b7280;
    }

    .batch-result-status {
        padding: 0.25rem 0.5rem;
        border-radius: 0.375rem;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .batch-result-status.pending {
        background: #fef3c7;
        color: #d97706;
    }

    .batch-result-status.processing {
        background: #dbeafe;
        color: #2563eb;
    }

    .batch-result-status.completed {
        background: #d1fae5;
        color: #059669;
    }

    .batch-result-status.error {
        background: #fee2e2;
        color: #dc2626;
    }

    /* 操作按钮 */
    .batch-result-item-actions {
        display: flex;
        gap: 0.5rem;
    }

    .batch-result-item-btn {
        flex: 1;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.25rem;
    }

    .batch-result-item-btn.primary {
        background: linear-gradient(135deg, #10b981, #3b82f6);
        color: white;
    }

    .batch-result-item-btn.primary:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
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
        background: #f59e0b;
        color: white;
    }

    .batch-result-item-btn.retry:hover {
        background: #d97706;
        transform: translateY(-1px);
    }

    .batch-result-item-btn svg {
        width: 1rem;
        height: 1rem;
    }

    /* 全尺寸查看模态框 */
    .batch-result-modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(8px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        padding: 2rem;
    }

    .batch-result-modal-content {
        background: white;
        border-radius: 1rem;
        max-width: 90vw;
        width: 80rem;
        max-height: 90vh;
        overflow: hidden;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
    }

    .batch-result-modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 2rem;
        border-bottom: 1px solid #e5e7eb;
    }

    .batch-result-modal-header h3 {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1f2937;
    }

    .batch-result-modal-close {
        background: none;
        border: none;
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 0.5rem;
        transition: all 0.3s ease;
    }

    .batch-result-modal-close:hover {
        background: #f3f4f6;
    }

    .batch-result-modal-close svg {
        width: 1.5rem;
        height: 1.5rem;
        color: #6b7280;
    }

    .batch-result-modal-body {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        padding: 2rem;
        max-height: 50vh;
        overflow-y: auto;
    }

    .batch-result-modal-original,
    .batch-result-modal-enhanced {
        text-align: center;
    }

    .batch-result-modal-original h4,
    .batch-result-modal-enhanced h4 {
        font-size: 1rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 1rem;
    }

    .batch-result-modal-original img,
    .batch-result-modal-enhanced img {
        width: 100%;
        height: auto;
        max-height: 50vh;
        object-fit: contain;
        border-radius: 0.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .batch-result-stats {
            grid-template-columns: repeat(2, 1fr);
        }

        .batch-result-grid {
            grid-template-columns: 1fr;
        }

        .batch-result-modal-body {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .batch-result-modal-content {
            width: 95vw;
            max-width: none;
        }
    }
</style>