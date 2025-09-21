// API 配置文件
export const API_CONFIG = {
    // 服务器地址 - 可以根据需要修改
    BASE_URL: 'https://gongjuxiang.work',

    // API 端点
    ENDPOINTS: {
        ENHANCE: '/api/v1/enhance',
        STATUS: '/api/v1/status',
        DOWNLOAD: '/api/v1/download'
    },

    // 超时设置
    TIMEOUT: 300000, // 5分钟

    // 轮询设置
    POLLING: {
        MAX_ATTEMPTS: 60,
        INTERVAL: 5000 // 5秒
    }
}

// 获取完整的API URL
export const getApiUrl = (endpoint: string) => {
    return `${API_CONFIG.BASE_URL}${endpoint}`
}

// 获取状态查询URL
export const getStatusUrl = (taskId: string) => {
    return `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.STATUS}/${taskId}`
}

// 获取下载URL
export const getDownloadUrl = (taskId: string) => {
    return `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.DOWNLOAD}/${taskId}`
}
