<template>
    <div class="w-full">
        <div @drop="handleDrop" @dragover.prevent @dragenter.prevent
            class="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-400 transition-colors duration-200"
            :class="{ 'border-blue-400 bg-blue-50': dragOver }" @dragenter="dragOver = true"
            @dragleave="dragOver = false">
            <div class="flex flex-col items-center justify-center">
                <svg class="w-16 h-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12">
                    </path>
                </svg>
                <p class="text-xl text-gray-600 mb-2">拖拽图片到此处或点击上传</p>
                <p class="text-sm text-gray-500 mb-6">支持 JPG 格式</p>
                <label
                    class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg cursor-pointer transition duration-200 ease-in-out transform hover:scale-105">
                    选择图片
                    <input type="file" class="hidden" accept=".jpg,.jpeg" @change="handleFileSelect"
                        :disabled="loading" />
                </label>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue'

    interface Props {
        loading?: boolean
    }

    interface Emits {
        (e: 'upload', imageDataUrl: string): void
    }

    defineProps < Props > ()
    const emit = defineEmits < Emits > ()

    const dragOver = ref(false)

    const handleDrop = (e: DragEvent) => {
        e.preventDefault()
        dragOver.value = false

        const files = e.dataTransfer?.files
        if (files && files.length > 0) {
            handleFile(files[0])
        }
    }

    const handleFileSelect = (e: Event) => {
        const target = e.target as HTMLInputElement
        const files = target.files
        if (files && files.length > 0) {
            handleFile(files[0])
        }
    }

    const handleFile = (file: File) => {
        // 检查文件类型
        if (!file.type.startsWith('image/jpeg')) {
            alert('请选择 JPG 格式的图片')
            return
        }

        // 读取文件
        const reader = new FileReader()
        reader.onload = (e) => {
            const result = e.target?.result as string
            emit('upload', result)
        }
        reader.readAsDataURL(file)
    }
</script>