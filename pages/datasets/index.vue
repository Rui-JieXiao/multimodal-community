<template>
  <div class="font-inter min-h-screen bg-gray-50 pb-12">
    
    <SectionHeader 
      title="开源数据"
      :subtitles="[
        '收录多模态领域经典与前沿数据集，提供高质量的基础模型训练与评测资源。'
      ]"
    />

    <div class="container mx-auto px-4">
        
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 mb-8 overflow-hidden transition-all duration-300">
          
          <div class="px-6 py-6 flex flex-col gap-5">
            
            <div class="flex flex-col md:flex-row md:items-start gap-3">
              <span class="text-sm font-bold text-slate-900 pt-1.5 shrink-0 w-12">模态</span>
              <div class="flex flex-wrap gap-2">
                <button 
                  @click="toggleModality('All')"
                  :class="selectedModalities.length === 0 ? 'bg-slate-900 text-white shadow-md' : 'text-gray-600 bg-gray-50 hover:bg-gray-100'"
                  class="px-3 py-1 rounded-md text-xs font-medium transition-all duration-200 border border-transparent"
                >
                  全部
                </button>
                <button 
                  v-for="mod in availableModalities" 
                  :key="mod"
                  @click="toggleModality(mod)"
                  :class="selectedModalities.includes(mod) ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 bg-white border border-gray-200 hover:border-blue-400 hover:text-blue-600'"
                  class="px-3 py-1 rounded-md text-xs font-medium transition-all duration-200 flex items-center gap-1"
                >
                  <span v-if="selectedModalities.includes(mod)">✓</span>
                  {{ mod }}
                </button>
              </div>
            </div>

            <div class="flex flex-col md:flex-row md:items-start gap-3">
              <span class="text-sm font-bold text-slate-900 pt-1.5 shrink-0 w-12">语言</span>
              <div class="flex flex-wrap gap-2">
                 <button 
                  v-for="lang in languageOptions" 
                  :key="lang.value"
                  @click="selectLanguage(lang.value)"
                  :class="selectedLangMode === lang.value ? 'bg-slate-900 text-white shadow-md' : 'text-gray-600 bg-gray-50 hover:bg-gray-100'"
                  class="px-3 py-1 rounded-md text-xs font-medium transition-all duration-200 border border-transparent"
                >
                  {{ lang.label }}
                </button>
              </div>
            </div>

            <div class="flex flex-col md:flex-row md:items-start gap-3">
              <span class="text-sm font-bold text-slate-900 pt-1.5 shrink-0 w-12">规模</span>
              <div class="flex flex-wrap gap-2">
                <button 
                  v-for="scale in scaleOptions" 
                  :key="scale.value"
                  @click="selectScale(scale.value)"
                  :class="selectedScale === scale.value ? 'bg-slate-900 text-white shadow-md' : 'text-gray-600 bg-gray-50 hover:bg-gray-100'"
                  class="px-3 py-1 rounded-md text-xs font-medium transition-all duration-200 border border-transparent"
                >
                  {{ scale.label }}
                </button>
              </div>
            </div>

          </div>

          <div class="bg-gray-50/50 px-6 py-4 flex flex-col md:flex-row items-center gap-4 border-t border-gray-100">
            <div class="flex-1 w-full relative">
              <input 
                v-model="searchKeyword"
                @input="resetPage"
                type="text" 
                placeholder="搜索数据集名称或描述..." 
                class="w-full pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-50 outline-none transition-all shadow-sm"
              >
              <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>

            <div class="flex items-center gap-4 shrink-0 w-full md:w-auto justify-between md:justify-end">
              <span class="text-xs text-gray-500">
                共找到 <strong class="text-slate-900 text-base mx-0.5">{{ filteredDatasets.length }}</strong> 个数据集
              </span>
              <button @click="resetFilters" class="text-xs text-gray-400 hover:text-blue-600 flex items-center gap-1 transition-colors">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg> 
                重置
              </button>
            </div>
          </div>

        </div>

        <div v-if="paginatedDatasets.length > 0">
            <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5 mb-12">
              <DatasetCard 
                v-for="(item, index) in paginatedDatasets" 
                :key="index" 
                :title="item.title"
                :description="item.description"
                :modalities="item.modalities"
                :languages="item.languages"
                :year="item.year"
                :samples="item.samples"
                :access_url="item.access_url"
                :reference_url="item.reference_url"
              />
            </div>

            <div class="flex flex-col md:flex-row justify-center items-center gap-4 py-8 border-t border-gray-100 select-none">
                <button 
                  @click="changePage(currentPage - 1)" 
                  :disabled="currentPage === 1"
                  class="w-9 h-9 flex items-center justify-center rounded-lg border border-gray-200 text-gray-500 hover:bg-white hover:text-blue-600 hover:border-blue-200 disabled:opacity-30 disabled:hover:bg-transparent disabled:cursor-not-allowed transition-all bg-white"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
                </button>

                <div class="flex items-center gap-1.5">
                  <template v-for="(page, index) in smartPageNumbers" :key="index">
                    <span v-if="page === '...'" class="px-2 text-gray-400 text-sm font-medium tracking-widest">...</span>
                    <button 
                      v-else 
                      @click="changePage(page)"
                      :class="currentPage === page ? 'bg-slate-900 text-white border-slate-900 shadow-md transform scale-105' : 'bg-white text-gray-600 border-gray-200 hover:border-blue-300 hover:text-blue-600'"
                      class="w-9 h-9 text-sm font-medium rounded-lg border transition-all duration-200 flex items-center justify-center"
                    >
                      {{ page }}
                    </button>
                  </template>
                </div>

                <button 
                  @click="changePage(currentPage + 1)" 
                  :disabled="currentPage === totalPages"
                  class="w-9 h-9 flex items-center justify-center rounded-lg border border-gray-200 text-gray-500 hover:bg-white hover:text-blue-600 hover:border-blue-200 disabled:opacity-30 disabled:hover:bg-transparent disabled:cursor-not-allowed transition-all bg-white"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                </button>
                
                <div class="flex items-center gap-2 ml-4 pl-4 border-l border-gray-200 hidden md:flex">
                    <span class="text-sm text-gray-500">跳转至</span>
                    <div class="relative">
                      <input 
                        v-model.number="jumpTarget" 
                        @keyup.enter="handleJump"
                        type="number" 
                        min="1" 
                        :max="totalPages"
                        class="w-16 pl-2 pr-1 py-1.5 text-sm text-center border border-gray-200 rounded-md focus:border-blue-500 focus:ring-1 focus:ring-blue-100 outline-none transition-all"
                      >
                    </div>
                    <span class="text-sm text-gray-500">页</span>
                    <button 
                      @click="handleJump"
                      class="text-sm text-blue-600 hover:text-blue-800 font-medium ml-1 px-2 py-1 hover:bg-blue-50 rounded"
                    >
                      Go
                    </button>
                  </div>
              </div>
        </div>

        <div v-else class="text-center py-24 bg-white rounded-xl border border-dashed border-gray-200">
          <div class="inline-flex items-center justify-center w-14 h-14 rounded-full bg-gray-50 mb-3">
            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>
          </div>
          <p class="text-gray-500 text-sm">没有找到符合组合条件的数据集</p>
          <button @click="resetFilters" class="mt-2 text-sm text-blue-600 font-medium hover:underline">
            重置所有筛选
          </button>
        </div>

      </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import datasetsData from '@/assets/data/datasets_data.json'
