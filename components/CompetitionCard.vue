<template>
  <div class="bg-white rounded-xl border border-gray-100 hover:shadow-xl transition-all duration-300 group flex flex-col h-full overflow-hidden relative">
    
    <a 
      :href="competition.link" 
      target="_blank" 
      class="aspect-[3.2/1] w-full relative overflow-hidden bg-white block shrink-0"
    >
      <img 
        v-if="competition.image" 
        :src="competition.image" 
        :alt="competition.title" 
        :class="[
          'w-full h-full object-contain transition-transform duration-700 group-hover:scale-[1.02]',
          status === 'ended' ? 'grayscale opacity-80' : ''
        ]" 
        loading="lazy"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-gray-300 bg-gray-50">
        <i class="fa fa-image text-3xl"></i>
      </div>

      <div v-if="competition.host_event" class="absolute top-3 left-3 z-30">
        <span 
          class="text-[10px] font-bold px-3 py-1.5 rounded-sm border border-purple-200 bg-purple-50/90 text-purple-700 backdrop-blur-md uppercase tracking-widest shadow-sm"
          v-html="highlightText(competition.host_event)"
        ></span>
      </div>

      <div class="absolute top-3 right-3 z-30">
        <span :class="[
          'text-[10px] font-bold px-3 py-1.5 rounded-sm border shadow-sm text-white backdrop-blur-md uppercase tracking-wide transition-colors duration-300',
          currentStatusConfig.class
        ]">
          {{ currentStatusConfig.label }}
        </span>
      </div>
    </a>

    <div class="p-7 flex flex-col flex-1">
      
      <h3 class="text-lg font-bold text-slate-900 mb-4 leading-snug group-hover:text-primary transition-colors line-clamp-2">
        <a 
          :href="competition.link" 
          target="_blank" 
          class="block"
          v-html="highlightText(competition.title)"
        ></a>
      </h3>
      
      <p 
        class="text-sm text-gray-600 mb-8 line-clamp-4 leading-relaxed flex-1 text-justify"
        v-html="highlightText(competition.description)"
      ></p>

      <div class="pt-5 border-t border-gray-100 flex items-center justify-between mt-auto">
        
        <div class="flex items-center gap-2 text-xs font-medium text-gray-500">
          <i class="fa fa-calendar-check-o text-blue-600/70"></i>
          <span class="font-mono tracking-tight">{{ competition.date_range }}</span>
        </div>

        <a 
          :href="competition.link" 
          target="_blank"
          class="flex items-center gap-1.5 text-sm font-bold text-primary hover:text-dark transition-colors group/link"
        >
          赛事详情 
          <i class="fa fa-arrow-right text-xs transition-transform group-hover/link:translate-x-1"></i>
        </a>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  competition: {
    type: Object,
    required: true
  },
  status: {
    type: String,
    default: 'active'
  },
  // 新增：接收搜索关键词
  searchKeyword: {
    type: String,
    default: ''
  }
})

// 状态映射配置
const statusMap = {
  active: { 
    label: '进行中', 
    class: 'bg-emerald-500/90 border-emerald-400' 
  },
  upcoming: { 
    label: '未开始', 
    class: 'bg-blue-500/90 border-blue-400' 
  },
  ended: { 
    label: '已结束', 
    class: 'bg-gray-500/90 border-gray-400' 
  }
}

// 计算当前配置
const currentStatusConfig = computed(() => {
  return statusMap[props.status] || statusMap.active
})

// 🛠️ 高亮处理函数
const highlightText = (text) => {
  if (!text) return ''
  const keyword = props.searchKeyword
  
  // 如果没有关键词，直接返回原文本
  if (!keyword || !keyword.trim()) return text

  // 转义正则特殊字符，防止用户输入 "+", "?" 等导致报错
  const escapedKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  
  // 创建正则：全局匹配 (g) + 忽略大小写 (i)
  const regex = new RegExp(`(${escapedKeyword})`, 'gi')

  // 替换匹配文本为带样式的 span
  return text.replace(regex, '<span class="bg-yellow-200 text-slate-900 rounded-sm px-0.5">$1</span>')
}
</script>