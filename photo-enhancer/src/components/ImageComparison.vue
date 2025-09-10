<template>
    <div class="w-full">
        <!-- 操作按钮 -->
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-semibold text-gray-800">图片对比</h2>
            <div class="flex space-x-3">
                <button v-if="enhancedImage && !processing" @click="$emit('download', enhancedImage)"
                    class="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200">
                    下载增强图片
                </button>
                <button @click="$emit('reset')"
                    class="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200">
                    重新上传
                </button>
            </div>
        </div>

        <!-- 图片对比区域 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- 原图 -->
            <div class="bg-gray-100 rounded-lg p-4">
                <h3 class="text-lg font-medium text-gray-700 mb-4 text-center">原图</h3>
                <div class="relative">
                    <img :src="originalImage" alt="原图" class="w-full h-auto rounded-lg shadow-md" />
                    <div class="absolute bottom-2 left-2 bg-black bg-opacity-75 text-white px-2 py-1 rounded text-sm">
                        原始分辨率
                    </div>
                </div>
            </div>

            <!-- 增强后的图片 -->
            <div class="bg-gray-100 rounded-lg p-4">
                <h3 class="text-lg font-medium text-gray-700 mb-4 text-center">增强后</h3>
                <div class="relative">
                    <div v-if="processing" class="flex items-center justify-center h-64 bg-gray-200 rounded-lg">
                        <div class="text-center">
                            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4">
                            </div>
                            <p class="text-gray-600">处理中...</p>
                        </div>
                    </div>
                    <div v-else-if="!enhancedImage"
                        class="flex items-center justify-center h-64 bg-gray-200 rounded-lg">
                        <p class="text-gray-500">点击"开始增强图片"按钮</p>
                    </div>
                    <div v-else>
                        <img :src="enhancedImage" alt="增强后的图片" class="w-full h-auto rounded-lg shadow-md" />
                        <div
                            class="absolute bottom-2 left-2 bg-black bg-opacity-75 text-white px-2 py-1 rounded text-sm">
                            增强分辨率
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 图片信息 -->
        <div v-if="originalImage" class="mt-6 bg-blue-50 rounded-lg p-4">
            <h4 class="font-semibold text-blue-800 mb-2">处理信息</h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                    <span class="font-medium text-blue-700">格式：</span>
                    <span class="text-blue-600">JPG</span>
                </div>
                <div>
                    <span class="font-medium text-blue-700">状态：</span>
                    <span class="text-blue-600">
                        {{ processing ? '处理中...' : enhancedImage ? '处理完成' : '等待处理' }}
                    </span>
                </div>
                <div>
                    <span class="font-medium text-blue-700">增强倍数：</span>
                    <span class="text-blue-600">2x</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    interface Props {
        originalImage: string
        enhancedImage?: string
        processing?: boolean
    }

    interface Emits {
        (e: 'reset'): void
        (e: 'download', imageUrl: string): void
    }

    defineProps < Props > ()
    defineEmits < Emits > ()
</script>