import DatasetCard from '@/components/DatasetCard.vue'

const PAGE_SIZE = 9 // 👈 每页9个卡片 (3x3)

// ================= 配置数据 =================

// 1. 模态选项
const availableModalities = [
  'Image', 'Text', 'Video', 'Audio', '3D', 'Spatial Prompts'
]

// 2. 语言选项
const languageOptions = [
  { label: '全部', value: '' },
  { label: 'English', value: 'English' },
  { label: 'Chinese', value: 'Chinese' },
  { label: 'Multilingual', value: 'Multilingual' }
]

// 3. 规模选项
const scaleOptions = [
  { label: '全部', value: '' },
  { label: '< 100K (小型)', value: 'small' },
  { label: '100K - 1M (中型)', value: 'medium' },
  { label: '> 1M (大型)', value: 'large' }
]

// ================= 状态定义 =================

const searchKeyword = ref('')
const selectedModalities = ref([]) 
const selectedLangMode = ref('')   
const selectedScale = ref('')      
const currentPage = ref(1) // 👈 当前页码
const jumpTarget = ref('') // 👈 跳转目标

// ================= 动作逻辑 =================

const resetPage = () => {
  currentPage.value = 1
}

// A. 模态多选逻辑 (带重置页码)
const toggleModality = (mod) => {
  if (mod === 'All') {
    selectedModalities.value = []
  } else {
    const idx = selectedModalities.value.indexOf(mod)
    if (idx > -1) {
      selectedModalities.value.splice(idx, 1)
    } else {
      selectedModalities.value.push(mod)
    }
  }
  resetPage() // 👈 状态同步
}

