<template>
  <div class="font-inter min-h-screen bg-gray-50 pb-12">
    
    <SectionHeader 
      title="精选文献"
      :subtitles="[
        '精选 CVPR、NeurIPS、ICLR 等顶会及 arXiv 科研文献。',
        '涵盖多模态表征、模态对齐、视觉语言推理及指令微调等核心领域。'
      ]"
    />

    <div class="container mx-auto px-4">
        
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 mb-8 overflow-hidden">
            
            <div class="px-8 py-5 flex flex-col md:flex-row gap-4 md:items-start">
                <span class="text-sm font-bold text-slate-900 pt-1.5 shrink-0 w-16">领域</span>
                <div class="flex flex-wrap gap-2">
                      <button 
                        v-for="(label, key) in displayDomains" 
                        :key="key"
                        @click="selectDomain(key)"
                        :class="selectedDomain === key ? 'bg-slate-900 text-white shadow-md' : 'text-gray-600 hover:text-blue-600 bg-transparent hover:bg-gray-50'"
                        class="px-4 py-1.5 rounded-full text-sm font-medium transition-all duration-200 border border-transparent"
                      >
                        {{ label }}
                      </button>
                </div>
            </div>

            <div class="border-t border-dashed border-gray-100 mx-8"></div>

            <div class="px-8 py-5 flex flex-col md:flex-row gap-4 md:items-start">
                 <span class="text-sm font-bold text-slate-900 pt-1.5 shrink-0 w-16">来源</span>
                 <div class="flex flex-wrap gap-2">
                    <button 
                        v-for="item in ['全部', ...mainVenues, '其他']" 
                        :key="item"
                        @click="selectConference(item)"
                        :class="isSelected(selectedConference, item) ? 'bg-slate-900 text-white shadow-md' : 'text-gray-600 hover:text-blue-600 bg-transparent hover:bg-gray-50'"
                        class="px-4 py-1.5 rounded-full text-sm font-medium transition-all duration-200 border border-transparent"
                      >
                        {{ item }}
                      </button>
                 </div>
            </div>

            <div class="border-t border-dashed border-gray-100 mx-8"></div>

            <div class="px-8 py-5 flex flex-col md:flex-row items-center gap-6">
                <span class="text-sm font-bold text-slate-900 shrink-0 w-16 hidden md:block">筛选</span>

                <div class="flex-1 w-full flex flex-col md:flex-row gap-4">
                    <div class="relative shrink-0 w-full md:w-32">
                        <select 
                          v-model="selectedYear" 
                          @change="resetPage"
                          class="w-full pl-4 pr-8 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 appearance-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 focus:bg-white outline-none transition-all cursor-pointer"
                        >
                          <option value="">全部年份</option>
                          <option v-for="year in dynamicYearOptions" :key="year" :value="year">
                            {{ year }}
                          </option>
                        </select>
                        <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </div>

                    <button 
                        @click="toggleOpenSource"
                        :class="onlyShowOpenSource ? 'bg-green-50 border-green-200 text-green-700' : 'bg-gray-50 border-gray-200 text-gray-600 hover:bg-white'"
                        class="shrink-0 flex items-center justify-center gap-2 px-4 py-2.5 border rounded-lg text-sm font-medium transition-all select-none"
                      >
                        <div 
                          class="w-4 h-4 rounded border flex items-center justify-center transition-colors"
                          :class="onlyShowOpenSource ? 'bg-green-500 border-green-500' : 'border-gray-400 bg-white'"
                        >
                          <svg v-if="onlyShowOpenSource" class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
                        </div>
                        只看已开源
                    </button>

                    <div class="relative flex-1">
                        <input 
                          v-model="searchKeyword"
                          @input="resetPage" 
                          type="text" 
                          placeholder="搜索论文标题..." 
                          class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-100 focus:bg-white outline-none transition-all"
                        >
                        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                    </div>
                </div>

                <div class="flex items-center gap-6 shrink-0 w-full md:w-auto justify-end mt-2 md:mt-0">
                      <span class="text-sm text-gray-500 whitespace-nowrap">
                        共 <strong class="text-blue-600 text-lg mx-0.5">{{ filteredPapers.length }}</strong> 篇
                      </span>
                      <button @click="resetFilters" class="text-sm text-gray-400 hover:text-slate-900 flex items-center gap-1 transition-colors">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg> 
                        重置
                      </button>
                </div>
            </div>

        </div>

        <div v-if="paginatedPapers.length > 0">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            <PaperCard 
              v-for="(item, index) in paginatedPapers" 
              :key="index" 
              :title="item.title"
              :conference="item.venue"
              :date="item.date"
              :authors="item.authors"
              :description="item.description"
              :image="item.image"
              :link="item.link"
              :code="item.code"
              :tags="item.tags" 
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

        <div v-else class="text-center py-24">
          <p class="text-gray-500 text-lg">没有找到匹配的论文</p>
          <button @click="resetFilters" class="mt-4 text-sm text-blue-600 font-medium hover:underline">
            清除所有筛选
          </button>
        </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import papersData from '@/assets/data/papers_data.json'
