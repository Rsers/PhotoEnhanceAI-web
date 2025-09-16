/**
 * 批量处理配置
 */
export const BATCH_PROCESSING_CONFIG = {
    // 并发处理数量
    CONCURRENCY: 1,
    
    // 处理超时时间（毫秒）
    TIMEOUT: 300000, // 5分钟
    
    // 重试次数
    MAX_RETRIES: 3,
    
    // 重试延迟（毫秒）
    RETRY_DELAY: 1000,
    
    // 支持的图片格式
    SUPPORTED_FORMATS: ['.jpg', '.jpeg'],
    
    // 最大文件大小（字节）
    MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
    
    // 最大批量数量
    MAX_BATCH_SIZE: 20
} as const

/**
 * 获取并发数
 */
export const getConcurrency = (): number => {
    return BATCH_PROCESSING_CONFIG.CONCURRENCY
}

/**
 * 获取超时时间
 */
export const getTimeout = (): number => {
    return BATCH_PROCESSING_CONFIG.TIMEOUT
}

/**
 * 获取重试次数
 */
export const getMaxRetries = (): number => {
    return BATCH_PROCESSING_CONFIG.MAX_RETRIES
}

/**
 * 获取重试延迟
 */
export const getRetryDelay = (): number => {
    return BATCH_PROCESSING_CONFIG.RETRY_DELAY
}
