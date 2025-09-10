<template>
    <div class="flex items-center justify-center">
        <div class="relative">
            <!-- 外圈 -->
            <div class="w-16 h-16 border-4 border-blue-200 rounded-full animate-pulse"></div>
            <!-- 内圈旋转 -->
            <div
                class="absolute top-0 left-0 w-16 h-16 border-4 border-transparent border-t-blue-600 rounded-full animate-spin">
            </div>
            <!-- 中心点 -->
            <div
                class="absolute top-1/2 left-1/2 w-2 h-2 bg-blue-600 rounded-full transform -translate-x-1/2 -translate-y-1/2">
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    // 纯展示组件，无需逻辑
</script>