import PaperCard from '@/components/PaperCard.vue'

const PAGE_SIZE = 12 

// --- 状态定义 ---
const searchKeyword = ref('')
const selectedDomain = ref('') 
const selectedConference = ref('')
const selectedYear = ref('')
const onlyShowOpenSource = ref(false) 
const currentPage = ref(1)
const jumpTarget = ref('') 

// 🟢 智能动态年份计算
const dynamicYearOptions = computed(() => {
  if (!papersData || papersData.length === 0) return ['2026']
  const yearSet = new Set()
  yearSet.add(2026)
  papersData.forEach(p => {
    const match = (p.date || '').toString().match(/\d{4}/)
    if (match) {
      yearSet.add(parseInt(match[0]))
    }
  })
  return Array.from(yearSet).sort((a, b) => b - a).map(String)
})

// --- 领域映射字典 ---
const displayDomains = {
  '': '全部',
  'Representation': '表征学习',
  'Fusion': '模态融合',
  'Alignment': '模态对齐',
  'Instruction Tuning': '指令微调',
  'Hallucination': '幻觉研究',
  'In-Context Learning': '上下文学习',
  'Chain-of-Thought': '思维链',
  'Visual Reasoning': '视觉推理',
  'Foundation Models': '基础模型',
  'Evaluation': '评测基准',
  'RLHF': 'RLHF',
  'Others': '其他'
}

const mainVenues = ['CVPR', 'ICCV', 'ECCV', 'NeurIPS', 'ICML', 'ICLR', 'arXiv']

const isSelected = (currentValue, itemValue) => {
  if (itemValue === '全部') return currentValue === ''
  return currentValue === itemValue
}

// 🟢 筛选动作：每次筛选变动都重置页码为 1
const selectDomain = (key) => {
  selectedDomain.value = key
  currentPage.value = 1 
}

const selectConference = (item) => {
  selectedConference.value = item === '全部' ? '' : item
  currentPage.value = 1 
}

const toggleOpenSource = () => {
  onlyShowOpenSource.value = !onlyShowOpenSource.value
  currentPage.value = 1
}

const resetPage = () => {
  currentPage.value = 1
}

// 🟢 核心过滤逻辑
const filteredPapers = computed(() => {
  return papersData.filter(paper => {
    const matchSearch = searchKeyword.value ? paper.title.toLowerCase().includes(searchKeyword.value.toLowerCase()) : true
    const matchDomain = selectedDomain.value ? (paper.tags && paper.tags.includes(selectedDomain.value)) : true
    
    // 会议筛选
    let matchConf = true
    if (selectedConference.value) {
      const paperVenue = (paper.venue || '').toLowerCase()
      if (selectedConference.value === '其他') {
        const isMainstream = mainVenues.some(venue => paperVenue.includes(venue.toLowerCase()))
        matchConf = !isMainstream
      } else {
        if (selectedConference.value === 'NeurIPS') {
          matchConf = paperVenue.includes('neurips') || paperVenue.includes('nips')
        } else {
          matchConf = paperVenue.includes(selectedConference.value.toLowerCase())
        }
      }
    }

    const matchYear = selectedYear.value ? (paper.date || '').toString().includes(selectedYear.value) : true
    const matchCode = onlyShowOpenSource.value ? !!paper.code : true
      
    return matchSearch && matchDomain && matchConf && matchYear && matchCode
  })
})

const totalPages = computed(() => Math.ceil(filteredPapers.value.length / PAGE_SIZE))

// 🟢 分页数据切片
const paginatedPapers = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredPapers.value.slice(start, start + PAGE_SIZE)
})

// 🟢 智能页码算法 (Delta = 2)
const smartPageNumbers = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const delta = 2 // 👈 修改为2，展示更多页码
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

// 🟢 辅助函数：平滑滚动至顶部
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 🟢 翻页动作 (带自动滚动)
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

const resetFilters = () => {
  searchKeyword.value = ''
  selectedDomain.value = ''
  selectedConference.value = ''
  selectedYear.value = ''
  onlyShowOpenSource.value = false
  currentPage.value = 1
}
</script>