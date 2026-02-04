<script setup lang="ts">
/**
 * 组件接收两个核心参数：
 * 1. title: 模块主标题 (如 "精选文献")
 * 2. subtitles: 描述文本数组 (如 ["第一行...", "第二行..."])
 */
defineProps<{
  title: string
  subtitles: string[]
}>()
</script>

<template>
  <div class="py-12 text-center">
    <div class="mx-auto max-w-7xl px-6 lg:px-8">
      
      <h2 class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl mb-4">
        {{ title }}
      </h2>

      <div class="mx-auto max-w-2xl text-base text-gray-500">
        <div class="flex flex-col items-center justify-center gap-1">
          <p v-for="(line, index) in subtitles" :key="index">
            {{ line }}
          </p>
        </div>
      </div>

    </div>
  </div>
</template>