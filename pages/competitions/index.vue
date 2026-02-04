<template>
  <div class="min-h-screen bg-gray-50 pb-12">
    
    <SectionHeader 
      title="竞赛挑战"
      :subtitles="[
        '汇聚全球顶级多模态算法竞赛，提供真实场景数据，赢取丰厚奖金与学术荣誉。'
      ]"
    />

    <div class="container mx-auto px-4">
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 mb-8 overflow-hidden">
        
        <div class="px-8 py-5 flex items-center gap-12">
          <span class="text-sm font-bold text-dark shrink-0">状态</span>
          <div class="flex flex-wrap gap-4"> 
            <button 
              v-for="status in statusOptions" 
              :key="status.value"
              @click="selectStatus(status.value)"
              :class="[
                'text-sm font-medium px-5 py-2 rounded-full transition-all duration-200 flex items-center gap-2 border',
                selectedStatus === status.value 
                  ? 'bg-dark text-white border-dark shadow-md' 
                  : 'bg-white text-gray-600 border-transparent hover:bg-gray-50'
              ]"
            >
              <span v-if="status.value !== 'all'" :class="[
                'w-1.5 h-1.5 rounded-full',
                selectedStatus === status.value ? 'bg-white' : status.dotColor
              ]"></span>
              {{ status.label }}
            </button>
          </div>
        </div>

        <div class="border-t border-dashed border-gray-100 mx-8"></div>

        <div class="px-8 py-5 flex items-center gap-12">
          <span class="text-sm font-bold text-dark shrink-0">搜索</span>
          
          <div class="flex-1 flex flex-col md:flex-row items-center gap-8">
            <div class="relative flex-1 w-full">
              <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
              <input 
                v-model="searchKeyword"
                @input="resetPage"
                type="text" 
                placeholder="搜索竞赛标题、源会议或关键词..." 
                class="w-full pl-11 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-dark placeholder-gray-400 focus:bg-white focus:border-primary focus:ring-4 focus:ring-blue-50 outline-none transition-all"
              />
            </div>
            
            <div class="flex items-center gap-6 shrink-0 w-full md:w-auto justify-between md:justify-start">
              <span class="text-sm text-gray-500 whitespace-nowrap">
                共 <strong class="text-primary font-bold text-base mx-0.5">{{ sortedAndFilteredItems.length }}</strong> 条结果
              </span>
              
              <button 
                @click="resetFilters"
                class="flex items-center gap-1.5 text-sm font-bold text-gray-400 hover:text-primary transition-colors border-l pl-6 border-gray-200"
                title="重置所有筛选条件"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                重置
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="paginatedItems.length > 0">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12">
          <CompetitionCard 
            v-for="(item, index) in paginatedItems" 
            :key="item.id || index" 
            :competition="item"
            :status="item._status" 
            :search-keyword="searchKeyword"
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

      <div v-else class="py-24 text-center bg-white rounded-xl border border-dashed border-gray-200">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-50 mb-4">
          <svg class="w-8 h-8 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"></path></svg>
        </div>
        <p class="text-gray-500 font-medium">暂无符合条件的赛事</p>
        <button @click="resetFilters" class="mt-4 text-primary text-sm font-bold hover:underline flex items-center gap-1 mx-auto">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
          清除所有筛选条件
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import competitionsData from '~/assets/data/competitions_data.json'

const PAGE_SIZE = 4 

const searchKeyword = ref('')
const selectedStatus = ref('all') // 默认为 'all'
const currentPage = ref(1)
const jumpTarget = ref('')

const statusOptions = [
  { label: '全部', value: 'all', dotColor: '' },
  { label: '进行中的竞赛', value: 'active', dotColor: 'bg-emerald-500' },
  { label: '未开始的竞赛', value: 'upcoming', dotColor: 'bg-blue-500' },
  { label: '已结束的竞赛', value: 'ended', dotColor: 'bg-gray-400' }
]

// 🛠️ 竞赛专用日期解析逻辑
const calculateStatusAndWeight = (dateRangeStr) => {
  const result = { status: 'ended', weight: 2, sortDate: 0 }
  if (!dateRangeStr) return result

  const matches = dateRangeStr.match(/\d{4}[\.\-\/]\d{2}[\.\-\/]\d{2}/g)
  if (!matches || matches.length === 0) return result

  const dates = matches.map(d => new Date(d.replace(/[\.\/]/g, '-'))).sort((a, b) => a - b)
  
  const now = new Date()
  const startDate = dates[0]
  const endDate = dates[dates.length - 1]
  // 截止时间设为当天最晚
  endDate.setHours(23, 59, 59, 999)

  if (now > endDate) {
    // 已结束 (权重 2)
    result.status = 'ended'
    result.weight = 2
    result.sortDate = endDate.getTime()
  } else if (now < startDate) {
    // 未开始 (权重 1)
    result.status = 'upcoming'
    result.weight = 1
    result.sortDate = startDate.getTime()
  } else {
    // 进行中 (权重 0)
    result.status = 'active'
    result.weight = 0
    result.sortDate = endDate.getTime()
  }

  return result
}

const resetPage = () => {
  currentPage.value = 1
}

const selectStatus = (val) => {
  selectedStatus.value = val
  resetPage()
}

const resetFilters = () => {
  searchKeyword.value = ''
  selectedStatus.value = 'all'
  resetPage()
  jumpTarget.value = ''
}

// 🟢 核心：预处理 -> 筛选 -> 排序 (隐藏逻辑)
const sortedAndFilteredItems = computed(() => {
  // 1. 预处理
  const processed = competitionsData.map(item => {
    const { status, weight, sortDate } = calculateStatusAndWeight(item.date_range)
    return { 
      ...item, 
      _status: status, 
      _weight: weight,
      _sortDate: sortDate 
    }
  })

  // 2. 筛选 (支持标题、HostEvent、描述三位一体搜索)
  const filtered = processed.filter(item => {
    const isStatusMatch = selectedStatus.value === 'all' || item._status === selectedStatus.value
    
    const query = searchKeyword.value.toLowerCase()
    
    // 三字段联合匹配
    const isTitleMatch = (item.title || '').toLowerCase().includes(query)
    const isHostMatch = (item.host_event || '').toLowerCase().includes(query)
    const isDescMatch = (item.description || '').toLowerCase().includes(query)

    return isStatusMatch && (isTitleMatch || isHostMatch || isDescMatch)
  })

  // 3. 排序 (权重优先 -> 日期次之)
  return filtered.sort((a, b) => {
    // 优先级 1: 状态权重 (Active 0 -> Upcoming 1 -> Ended 2)
    if (a._weight !== b._weight) return a._weight - b._weight

    // 优先级 2: 同状态内的日期逻辑
    if (a._weight === 0) {
      // 进行中：按截止日期升序 (越快截止排越前，紧迫感)
      return a._sortDate - b._sortDate
    } else if (a._weight === 1) {
      // 未开始：按开始日期升序 (越快开始排越前)
      return a._sortDate - b._sortDate
    } else {
      // 已结束：按结束日期降序 (刚结束的排前面)
      return b._sortDate - a._sortDate
    }
  })
})

// ================= 分页逻辑 =================

const totalPages = computed(() => Math.ceil(sortedAndFilteredItems.value.length / PAGE_SIZE))

const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return sortedAndFilteredItems.value.slice(start, start + PAGE_SIZE)
})

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

useHead({
  title: '竞赛挑战 - Multimodal Open Community'
})
</script>