// 图片下载和转换工具

/**
 * 将服务器图片URL下载并转换为Base64格式
 * @param imageUrl 服务器图片URL
 * @returns Promise<string> Base64格式的图片数据
 */
export const downloadImageAsBase64 = async (imageUrl: string): Promise<string> => {
    return new Promise((resolve, reject) => {
        try {
            console.log(`🔄 开始下载服务器图片: ${imageUrl}`)

            // 使用fetch下载图片
            fetch(imageUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`)
                    }
                    return response.blob()
                })
                .then(blob => {
                    console.log(`✅ 图片下载成功，大小: ${blob.size} bytes`)

                    // 转换为Base64
                    const reader = new FileReader()
                    reader.onload = () => {
                        const base64Data = reader.result as string
                        console.log(`✅ 图片已转换为Base64格式`)
                        resolve(base64Data)
                    }
                    reader.onerror = () => {
                        reject(new Error('Base64转换失败'))
                    }
                    reader.readAsDataURL(blob)
                })
                .catch(error => {
                    console.error('❌ 图片下载失败:', error)
                    reject(error)
                })
        } catch (error) {
            console.error('❌ 下载过程出错:', error)
            reject(error)
        }
    })
}

/**
 * 检查图片URL是否为服务器URL
 * @param imageUrl 图片URL
 * @returns boolean
 */
export const isServerImageUrl = (imageUrl: string): boolean => {
    return imageUrl.startsWith('http://') || imageUrl.startsWith('https://')
}

/**
 * 检查图片数据是否为Base64格式
 * @param imageData 图片数据
 * @returns boolean
 */
export const isBase64Image = (imageData: string): boolean => {
    return imageData.startsWith('data:image/')
}
