<template>
  <div class = "group relative bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300 overflow-hidden flex flex-row min-h-[13rem]">
    
    <div class = "w-14 bg-gray-50/50 border-r border-gray-100 flex flex-col items-center py-4 gap-2 shrink-0">
    <div class = "flex flex-col gap-2 w-full items-center px-1">
         <span 
            v-for = "mod in modalities.slice(0, 4)"
          :key    = "mod"
          :class  = "['text-[9px] font-bold px-1 py-1 rounded-md w-full text-center break-words leading-tight border border-black/5 shadow-sm', getModalityColor(mod)]"
          :title  = "mod"
        >
          {{ formatModality(mod) }}
        </span>
        <span v-if = "modalities.length > 4" class = "text-[9px] text-gray-400 font-medium">
          +{{ modalities.length - 4 }}
        </span>
      </div>
    </div>

    <div class = "flex-1 flex flex-col py-4 pl-4 pr-3">
    <h3  class = "text-base font-bold text-gray-900 leading-snug mb-2 line-clamp-2 group-hover:text-primary-600 transition-colors">
        {{ title }}
      </h3>

      <p class = "text-xs text-gray-500 leading-relaxed line-clamp-8 mb-auto text-justify tracking-wide">
        {{ description || '暂无详细描述，请参考论文或链接。' }}
      </p>

      <div class = "flex items-center gap-3 mt-4 pt-3 border-t border-gray-50">
        
        <a 
            v-if   = "access_url"
          :href    = "access_url"
            target = "_blank"
            class  = "flex items-center gap-1.5 text-xs font-semibold text-gray-600 hover:text-yellow-600 transition-colors group/btn"
            title  = "Access Dataset"
        >
          <span class          = "p-1.5 rounded-md bg-yellow-50 text-yellow-600 group-hover/btn:bg-yellow-100 transition-colors">
          <svg  class          = "w-3.5 h-3.5" fill      = "none" viewBox       = "0 0 24 24" stroke = "currentColor">
          <path stroke-linecap = "round" stroke-linejoin = "round" stroke-width = "2" d              = "M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
            </svg>
          </span>
          <span class = "hidden sm:inline">Data</span>
        </a>

        <a 
            v-if   = "reference_url"
          :href    = "reference_url"
            target = "_blank"
            class  = "flex items-center gap-1.5 text-xs font-semibold text-gray-600 hover:text-red-600 transition-colors group/btn"
            title  = "View Paper"
        >
          <span class          = "p-1.5 rounded-md bg-red-50 text-red-600 group-hover/btn:bg-red-100 transition-colors">
          <svg  class          = "w-3.5 h-3.5" fill      = "none" viewBox       = "0 0 24 24" stroke = "currentColor">
          <path stroke-linecap = "round" stroke-linejoin = "round" stroke-width = "2" d              = "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </span>
          <span class = "hidden sm:inline">Paper</span>
        </a>
      </div>
    </div>

    <div class = "w-24 border-l border-gray-100 flex flex-col py-4 px-2 shrink-0 bg-gray-50/30">
      
      <div class = "mb-3">
      <div class = "text-[10px] text-gray-400 font-medium mb-0.5 uppercase tracking-wider scale-90 origin-top-left flex items-center gap-1">
           Lang
        </div>
        <div class = "text-[10px] font-bold text-gray-700 leading-tight break-words" :title = "languages.join(', ')">
          {{ formattedLanguage }}
        </div>
      </div>

      <div class = "mb-3">
      <div class = "text-[10px] text-gray-400 font-medium mb-0.5 uppercase tracking-wider scale-90 origin-top-left">Year</div>
      <div class = "text-xs font-bold text-gray-800 font-mono">
          {{ year || '-' }}
        </div>
      </div>

      <div class = "mt-auto">
      <div class = "text-[10px] text-gray-400 font-medium mb-1 uppercase tracking-wider scale-90 origin-top-left">Samples</div>
      <div v-if  = "samples" class = "inline-block px-1.5 py-1 bg-slate-800 text-white text-[11px] font-bold rounded shadow-sm">
          {{ samples }}
        </div>
        <div v-else class = "text-[10px] text-gray-300 italic">
          -
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title        : { type: String, default: '' },
  description  : { type: String, default: '' },
  modalities   : { type: Array, default: () => [] },
  languages    : { type: Array, default: () => [] },
  year         : { type: [String, Number], default: '' },
  samples      : { type: String, default: '' },
  access_url   : { type: String, default: '' },
  reference_url: { type: String, default: '' }
})

  // 🎨 模态颜色映射系统 (Pastel Colors - 极简淡色系)
const getModalityColor = (mod) => {
  if (!mod) return 'bg-gray-100 text-gray-600';
  const m = mod.toLowerCase();
  
  if (m.includes('image')) return 'bg-blue-50 text-blue-700 border-blue-100';
  if (m.includes('text')) return 'bg-emerald-50 text-emerald-700 border-emerald-100';
  if (m.includes('video')) return 'bg-purple-50 text-purple-700 border-purple-100';
  if (m.includes('audio')) return 'bg-amber-50 text-amber-700 border-amber-100';
  if (m.includes('3d') || m.includes('point')) return 'bg-rose-50 text-rose-700 border-rose-100';
      // Spatial Prompts / Geometry 使用橙色
  if (m.includes('spatial') || m.includes('geometry') || m.includes('box')) return 'bg-orange-50 text-orange-700 border-orange-100';
  if (m.includes('thermal')) return 'bg-red-50 text-red-700 border-red-100';
  
  return 'bg-gray-100 text-gray-600 border-gray-200';  // 默认
}

// 🔠 模态简写格式化
const formatModality = (mod) => {
  if (!mod) return '';
  const lower = mod.toLowerCase();
  // 特殊缩写处理，防止侧边栏挤爆
  if (lower.includes('spatial prompts')) return 'Spatial'; 
  if (lower.includes('instruction')) return 'Instr.';
  
  // 如果单词太长，适当截断 (超过8字符)
  if (mod.length > 9) return mod.slice(0, 8) + '.';
  return mod;
}

// 🌐 语言显示逻辑 (增强版)
const formattedLanguage = computed(() => {
  const langs = props.languages || [];
  if (langs.length === 0) return 'En'; // 默认兜底
  
  // 逻辑：超过2种语言，或者包含 'Multilingual' (正则匹配，忽略大小写)
  // /^multi/i 匹配以 Multi 开头的单词，如 Multilingual, Multi-lang
  const isMulti = langs.length >= 3 || langs.some(l => /^multi/i.test(l));
  
  if (isMulti) return 'Multilingual';
  if (langs.length === 2) return langs.join(' · ');
  return langs[0];
})
</script>

<style scoped>
/* 无需额外样式，全部使用 Tailwind */
</style>