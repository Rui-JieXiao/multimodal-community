<template>
  <div class="group flex flex-col w-full min-w-[300px] h-[480px] bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-2xl transition-all duration-300 overflow-hidden">
    
    <div class="h-[190px] shrink-0 p-5 flex flex-col relative z-10">
      
      <div class="mb-2 shrink-0">
        <span 
          class="inline-block text-[10px] font-bold px-2 py-0.5 rounded border"
          :class="venueConfig.style"
        >
          {{ conference || 'Paper' }}
        </span>
      </div>

      <div class="h-[3rem] mb-2 shrink-0 overflow-hidden">
        <h3 class="text-base font-bold text-gray-900 leading-snug group-hover:text-blue-600 transition-colors line-clamp-2" :title="title">
          <a :href="link" target="_blank" class="block">
            {{ title }}
          </a>
        </h3>
      </div>

      <div class="mb-1 shrink-0">
        <div class="flex items-start text-xs text-gray-500 leading-relaxed" :title="authors">
          <svg class="w-3.5 h-3.5 mr-2 shrink-0 mt-0.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
          <span class="line-clamp-3">
            {{ authors || 'Unknown Authors' }}
          </span>
        </div>
      </div>

      <div class="mt-auto flex items-center text-xs text-gray-400 font-medium">
        <svg class="w-3.5 h-3.5 mr-2 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
        <span>{{ date || '2024' }}</span>
      </div>

    </div>

    <div class="flex-1 w-full px-5 pb-0 overflow-hidden flex flex-col">
      
      <div class="relative w-full h-full rounded-t-lg overflow-hidden bg-gray-50 border-x border-t border-gray-100">
        
        <img 
          :src="image || defaultImage" 
          :alt="title" 
          class="w-full h-full object-cover object-top transition-transform duration-700 group-hover:scale-105" 
        />

        <div class="absolute inset-0 bg-slate-900/95 backdrop-blur-sm p-5 flex flex-col justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          
          <h4 class="text-white/90 font-bold mb-2 text-xs uppercase tracking-wider border-b border-white/10 pb-1">Intro</h4>
          <div class="w-full flex-1 overflow-y-auto custom-scrollbar">
            <p class="text-xs text-gray-300 leading-relaxed text-justify whitespace-pre-line">
              {{ description || '暂无详细描述...' }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="p-4 bg-white shrink-0 grid gap-3" :class="code ? 'grid-cols-2' : 'grid-cols-1'">
      
      <a 
        :href="link" 
        target="_blank"
        class="flex items-center justify-center py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-lg transition-colors shadow-sm"
      >
        <svg class="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
        阅读原文
      </a>

      <a 
        v-if="code"
        :href="code" 
        target="_blank"
        class="flex items-center justify-center py-2 bg-gray-50 hover:bg-gray-100 text-gray-700 text-xs font-bold rounded-lg transition-colors border border-gray-200"
      >
        <svg class="w-3.5 h-3.5 mr-1.5" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path></svg>
        查看代码
      </a>

    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: { type: String, default: 'Untitled Paper' },
  image: { type: String, default: '' },
  conference: { type: String, default: 'Research' },
  authors: { type: String, default: '' },
  description: { type: String, default: '' },
  date: { type: String, default: '2024' },
  link: { type: String, default: '#' },
  code: { type: String, default: '' }
})

const defaultImage = '/paper_images/default-cover.jpg'

const venueConfig = computed(() => {
  const v = (props.conference || '').toLowerCase()
  if (/cvpr|iccv|eccv|neurips|icml|iclr|aaai|acl/.test(v)) {
    return { style: 'bg-purple-50 text-purple-700 border-purple-200' }
  }
  if (v.includes('arxiv')) {
    return { style: 'bg-gray-50 text-gray-600 border-gray-200' }
  }
  if (/blog|openai|google|meta|deepmind|seed|apple|tech report/.test(v)) {
    return { style: 'bg-teal-50 text-teal-700 border-teal-200' }
  }
  return { style: 'bg-blue-50 text-blue-700 border-blue-200' }
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 3px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.5);
}
</style>