// 图片格式转换工具
export interface ConversionResult {
    success: boolean
    dataUrl?: string
    error?: string
}

/**
 * 将AVIF格式图片转换为JPG格式
 * @param file AVIF格式的File对象
 * @param quality JPG质量 (0-1, 默认0.9)
 * @returns Promise<ConversionResult>
 */
export const convertAvifToJpg = async (file: File, quality: number = 0.9): Promise<ConversionResult> => {
    return new Promise((resolve) => {
        try {
            // 检查文件类型
            if (!file.type.includes('avif') && !file.name.toLowerCase().endsWith('.avif')) {
                resolve({
                    success: false,
                    error: '文件不是AVIF格式'
                })
                return
            }

            console.log(`🔄 开始转换AVIF图片: ${file.name}`)

            // 创建Image对象加载AVIF图片
            const img = new Image()

            img.onload = () => {
                try {
                    console.log(`✅ AVIF图片加载成功: ${img.width}x${img.height}`)

                    // 创建Canvas进行转换
                    const canvas = document.createElement('canvas')
                    const ctx = canvas.getContext('2d')

                    if (!ctx) {
                        resolve({
                            success: false,
                            error: '无法创建Canvas上下文'
                        })
                        return
                    }

                    // 设置Canvas尺寸
                    canvas.width = img.width
                    canvas.height = img.height

                    // 绘制图片到Canvas
                    ctx.drawImage(img, 0, 0)

                    // 转换为JPG格式的DataURL
                    const jpgDataUrl = canvas.toDataURL('image/jpeg', quality)

                    console.log(`✅ AVIF转JPG成功: ${file.name}`)

                    resolve({
                        success: true,
                        dataUrl: jpgDataUrl
                    })
                } catch (error) {
                    console.error('❌ Canvas转换失败:', error)
                    resolve({
                        success: false,
                        error: `Canvas转换失败: ${error}`
                    })
                }
            }

            img.onerror = (error) => {
                console.error('❌ AVIF图片加载失败:', error)
                resolve({
                    success: false,
                    error: 'AVIF图片加载失败，可能浏览器不支持AVIF格式'
                })
            }

            // 创建对象URL并加载图片
            const objectUrl = URL.createObjectURL(file)
            img.src = objectUrl

            // 清理对象URL
            const originalOnload = img.onload
            img.onload = (event) => {
                URL.revokeObjectURL(objectUrl)
                if (originalOnload) {
                    originalOnload.call(img, event)
                }
            }

        } catch (error) {
            console.error('❌ AVIF转换过程出错:', error)
            resolve({
                success: false,
                error: `转换过程出错: ${error}`
            })
        }
    })
}

/**
 * 检查文件是否为AVIF格式
 * @param file 文件对象
 * @returns boolean
 */
export const isAvifFile = (file: File): boolean => {
    return file.type.includes('avif') || file.name.toLowerCase().endsWith('.avif')
}

/**
 * 检查文件是否为支持的图片格式
 * @param file 文件对象
 * @returns boolean
 */
export const isSupportedImageFormat = (file: File): boolean => {
    const supportedTypes = ['image/jpeg', 'image/jpg', 'image/avif']
    const supportedExtensions = ['.jpg', '.jpeg', '.avif']

    const extension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'))

    return supportedTypes.includes(file.type) || supportedExtensions.includes(extension)
}

/**
 * 获取文件格式的显示名称
 * @param file 文件对象
 * @returns string
 */
export const getFileFormatDisplayName = (file: File): string => {
    if (isAvifFile(file)) return 'AVIF'
    if (file.type.includes('jpeg') || file.name.toLowerCase().endsWith('.jpg') || file.name.toLowerCase().endsWith('.jpeg')) {
        return 'JPG'
    }
    return '未知格式'
}