// B. 语言互斥逻辑 (带重置页码)
const selectLanguage = (val) => {
  if (selectedLangMode.value === val) {
    selectedLangMode.value = ''
  } else {
    selectedLangMode.value = val
  }
  resetPage() // 👈 状态同步
}

// C. 规模筛选逻辑 (带重置页码)
const selectScale = (val) => {
  if (selectedScale.value === val) {
    selectedScale.value = ''
  } else {
    selectedScale.value = val
  }
  resetPage() // 👈 状态同步
}

const resetFilters = () => {
  searchKeyword.value = ''
  selectedModalities.value = []
  selectedLangMode.value = ''
  selectedScale.value = ''
  resetPage()
  jumpTarget.value = ''
}

// ================= 核心算法：规模解析 =================
const parseSamples = (str) => {
  if (!str || typeof str !== 'string') return 0
  
  // 提取数字部分
  let numStr = str.replace(/[^0-9.]/g, '')
  let num = parseFloat(numStr)
  if (isNaN(num)) return 0
  
  const upper = str.toUpperCase()
  if (upper.includes('M') || upper.includes('MILLION')) num *= 1000000
  else if (upper.includes('K')) num *= 1000
  else if (upper.includes('B')) num *= 1000000000 
  
  return num
}

// ================= 核心过滤计算 =================

const filteredDatasets = computed(() => {
  return datasetsData.filter(item => {
    
    // 1. 搜索过滤
    if (searchKeyword.value) {
      const kw = searchKeyword.value.toLowerCase()
      const inTitle = item.title?.toLowerCase().includes(kw)
      const inDesc = item.description?.toLowerCase().includes(kw)
      if (!inTitle && !inDesc) return false
    }

    // 2. 模态过滤 (精准交集 - AND 逻辑)
    if (selectedModalities.value.length > 0) {
      const itemMods = (item.modalities || []).map(m => m.toLowerCase())
      const hasAllMatches = selectedModalities.value.every(sel => 
        itemMods.some(im => im.includes(sel.toLowerCase()))
      )
      if (!hasAllMatches) return false
    }

    // 3. 语言过滤 (包容逻辑)
    if (selectedLangMode.value) {
      const itemLangs = (item.languages || []).map(l => l.toLowerCase())
      const target = selectedLangMode.value.toLowerCase()
      
      const isMultiDataset = itemLangs.some(l => /^multi/i.test(l)) || itemLangs.length >= 3

      if (target === 'multilingual') {
        if (!isMultiDataset) return false
      } else {
        const hasSpecificLang = itemLangs.some(l => l.includes(target))
        if (!hasSpecificLang && !isMultiDataset) return false
      }
    }

    // 4. 规模过滤
    if (selectedScale.value) {
      const num = parseSamples(item.samples)
      if (selectedScale.value === 'small' && num >= 100000) return false
      if (selectedScale.value === 'medium' && (num < 100000 || num > 1000000)) return false
      if (selectedScale.value === 'large' && num <= 1000000) return false
    }

    return true
  })
})

// ================= 分页逻辑 =================

const totalPages = computed(() => Math.ceil(filteredDatasets.value.length / PAGE_SIZE))

const paginatedDatasets = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredDatasets.value.slice(start, start + PAGE_SIZE)
})

// 🟢 智能页码 (Delta = 2)
const smartPageNumbers = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const delta = 2 
  const range = []
  const rangeWithDots = []
  let l
  for (let i = 1; i <= total; i++) {
    if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) range.push(i)
  }
  for (let i of range) {
    if (l) {
      if (i - l === 2) rangeWithDots.push(l + 1)
      else if (i - l !== 1) rangeWithDots.push('...')
    }
    rangeWithDots.push(i)
    l = i
  }
  return rangeWithDots
})

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    scrollToTop()
  }
}

const handleJump = () => {
  const target = parseInt(jumpTarget.value)
  if (target >= 1 && target <= totalPages.value) {
    currentPage.value = target
    jumpTarget.value = ''
    scrollToTop()
  }
}
</script>