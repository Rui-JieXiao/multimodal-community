<template>
  <div class="bg-white rounded-xl border border-gray-100 hover:shadow-xl transition-all duration-300 group flex flex-col h-full overflow-hidden relative">
    
    <div class="absolute top-3 left-3 z-30 pointer-events-none flex flex-col items-start gap-1">
      <span 
        class="bg-black/70 backdrop-blur-md text-white text-[10px] font-bold px-2 py-1 rounded border border-black/10 shadow-sm uppercase tracking-wider"
        v-html="highlightText(source.includes('/') ? source.split('/')[0].trim() : source)">
      </span>

      <span v-if="source.includes('/')" 
        class="bg-white/90 backdrop-blur-md text-dark text-[10px] font-bold px-2 py-1 rounded border border-gray-100 shadow-sm uppercase tracking-wider"
        v-html="highlightText(source.split('/').pop().trim())">
      </span>
    </div>

    <div class="absolute top-3 right-3 z-30 pointer-events-none">
      <span :class="[
        'text-[10px] font-bold px-2 py-0.5 rounded-sm shadow-sm border backdrop-blur-md transition-colors duration-300',
        currentStatusConfig.class
      ]">
        {{ currentStatusConfig.label }}
      </span>
    </div>

    <a 
      :href="link" 
      target="_blank" 
      rel="noopener noreferrer"
      :class="[
        'aspect-[3.2/1] w-full overflow-hidden relative flex items-center justify-center border-b border-gray-50 cursor-pointer block transition-all active:scale-[0.99]',
        isJournalMode ? 'bg-gray-200' : 'bg-white' 
      ]"
      title="点击查看征稿详情"
    >
      <img 
        v-if="finalImage && isJournalMode" 
        :src="finalImage" 
        class="absolute inset-0 w-full h-full object-cover blur-3xl opacity-50 scale-150 pointer-events-none"
        @error="handleImageError"
      />
      
      <div v-if="isJournalMode" class="absolute inset-0 bg-black/25 pointer-events-none"></div>

      <div :class="[
        'relative z-10 transition-all duration-500 flex items-center justify-center',
        isJournalMode 
          ? 'h-[80%] shrink-0 shadow-2xl group-hover:scale-110 group-hover:-rotate-2' 
          : 'w-full h-full group-hover:scale-[1.02]'                                  
      ]">
        <img 
          v-if="finalImage" 
          :src="finalImage" 
          alt="Cover"
          :class="[
            isJournalMode 
              ? 'h-full w-auto object-contain rounded-sm border border-white/20' 
              : 'w-full h-full object-cover' 
          ]" 
          @error="handleImageError"
        />
        <div v-else class="h-full w-24 bg-gray-200 flex items-center justify-center rounded-sm">
          <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
          </svg>
        </div>
      </div>

      <div v-if="metrics && metrics.length" class="relative z-10 flex flex-col gap-2 border-l-2 border-white/30 pl-5 lg:pl-10">
        <div v-for="(m, index) in metrics" :key="index" class="flex flex-col">
          <span class="text-[9px] text-white/90 uppercase font-black tracking-widest leading-none mb-1 drop-shadow-strong">
            {{ m.label }}
          </span>
          <span class="text-2xl lg:text-3xl text-white font-black leading-none drop-shadow-strong font-mono">
            {{ m.value }}
          </span>
        </div>
      </div>
    </a>

    <div class="p-6 flex flex-col flex-1">
      <h3 
        class="text-base font-bold text-dark mb-3 leading-snug group-hover:text-blue-600 transition-colors line-clamp-2"
        v-html="highlightText(title)"
      ></h3>
      
      <p 
        class="text-[13px] text-gray-600 line-clamp-3 leading-relaxed mb-6 flex-1"
        v-html="highlightText(scope)"
      ></p>

      <div class="pt-4 border-t border-gray-50 flex items-center justify-between mt-auto">
        <div class="flex items-center gap-2 text-[11px] font-medium text-gray-400">
          <svg class="w-3.5 h-3.5 text-blue-600/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
          </svg>
          <span class="font-mono">{{ date_range }}</span>
        </div>

        <a 
          :href="link" 
          target="_blank" 
          rel="noopener noreferrer"
          class="flex items-center gap-1 text-xs font-bold text-blue-600 hover:text-dark transition-colors"
        >
          征稿详情
          <svg class="w-3 h-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
          </svg>
        </a>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  id: String,
  source: String,
  title: String,
  scope: String,
  date_range: String, 
  image: String,      
  link: String,
  status: String,
  metrics: Array,
  searchKeyword: {
    type: String,
    default: ''
  }
})

// 状态样式映射表
const statusMap = {
  open: { label: '进行中', class: 'bg-green-500/90 text-white border-green-400' },
  upcoming: { label: '未开始', class: 'bg-blue-500/90 text-white border-blue-400' },
  closed: { label: '已结束', class: 'bg-gray-500/90 text-white border-gray-400' }
}

const currentStatusConfig = computed(() => {
  return statusMap[props.status] || statusMap.open
})

const isJournalMode = computed(() => {
  return props.metrics && props.metrics.length > 0
})

const finalImage = computed(() => {
  if (props.image) return props.image
  if (props.id) return `/cfp_covers/${props.id}.webp`
  return null
})

const handleImageError = (e) => {
  e.target.src = '/paper_images/default-cover.jpg'
}

// 🟢 修复点 2：增强高亮函数，添加内联样式兜底，并增加 trim()
const highlightText = (text) => {
  if (!text) return ''
  // 确保关键词去空
  const keyword = props.searchKeyword ? props.searchKeyword.trim() : ''
  
  if (!keyword) return text

  const escapedKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const regex = new RegExp(`(${escapedKeyword})`, 'gi')

  // 添加 style="background-color: ..." 以防止 Tailwind 类名被 Purge 掉
  // 添加 text-slate-900 确保文字颜色在深色背景下也清晰（虽然这里背景是黄色的）
  return text.replace(regex, '<span class="bg-yellow-200 text-slate-900 rounded-sm px-0.5" style="background-color: #fef08a; color: #0f172a;">$1</span>')
}
</script>

<style scoped>
.drop-shadow-strong {
  filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.6)) drop-shadow(0 1px 2px rgba(0, 0, 0, 0.8));
}

/* 🟢 修复点 3：确保 v-html 内部样式能穿透 scope */
:deep(.bg-yellow-200) {
  background-color: #fef08a;
  color: #0f172a;
}
</style>