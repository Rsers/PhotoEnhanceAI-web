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
    SUPPORTED_FORMATS: ['.jpg', '.jpeg', '.avif'],

    // 最大文件大小（字节）
    MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB

    // 最大批量数量
    MAX_BATCH_SIZE: 20,

    // 批量下载配置
    DOWNLOAD_BATCH_SIZE: 3, // 每批下载的图片数量（减少到3张避免浏览器阻止）
    DOWNLOAD_DELAY: 1000, // 每张图片下载间隔（毫秒）（增加到1秒）
    BATCH_DELAY: 2000, // 批次间延迟（毫秒）（增加到2秒）

    // Base64编码配置
    PREVIEW_BATCH_SIZE: 2, // 预览分批大小（每批2张图片）
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

/**
 * 获取下载批次大小
 */
export const getDownloadBatchSize = (): number => {
    return BATCH_PROCESSING_CONFIG.DOWNLOAD_BATCH_SIZE
}

/**
 * 获取下载延迟
 */
export const getDownloadDelay = (): number => {
    return BATCH_PROCESSING_CONFIG.DOWNLOAD_DELAY
}

/**
 * 获取批次延迟
 */
export const getBatchDelay = (): number => {
    return BATCH_PROCESSING_CONFIG.BATCH_DELAY
}

/**
 * 获取预览批次大小
 */
export const getPreviewBatchSize = (): number => {
    return BATCH_PROCESSING_CONFIG.PREVIEW_BATCH_SIZE
}
