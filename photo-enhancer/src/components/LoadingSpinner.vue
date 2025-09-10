<template>
  <div class="flex items-center justify-center">
    <div class="relative w-24 h-24">
      <!-- 外圈渐变环 -->
      <div class="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 animate-spin opacity-75">
        <div class="absolute inset-1 bg-white rounded-full"></div>
      </div>
      
      <!-- 内圈脉冲 -->
      <div class="absolute inset-2 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 animate-pulse opacity-60">
        <div class="absolute inset-1 bg-white rounded-full"></div>
      </div>
      
      <!-- 中心图标 -->
      <div class="absolute inset-0 flex items-center justify-center">
        <div class="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center animate-pulse">
          <svg class="w-5 h-5 text-white animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
        </div>
      </div>
      
      <!-- 装饰性粒子 -->
      <div class="absolute -top-1 left-1/2 w-2 h-2 bg-blue-400 rounded-full animate-ping"></div>
      <div class="absolute -right-1 top-1/2 w-1.5 h-1.5 bg-purple-400 rounded-full animate-ping" style="animation-delay: 0.5s;"></div>
      <div class="absolute -bottom-1 left-1/3 w-1 h-1 bg-pink-400 rounded-full animate-ping" style="animation-delay: 1s;"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 纯展示组件，无需逻辑
</script>

<style scoped>
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 2s linear infinite;
}
</style>