<template>
  <div class="min-h-screen bg-gray-50 pb-12">
    
    <SectionHeader 
      title="征稿专栏"
      :subtitles="[
        '汇总国内外多模态相关会议 Workshop、特刊及学术期刊的征稿动态。'
      ]"
    />

    <div class="container mx-auto px-4">
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 mb-8 overflow-hidden">
        
        <div class="px-8 py-5 flex items-center gap-12">
          <span class="text-sm font-bold text-dark shrink-0">状态</span>
          <div class="flex flex-wrap gap-8">
            <button 
              v-for="status in statusOptions" 
              :key="status.value"
              @click="selectStatus(status.value)"
              :class="[
                'text-sm font-medium px-5 py-2 rounded-full transition-all duration-200 flex items-center gap-2 border',
                currentStatus === status.value 
                  ? 'bg-dark text-white border-dark shadow-md' 
                  : 'bg-white text-gray-600 border-transparent hover:bg-gray-50'
              ]"
            >
              <span v-if="status.value !== 'all'" :class="[
                'w-1.5 h-1.5 rounded-full',
                currentStatus === status.value ? 'bg-white' : status.dotColor
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
                v-model="searchQuery"
                @input="resetPage"
                type="text" 
                placeholder="搜索征稿主题、来源或关键词..." 
                class="w-full pl-11 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-dark placeholder-gray-400 focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-100 outline-none transition-all"
              />
            </div>
            
            <div class="flex items-center gap-6 shrink-0 w-full md:w-auto justify-between md:justify-start">
              <span class="text-sm text-gray-500 whitespace-nowrap">
                共 <strong class="text-blue-600 font-bold text-base mx-0.5">{{ sortedAndFilteredCfps.length }}</strong> 条结果
              </span>
              
              <button 
                @click="resetFilters"
                class="flex items-center gap-1.5 text-sm font-bold text-gray-400 hover:text-blue-600 transition-colors border-l pl-6 border-gray-200"
                title="重置所有筛选条件"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                重置
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="paginatedCfps.length > 0">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12">
          <CfpCard
            v-for="item in paginatedCfps"
            :key="item.id"
            v-bind="item"
            :status="item._status" 
            :search-keyword="searchQuery"
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
          <svg class="w-8 h-8 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        </div>
        <p class="text-gray-500 font-medium">没有找到符合条件的征稿</p>
        <button @click="resetFilters" class="mt-4 text-blue-600 text-sm font-bold hover:underline flex items-center gap-1 mx-auto">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
          清除所有筛选条件
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import CfpCard from '~/components/CfpCard.vue'
import rawCfpData from '~/assets/data/cfp_data.json'
import { ref, computed } from 'vue'

const PAGE_SIZE = 4 

const searchQuery = ref('')
const currentStatus = ref('all')
const currentPage = ref(1)
const jumpTarget = ref('')

const statusOptions = [
  { label: '全部', value: 'all', dotColor: '' },
  { label: '进行中的征稿', value: 'open', dotColor: 'bg-green-500' },
  { label: '未开始的征稿', value: 'upcoming', dotColor: 'bg-blue-500' },
  { label: '已结束的征稿', value: 'closed', dotColor: 'bg-gray-400' }
]

// 🛠️ 增强版日期解析工具：根据连接符智能识别状态
const calculateStatusAndWeight = (dateRangeString) => {
  const result = { status: 'closed', weight: 2, sortDate: 0 }
  
  if (!dateRangeString) return result

  // 1. 正则提取所有日期 (YYYY-MM-DD 或 YYYY.MM.DD)
  const matches = dateRangeString.match(/\d{4}[\.\-\/]\d{2}[\.\-\/]\d{2}/g)
  
  if (!matches || matches.length === 0) return result

  // 2. 转换日期对象并排序
  const dates = matches.map(d => new Date(d.replace(/[\.\/]/g, '-'))).sort((a, b) => a - b)
  
  const now = new Date()
  // 设置最晚截止时间为当天的 23:59:59，避免当天被判定为已结束
  const latestDate = new Date(dates[dates.length - 1])
  latestDate.setHours(23, 59, 59, 999)

  // 3. 核心判定逻辑
  if (now > latestDate) {
    // 优先级最高：如果当前时间晚于所有日期 -> 已结束
    result.status = 'closed'
    result.weight = 2
    result.sortDate = latestDate.getTime()
  } 
  // 检查是否包含 "——" (长破折号)，这代表时间区间
  else if (dateRangeString.includes('——')) {
    const startDate = new Date(dates[0])
    if (now < startDate) {
      // 只有在明确是区间且当前时间早于开始时间 -> 未开始
      result.status = 'upcoming'
      result.weight = 1
      result.sortDate = startDate.getTime()
    } else {
      // 在区间内 -> 进行中
      result.status = 'open'
      result.weight = 0
      result.sortDate = latestDate.getTime()
    }
  } 
  // 其他情况 (单日期 OR 多截稿日期如 "Date A / Date B")
  // 只要还没过 latestDate (上面已排除)，都算 Open
  else {
    result.status = 'open'
    result.weight = 0
    result.sortDate = latestDate.getTime()
  }

  return result
}

const resetPage = () => {
  currentPage.value = 1
}

const selectStatus = (val) => {
  currentStatus.value = val
  resetPage()
}

const resetFilters = () => {
  searchQuery.value = ''
  currentStatus.value = 'all'
  resetPage()
  jumpTarget.value = ''
}

// 🟢 核心计算属性：数据注入 -> 筛选 -> 排序
const sortedAndFilteredCfps = computed(() => {
  // 1. 数据注入：计算动态属性
  const processed = rawCfpData.map(item => {
    const { status, weight, sortDate } = calculateStatusAndWeight(item.date_range)
    return { 
      ...item, 
      _status: status, // 注入动态状态
      _weight: weight, // 注入排序权重
      _sortDate: sortDate 
    }
  })

  // 2. 筛选 (支持 title / source / scope 多维搜索)
  const filtered = processed.filter(item => {
    const isStatusMatch = currentStatus.value === 'all' || item._status === currentStatus.value
    
    const query = searchQuery.value.trim().toLowerCase()
    const isSearchMatch = !query || 
                          (item.title || '').toLowerCase().includes(query) || 
                          (item.source || '').toLowerCase().includes(query) ||
                          (item.scope || '').toLowerCase().includes(query) // 新增 scope 搜索
    
    return isStatusMatch && isSearchMatch
  })

  // 3. 排序 (隐藏逻辑核心)
  return filtered.sort((a, b) => {
    // 第一优先级：按状态权重排序 (进行中0 -> 未开始1 -> 已结束2)
    if (a._weight !== b._weight) {
      return a._weight - b._weight
    }
    
    // 第二优先级：同状态下的日期排序
    if (a._weight === 0) {
      // 进行中：截止日期越近越靠前 (升序)，增加紧迫感
      return a._sortDate - b._sortDate 
    } else if (a._weight === 1) {
      // 未开始：开始日期越近越靠前 (升序)
      return a._sortDate - b._sortDate
    } else {
      // 已结束：结束日期越晚越靠前 (降序)，刚结束的排前面
      return b._sortDate - a._sortDate
    }
  })
})

// ================= 分页逻辑 =================

const totalPages = computed(() => Math.ceil(sortedAndFilteredCfps.value.length / PAGE_SIZE))

const paginatedCfps = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return sortedAndFilteredCfps.value.slice(start, start + PAGE_SIZE)
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
</script>