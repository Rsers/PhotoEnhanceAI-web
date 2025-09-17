import axios from 'axios'
import { getConcurrency } from '@/config/batchProcessing'
import { API_CONFIG, getApiUrl, getStatusUrl, getDownloadUrl } from '@/config/api'

// 创建 axios 实例
const api = axios.create({
    baseURL: API_CONFIG.BASE_URL,
    timeout: API_CONFIG.TIMEOUT, // 5分钟超时 (图片处理可能需要更长时间)
    headers: {
        'Content-Type': 'multipart/form-data'
    }
})

// 请求拦截器
api.interceptors.request.use(
    (config) => {
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// 响应拦截器
api.interceptors.response.use(
    (response) => {
        return response
    },
    (error) => {
        console.error('API Error:', error)
        return Promise.reject(error)
    }
)

// 图片增强 API - 连接真实后端
export const enhanceImageAPI = async (imageDataUrl: string) => {
    console.log('开始调用API...')

    // 将 base64 转换为 blob
    const response = await fetch(imageDataUrl)
    const blob = await response.blob()
    console.log('图片转换完成，大小:', blob.size)

    // 创建 FormData
    const formData = new FormData()
    formData.append('file', blob, 'image.jpg')
    formData.append('tile_size', '400')
    formData.append('quality_level', 'high')

    console.log('发送请求到:', getApiUrl(API_CONFIG.ENDPOINTS.ENHANCE))

    // 发送请求到真实的API接口
    const apiResponse = await api.post(API_CONFIG.ENDPOINTS.ENHANCE, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        timeout: API_CONFIG.TIMEOUT, // 5分钟超时
        onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / (progressEvent.total || 1));
            console.log(`上传进度: ${percentCompleted}%`);
        }
    })

    console.log('API响应:', apiResponse.data)

    // 检查是否是异步任务响应
    if (apiResponse.data.task_id && apiResponse.data.status) {
        console.log('检测到异步任务，开始轮询结果...')
        return await pollTaskResult(apiResponse.data.task_id)
    }

    return apiResponse
}

// 模拟 API（用于开发测试）
export const mockEnhanceImageAPI = async (imageDataUrl: string): Promise<{ data: { enhanced_image: string } }> => {
    // 模拟处理时间
    await new Promise(resolve => setTimeout(resolve, 3000))

    // 返回模拟的增强图片（实际上是原图，但可以用于测试界面）
    return {
        data: {
            enhanced_image: imageDataUrl
        }
    }
}

// 轮询任务结果
const pollTaskResult = async (taskId: string, maxAttempts = API_CONFIG.POLLING.MAX_ATTEMPTS, interval = API_CONFIG.POLLING.INTERVAL): Promise<any> => {
    console.log(`开始轮询任务 ${taskId}...`)

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
            console.log(`第 ${attempt} 次查询任务状态...`)

            // 查询任务状态 - 根据示例代码使用正确的路径
            const response = await api.get(getStatusUrl(taskId))
            console.log('任务状态响应:', response.data)

            // 显示进度信息
            if (response.data.progress) {
                console.log(`状态: ${response.data.status} (${(response.data.progress * 100).toFixed(1)}%)`)
            }

            if (response.data.status === 'completed') {
                console.log('任务完成！')
                // 获取下载链接
                const downloadUrl = getDownloadUrl(taskId)
                console.log('下载链接:', downloadUrl)

                // 返回包含下载链接的响应
                return {
                    data: {
                        download_url: downloadUrl,
                        enhanced_image: downloadUrl
                    }
                }
            } else if (response.data.status === 'failed') {
                throw new Error(`任务失败: ${response.data.error || '未知错误'}`)
            } else if (response.data.status === 'processing' || response.data.status === 'queued') {
                console.log(`任务状态: ${response.data.status}，继续等待...`)
                // 等待指定时间后继续轮询
                await new Promise(resolve => setTimeout(resolve, interval))
            } else {
                console.log(`未知任务状态: ${response.data.status}`)
                await new Promise(resolve => setTimeout(resolve, interval))
            }

        } catch (error: any) {
            console.error(`轮询任务状态时出错:`, error)
            if (attempt === maxAttempts) {
                throw new Error(`任务轮询失败: ${error.message}`)
            }
            await new Promise(resolve => setTimeout(resolve, interval))
        }
    }

    throw new Error('任务处理超时，请稍后查看结果')
}

// 批量图片增强 API
export const batchEnhanceImagesAPI = async (imageDataUrls: string[]) => {
    console.log(`开始批量处理 ${imageDataUrls.length} 张图片...`)

    const results = []

    // 并发处理所有图片（限制并发数避免服务器压力）
    const concurrency = getConcurrency()
    const chunks = []
    for (let i = 0; i < imageDataUrls.length; i += concurrency) {
        chunks.push(imageDataUrls.slice(i, i + concurrency))
    }

    for (const chunk of chunks) {
        const chunkResults = await Promise.allSettled(
            chunk.map(async (imageDataUrl, index) => {
                try {
                    console.log(`处理第 ${index + 1} 张图片...`)
                    const result = await enhanceImageAPI(imageDataUrl)
                    return {
                        success: true,
                        data: result.data,
                        index: index
                    }
                } catch (error: any) {
                    console.error(`第 ${index + 1} 张图片处理失败:`, error)
                    return {
                        success: false,
                        error: error.message || '处理失败',
                        index: index
                    }
                }
            })
        )
        results.push(...chunkResults)
    }

    console.log('批量处理完成，结果:', results)
    return results
}

// 批量轮询任务结果
export const batchPollTaskResults = async (taskIds: string[], maxAttempts = API_CONFIG.POLLING.MAX_ATTEMPTS, interval = API_CONFIG.POLLING.INTERVAL) => {
    console.log(`开始批量轮询 ${taskIds.length} 个任务...`)

    const results = []

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        console.log(`第 ${attempt} 次批量查询任务状态...`)

        const promises = taskIds.map(async (taskId, index) => {
            try {
                const response = await api.get(getStatusUrl(taskId))
                return {
                    taskId,
                    index,
                    status: response.data.status,
                    progress: response.data.progress,
                    error: response.data.error,
                    data: response.data
                }
            } catch (error: any) {
                return {
                    taskId,
                    index,
                    status: 'error',
                    error: error.message,
                    data: null
                }
            }
        })

        const responses = await Promise.all(promises)

        // 检查是否所有任务都完成
        const allCompleted = responses.every(r =>
            r.status === 'completed' || r.status === 'failed' || r.status === 'error'
        )

        if (allCompleted) {
            console.log('所有任务已完成')
            return responses.map(r => ({
                taskId: r.taskId,
                index: r.index,
                status: r.status,
                downloadUrl: r.status === 'completed'
                    ? getDownloadUrl(r.taskId)
                    : null,
                error: r.error
            }))
        }

        // 等待指定时间后继续轮询
        await new Promise(resolve => setTimeout(resolve, interval))
    }

    throw new Error('批量任务处理超时')
}

export default api
