// 图片大小计算工具

/**
 * 计算Base64图片的大小（字节）
 * @param base64Data Base64格式的图片数据
 * @returns number 图片大小（字节）
 */
export const calculateBase64ImageSize = (base64Data: string): number => {
    if (!base64Data || !base64Data.startsWith('data:')) {
        return 0
    }

    try {
        // 移除data:image/xxx;base64,前缀
        const base64String = base64Data.split(',')[1]
        if (!base64String) {
            return 0
        }

        // Base64编码会增加约33%的大小，所以需要计算原始大小
        // Base64字符串长度 * 3/4 得到原始字节数
        const sizeInBytes = Math.floor(base64String.length * 3 / 4)

        return sizeInBytes
    } catch (error) {
        console.error('计算Base64图片大小失败:', error)
        return 0
    }
}

/**
 * 从Blob计算图片大小
 * @param blob Blob对象
 * @returns number 图片大小（字节）
 */
export const calculateBlobSize = (blob: Blob): number => {
    return blob.size
}

/**
 * 格式化文件大小显示
 * @param bytes 字节数
 * @returns string 格式化后的大小字符串
 */
export const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
