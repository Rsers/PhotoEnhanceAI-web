import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
    baseURL: import.meta.env.DEV ? 'http://localhost:8000' : '/api',
    timeout: 60000, // 1分钟超时
    headers: {
        'Content-Type': 'application/json'
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

// 图片增强 API
export const enhanceImageAPI = async (imageDataUrl: string) => {
    // 将 base64 转换为 blob
    const response = await fetch(imageDataUrl)
    const blob = await response.blob()

    // 创建 FormData
    const formData = new FormData()
    formData.append('image', blob, 'image.jpg')

    // 发送请求
    return api.post('/enhance', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
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

export default api
