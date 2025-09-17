<template>
    <div class="w-full">
        <!-- 操作栏 -->
        <div class="flex justify-between items-center p-6 border-b border-gray-100">
            <div class="flex items-center space-x-4">
                <div class="flex items-center space-x-2">
                    <div class="w-3 h-3 rounded-full bg-blue-500"></div>
                    <span class="text-sm font-medium text-gray-700">对比视图</span>
                </div>
                <div class="text-sm text-gray-500">
                    {{ processing ? '处理中...' : enhancedImage ? '处理完成' : '等待处理' }}
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <button v-if="enhancedImage && !processing" @click="$emit('download', enhancedImage)"
                    class="inline-flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                        </path>
                    </svg>
                    下载高清图片
                </button>
                <button @click="$emit('reset')"
                    class="inline-flex items-center px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white text-sm font-medium rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                        </path>
                    </svg>
                    重新上传
                </button>
            </div>
        </div>

        <!-- 左右对比区域 -->
        <div class="flex flex-col lg:flex-row min-h-[500px]">
            <!-- 原图区域 -->
            <div class="flex-1 relative bg-gradient-to-br from-gray-50 to-gray-100">
                <!-- 标签 -->
                <div class="absolute top-4 left-4 z-10">
                    <div
                        class="inline-flex items-center px-3 py-1 bg-white/90 backdrop-blur-sm rounded-full shadow-lg border border-white/20">
                        <div class="w-2 h-2 bg-orange-500 rounded-full mr-2"></div>
                        <span class="text-sm font-medium text-gray-700">原图</span>
                    </div>
                </div>

                <!-- 图片容器 -->
                <div class="h-full flex items-center justify-center p-8">
                    <div class="relative max-w-full max-h-full">
                        <img :src="originalImage" alt="原图"
                            class="max-w-full max-h-full object-contain rounded-xl shadow-2xl border border-white/20" />
                        <!-- 图片信息 -->
                        <div
                            class="absolute bottom-3 right-3 bg-black/70 text-white px-3 py-1 rounded-lg text-xs backdrop-blur-sm">
                            原始分辨率
                        </div>
                    </div>
                </div>
            </div>

            <!-- 分隔线 -->
            <div class="hidden lg:block w-px bg-gradient-to-b from-transparent via-gray-200 to-transparent"></div>
            <div class="lg:hidden h-px bg-gradient-to-r from-transparent via-gray-200 to-transparent"></div>

            <!-- 增强图区域 -->
            <div class="flex-1 relative bg-gradient-to-br from-blue-50 to-purple-50">
                <!-- 标签 -->
                <div class="absolute top-4 right-4 z-10">
                    <div
                        class="inline-flex items-center px-3 py-1 bg-white/90 backdrop-blur-sm rounded-full shadow-lg border border-white/20">
                        <div class="w-2 h-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full mr-2"></div>
                        <span class="text-sm font-medium text-gray-700">AI 增强</span>
                    </div>
                </div>

                <!-- 图片容器 -->
                <div class="h-full flex items-center justify-center p-8">
                    <!-- 处理中状态 -->
                    <div v-if="processing" class="text-center">
                        <div class="relative mb-6">
                            <div
                                class="w-20 h-20 border-4 border-blue-200 rounded-full animate-spin border-t-blue-600 mx-auto">
                            </div>
                            <div class="absolute inset-0 flex items-center justify-center">
                                <svg class="w-8 h-8 text-blue-600 animate-pulse" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                                </svg>
                            </div>
                        </div>
                        <h3 class="text-lg font-semibold text-gray-800 mb-2">AI 处理中</h3>
                        <p class="text-gray-600 mb-4">正在使用深度学习算法增强图像...</p>
                        <div class="w-48 mx-auto bg-gray-200 rounded-full h-2">
                            <div class="bg-gradient-to-r from-blue-600 to-purple-600 h-2 rounded-full animate-pulse"
                                style="width: 75%"></div>
                        </div>
                    </div>

                    <!-- 等待处理状态 -->
                    <div v-else-if="!enhancedImage" class="text-center">
                        <div
                            class="w-20 h-20 bg-gradient-to-r from-blue-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
                            <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                            </svg>
                        </div>
                        <h3 class="text-lg font-semibold text-gray-800 mb-2">准备增强</h3>
                        <p class="text-gray-600">点击下方按钮开始 AI 处理</p>
                    </div>

                    <!-- 处理完成状态 -->
                    <div v-else class="relative max-w-full max-h-full">
                        <img :src="enhancedImage" alt="AI 增强后的图片"
                            class="max-w-full max-h-full object-contain rounded-xl shadow-2xl border border-white/20" />
                        <!-- 图片信息 -->
                        <div
                            class="absolute bottom-3 right-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-3 py-1 rounded-lg text-xs backdrop-blur-sm">
                            超分辨率 2x
                        </div>
                        <!-- 完成标识 -->
                        <div class="absolute top-3 left-3 bg-green-500 text-white p-2 rounded-full shadow-lg">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M5 13l4 4L19 7"></path>
                            </svg>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 底部信息栏 -->
        <div class="p-6 bg-gradient-to-r from-blue-50 to-purple-50 border-t border-gray-100">
            <div class="flex flex-col sm:flex-row items-center justify-between space-y-4 sm:space-y-0">
                <div class="flex items-center space-x-6 text-sm">
                    <div class="flex items-center space-x-2">
                        <span class="font-medium text-gray-700">格式：</span>
                        <span class="px-2 py-1 bg-white rounded-md text-gray-600 shadow-sm">JPG</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span class="font-medium text-gray-700">增强倍数：</span>
                        <span
                            class="px-2 py-1 bg-gradient-to-r from-blue-100 to-purple-100 rounded-md text-gray-800 shadow-sm">2x</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span class="font-medium text-gray-700">状态：</span>
                        <span class="px-2 py-1 rounded-md shadow-sm" :class="{
              'bg-yellow-100 text-yellow-800': processing,
              'bg-green-100 text-green-800': enhancedImage && !processing,
              'bg-gray-100 text-gray-600': !enhancedImage && !processing
            }">
                            {{ processing ? '处理中' : enhancedImage ? '已完成' : '等待处理' }}
                        </span>
                    </div>
                </div>

                <div v-if="enhancedImage" class="flex items-center space-x-2 text-sm text-green-600">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <span class="font-medium">图片增强完成</span>
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