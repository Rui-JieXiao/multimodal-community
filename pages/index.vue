<template>
  <div>
    <section class="relative bg-white min-h-[85vh] flex items-center overflow-hidden">
      <div class="absolute top-0 right-0 w-2/3 h-full bg-gradient-to-l from-blue-50/80 via-blue-50/20 to-transparent pointer-events-none"></div>
      <div class="absolute -bottom-20 -left-20 w-96 h-96 bg-purple-50/50 rounded-full blur-3xl pointer-events-none"></div>

      <div class="container mx-auto px-4 relative z-10 w-full py-12 lg:py-20">
        <div class="flex flex-col lg:flex-row items-center justify-between gap-12 lg:gap-20">
          
          <div class="w-full lg:w-[42%] space-y-8 lg:space-y-10 text-left">
            <a 
              href="https://openai.com/zh-Hans-CN/index/introducing-gpt-5-2/" 
              target="_blank"
              class="inline-flex items-center gap-2 bg-white border border-blue-100 text-primary px-4 py-1.5 rounded-full text-xs md:text-sm font-bold shadow-sm hover:shadow-md hover:scale-105 transition-all cursor-pointer group"
            >
              <span class="flex h-2.5 w-2.5 relative">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-primary"></span>
              </span>
              最新收录 GPT-5.2 技术报告 
              <svg class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity -ml-1 group-hover:ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </a>

            <div class="space-y-2">
              <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight tracking-tight">
                <span class="text-slate-900">多模态</span><span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-blue-600">智能社区</span>
              </h1>
              <div class="text-lg md:text-xl font-medium text-gray-400 tracking-wide font-sans pl-1">
                Multimodal Intelligence Community
              </div>
            </div>
            
            <p class="text-lg md:text-xl text-gray-500 leading-relaxed max-w-xl">
              连接视觉与语言，构建下一代 AGI 知识库。<br class="hidden xl:block">
              这里汇聚了 CVPR,NeurIPS 等顶会精选论文与开源代码。
            </p>

            <div class="flex flex-col sm:flex-row gap-4">
              <NuxtLink to="/papers" class="w-full sm:w-auto justify-center px-8 py-4 bg-primary text-white text-lg font-bold rounded-xl hover:bg-primary-dark transition-all shadow-xl shadow-primary/20 hover:-translate-y-1 flex items-center">
                <svg class="w-5 h-5 mr-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                开始探索
              </NuxtLink>
              
              <button 
                @click="scrollToContact"
                class="w-full sm:w-auto justify-center px-8 py-4 bg-white text-dark border border-gray-200 text-lg font-bold rounded-xl hover:bg-gray-50 transition-all flex items-center shadow-sm hover:shadow-md"
              >
                <svg class="w-5 h-5 mr-2.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path></svg>
                联系我们
              </button>
            </div>

            <div class="pt-8 border-t border-gray-100 grid grid-cols-2 md:grid-cols-4 gap-y-6 gap-x-4">
              <div>
                <div class="text-2xl md:text-3xl font-bold text-dark mb-1">{{ paperCountDisplay }}</div>
                <div class="text-xs text-gray-400 font-medium uppercase tracking-wide">收录论文</div>
              </div>
              <div>
                <div class="text-2xl md:text-3xl font-bold text-dark mb-1">{{ datasetCountDisplay }}</div>
                <div class="text-xs text-gray-400 font-medium uppercase tracking-wide">开源数据</div>
              </div>
              <div>
                <div class="text-2xl md:text-3xl font-bold text-dark mb-1">{{ competitionCountDisplay }}</div>
                <div class="text-xs text-gray-400 font-medium uppercase tracking-wide">竞赛信息</div>
              </div>
              <div>
                <div class="text-2xl md:text-3xl font-bold text-dark mb-1">{{ cfpCountDisplay }}</div>
                <div class="text-xs text-gray-400 font-medium uppercase tracking-wide">征稿信息</div>
              </div>
            </div>

          </div>

          <div class="w-full lg:w-[53%] relative mt-8 lg:mt-0">
            <div class="absolute -inset-1 bg-gradient-to-r from-primary/20 to-purple-500/20 rounded-[2rem] opacity-70 blur-2xl transform rotate-2 pointer-events-none"></div>
            
            <div class="relative bg-white rounded-2xl shadow-2xl shadow-gray-200/50 border border-gray-100 overflow-hidden group hover:shadow-3xl transition-shadow duration-500">
              <swiper
                :modules="[Autoplay, Pagination, Navigation]"
                :slides-per-view="1"
                :space-between="30"
                :loop="true"
                :autoplay="{ delay: 5000, disableOnInteraction: false }"
                :pagination="{ clickable: true, dynamicBullets: true }"
                :navigation="true"
                class="w-full h-auto"
              >
                <swiper-slide>
                  <a href="https://openai.com/zh-Hans-CN/index/introducing-gpt-5-2/" target="_blank" class="block h-full">
                    <div class="h-64 md:h-80 lg:h-96 w-full relative overflow-hidden bg-gray-900 group-slide">
                      <img src="https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=1200&auto=format&fit=crop" class="w-full h-full object-cover opacity-90 group-slide-hover:scale-105 transition-transform duration-700" alt="GPT-5.2" />
                      <div class="absolute inset-0 flex items-center justify-center bg-black/10 group-slide-hover:bg-black/20 transition-colors">
                        <div class="w-16 h-16 md:w-20 md:h-20 bg-white/20 backdrop-blur-md rounded-full flex items-center justify-center text-white border border-white/40 shadow-lg">
                          <svg class="w-6 h-6 md:w-8 md:h-8 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                        </div>
                      </div>
                      <div class="absolute top-4 left-4 md:top-6 md:left-6 flex gap-3">
                        <div class="bg-primary text-white text-xs md:text-sm font-bold px-3 py-1.5 md:px-4 md:py-2 rounded-lg shadow-lg flex items-center gap-2">
                          <svg class="w-3 h-3 md:w-4 md:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                          前沿头条
                        </div>
                      </div>
                    </div>
                    <div class="p-6 md:p-8 flex flex-col md:flex-row md:items-center justify-between gap-4 md:gap-6 bg-white relative z-10">
                      <div class="flex-1 min-w-0 space-y-2 md:space-y-3">
                        <div class="flex items-center gap-3">
                          <span class="text-xs font-bold text-gray-500 border border-gray-200 px-2 py-1 rounded uppercase bg-gray-50">Tech Report</span>
                          <span class="text-xs font-bold text-purple-600 bg-purple-50 px-2 py-1 rounded border border-purple-100">Hot</span>
                        </div>
                        <h3 class="text-xl md:text-2xl font-bold text-dark truncate">GPT-5.2: 超越感知的多模态革命</h3>
                        <p class="text-sm md:text-base text-gray-500 line-clamp-1">OpenAI 最新技术报告，深度解析长视频理解与复杂推理能力。</p>
                      </div>
                      <div class="hidden md:flex px-6 py-3 bg-dark text-white font-bold rounded-xl hover:bg-black transition-colors shrink-0 items-center gap-2 shadow-lg">
                        阅读报告 
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                      </div>
                    </div>
                  </a>
                </swiper-slide>
                <swiper-slide>
                  <a href="https://huggingface.co/spaces/opencompass/open_vlm_leaderboard" target="_blank" class="block h-full">
                     <div class="h-64 md:h-80 lg:h-96 w-full relative overflow-hidden bg-slate-800 group-slide">
                      <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1200&auto=format&fit=crop" class="absolute inset-0 w-full h-full object-cover opacity-30" alt="Data" />
                      <div class="absolute inset-0 flex items-center justify-center">
                        <div class="text-center text-white space-y-2 md:space-y-4 relative z-10">
                          <div class="text-4xl md:text-5xl font-bold tracking-tighter">SOTA</div>
                          <div class="text-base md:text-lg font-mono text-blue-300 bg-black/30 px-4 py-1 rounded-full border border-white/10">Leaderboard 2024</div>
                        </div>
                      </div>
                    </div>
                    <div class="p-6 md:p-8 flex flex-col md:flex-row md:items-center justify-between gap-4 md:gap-6 bg-white relative z-10">
                      <div class="flex-1 min-w-0 space-y-2 md:space-y-3">
                        <h3 class="text-xl md:text-2xl font-bold text-dark truncate">MMMU / MME-RealWorld 实时榜单</h3>
                        <p class="text-sm md:text-base text-gray-500 line-clamp-1">谁是当前最强模型？查看最新的多模态评测基准排名。</p>
                      </div>
                    </div>
                  </a>
                </swiper-slide>
              </swiper>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="container mx-auto px-4 py-12 md:py-20">
      <div class="flex flex-col md:flex-row items-center justify-between mb-8 gap-6">
        <div class="text-center md:text-left">
          <h2 class="text-2xl md:text-3xl font-bold text-dark mb-2">精选论文</h2>
          <p class="text-gray-500 text-sm md:text-base">精选五大核心领域，探索前沿工作。</p>
        </div>
        <div class="flex flex-wrap justify-center gap-2">
          <button v-for="tab in tabs" :key="tab.key" @click="switchTab(tab.key)"
            :class="activeTab === tab.key ? 'bg-slate-900 text-white shadow-md' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
            class="px-3 py-1.5 md:px-4 md:py-2 rounded-full text-xs md:text-sm font-medium transition-all duration-200">
            {{ tab.label }}
          </button>
        </div>
      </div>

      <div class="flex justify-between items-center mb-6 px-1">
        <button @click="refreshPapers" class="text-sm font-medium text-blue-600 flex items-center gap-1.5 hover:text-blue-800 transition-colors group select-none">
          <svg class="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
          换一批
        </button>
        <NuxtLink to="/papers" class="hidden md:flex items-center text-gray-500 hover:text-primary font-medium text-sm transition-colors">
          进入完整论文库 
          <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
        </NuxtLink>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8 min-h-[400px]">
        <PaperCard v-for="(item, index) in displayPapers" :key="item.title + index" v-bind="item" />
      </div>
    </section>

    <section class="bg-gray-50 py-12 md:py-20 border-y border-gray-100">
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between mb-8 md:mb-10">
          <div>
            <h2 class="text-2xl md:text-3xl font-bold text-dark mb-2 md:mb-3">相关数据集</h2>
            <p class="text-gray-500 text-sm md:text-lg">多模态大模型训练所需的经典开源数据集。</p>
          </div>
          
          <div class="flex items-center gap-6">
            <button @click="refreshDatasets" class="text-sm font-medium text-blue-600 flex items-center gap-1.5 hover:text-blue-800 transition-colors group select-none">
              <svg class="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
              换一批
            </button>
            
            <NuxtLink to="/datasets" class="hidden md:flex items-center text-primary font-bold hover:underline text-lg">
              查看全部 
              <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </NuxtLink>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          <DatasetCard 
            v-for="(item, index) in displayDatasets" 
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
      </div>
    </section>

    <section class="container mx-auto px-4 py-12 md:py-20">
      <div class="flex items-center justify-between mb-8 md:mb-10">
        <div>
          <h2 class="text-2xl md:text-3xl font-bold text-dark mb-2 md:mb-3">技术竞赛</h2>
          <p class="text-gray-500 text-sm md:text-lg">关注全球最新的多模态技术挑战赛。</p>
        </div>
        
        <div class="flex items-center gap-6">
            <button @click="refreshCompetitions" class="text-sm font-medium text-blue-600 flex items-center gap-1.5 hover:text-blue-800 transition-colors group select-none">
              <svg class="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
              换一批
            </button>

            <NuxtLink to="/competitions" class="hidden md:flex items-center text-primary font-bold hover:underline text-lg">
            更多比赛 
            <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </NuxtLink>
        </div>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8">
        <CompetitionCard 
          v-for="(item, index) in displayCompetitions" 
          :key="index" 
          :competition="item"
          :status="item._computedStatus"
        />
      </div>
    </section>

    <section class="bg-gray-50 py-12 md:py-20 border-y border-gray-100">
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between mb-8 md:mb-10">
          <div>
            <h2 class="text-2xl md:text-3xl font-bold text-dark mb-2 md:mb-3">征稿专栏</h2>
            <p class="text-gray-500 text-sm md:text-lg">汇总国内外多模态相关会议征稿动态。</p>
          </div>

          <div class="flex items-center gap-6">
            <button @click="refreshCfps" class="text-sm font-medium text-blue-600 flex items-center gap-1.5 hover:text-blue-800 transition-colors group select-none">
              <svg class="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
              换一批
            </button>

            <NuxtLink to="/cfp" class="hidden md:flex items-center text-primary font-bold hover:underline text-lg">
              查看更多 
              <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </NuxtLink>
          </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <CfpCard 
            v-for="(item, index) in displayCfps" 
            :key="item.id || index" 
            v-bind="item"
            :status="item._computedStatus" 
          />
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import papersData from '@/assets/data/papers_data.json'
import datasetsData from '@/assets/data/datasets_data.json' 
import competitionsData from '@/assets/data/competitions_data.json' 
import cfpData from '@/assets/data/cfp_data.json' 

import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Pagination, Navigation } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/navigation'

// 🟢 新增：平滑滚动到底部（联系我们）
const scrollToContact = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}

// 🟢 核心修改：四大板块的动态统计
const paperCountDisplay = computed(() => {
  if (!papersData || papersData.length === 0) return '0+'
  const count = Math.floor(papersData.length / 100) * 100
  return `${count}+`
})

const datasetCountDisplay = computed(() => {
  if (!datasetsData || datasetsData.length === 0) return '0+'
  const count = Math.floor(datasetsData.length / 10) * 10
  return `${count}+`
})

const competitionCountDisplay = computed(() => {
  if (!competitionsData || competitionsData.length === 0) return '0+'
  const count = Math.floor(competitionsData.length / 10) * 10
  return `${count}+`
})

const cfpCountDisplay = computed(() => {
  if (!cfpData || cfpData.length === 0) return '0+'
  const count = Math.floor(cfpData.length / 10) * 10
  return `${count}+`
})

// --- 通用工具函数 ---
const shuffleArray = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

// 🟢 竞赛日期状态计算函数
const calculateCompetitionStatus = (dateRangeStr) => {
  if (!dateRangeStr) return 'ended'

  const matches = dateRangeStr.match(/\d{4}[\.\-\/]\d{2}[\.\-\/]\d{2}/g)
  if (!matches || matches.length === 0) return 'ended'

  const dates = matches.map(d => new Date(d.replace(/[\.\/]/g, '-'))).sort((a, b) => a - b)
  
  const now = new Date()
  const startDate = dates[0]
  const endDate = dates[dates.length - 1]
  endDate.setHours(23, 59, 59, 999)

  if (now > endDate) {
    return 'ended'
  } else if (now < startDate) {
    return 'upcoming'
  } else {
    return 'active'
  }
}

// 🟢 征稿日期状态计算函数
const calculateCfpStatus = (dateRangeString) => {
  if (!dateRangeString) return 'closed'

  const matches = dateRangeString.match(/\d{4}[\.\-\/]\d{2}[\.\-\/]\d{2}/g)
  if (!matches || matches.length === 0) return 'closed'

  const dates = matches.map(d => new Date(d.replace(/[\.\/]/g, '-'))).sort((a, b) => a - b)
  
  const now = new Date()
  const latestDate = new Date(dates[dates.length - 1])
  latestDate.setHours(23, 59, 59, 999)

  if (now > latestDate) {
    return 'closed'
  } 
  else if (dateRangeString.includes('——')) {
    const startDate = new Date(dates[0])
    if (now < startDate) {
      return 'upcoming'
    } else {
      return 'open'
    }
  } 
  else {
    return 'open'
  }
}


// ================== 论文板块 ==================
const activeTab = ref('Representation')
const displayPapers = ref([])
const tabs = [
  { key: 'Representation', label: '表征学习' },
  { key: 'Fusion', label: '模态融合' },
  { key: 'Alignment', label: '模态对齐' },
  { key: 'Instruction Tuning', label: '指令微调' },
  { key: 'Hallucination', label: '幻觉研究' }
]

const parseDate = (dateStr) => {
  if (!dateStr) return 0
  if (/^\d{4}$/.test(dateStr)) return new Date(dateStr, 0, 1).getTime()
  return new Date(dateStr).getTime()
}

const getPapersByTab = (tabKey) => {
  return papersData.filter(p => p.tags && p.tags.includes(tabKey))
}

const switchTab = (tabKey) => {
  activeTab.value = tabKey
  const allPapers = getPapersByTab(tabKey)
  allPapers.sort((a, b) => parseDate(b.date) - parseDate(a.date))
  displayPapers.value = allPapers.slice(0, 3)
}

const refreshPapers = () => {
  const allPapers = getPapersByTab(activeTab.value)
  const shuffled = shuffleArray([...allPapers])
  displayPapers.value = shuffled.slice(0, 3)
}

// ================== 数据集板块 ==================
const displayDatasets = ref([])

const refreshDatasets = () => {
  const shuffled = shuffleArray([...datasetsData])
  displayDatasets.value = shuffled.slice(0, 3)
}

// ================== 竞赛板块 ==================
const displayCompetitions = ref([])

const refreshCompetitions = () => {
  const activeCompetitions = competitionsData
    .map(item => ({
      ...item,
      _computedStatus: calculateCompetitionStatus(item.date_range)
    }))
    .filter(item => item._computedStatus !== 'ended')

  const shuffled = shuffleArray([...activeCompetitions])
  displayCompetitions.value = shuffled.slice(0, 2)
}

// ================== 征稿板块 ==================
const displayCfps = ref([])

const refreshCfps = () => {
  const activeCfps = cfpData
    .map(item => ({
      ...item,
      _computedStatus: calculateCfpStatus(item.date_range)
    }))
    .filter(item => item._computedStatus === 'open')

  const shuffled = shuffleArray([...activeCfps])
  displayCfps.value = shuffled.slice(0, 2)
}

// ================== 初始化 ==================
onMounted(() => {
  switchTab('Representation')
  refreshDatasets()
  refreshCompetitions()
  refreshCfps()
})
</script>

<style>
.swiper-pagination-bullet {
  background-color: white !important;
  opacity: 0.5 !important;
  width: 8px !important;
  height: 8px !important;
}
.swiper-pagination-bullet-active {
  background-color: #2563EB !important;
  opacity: 1 !important;
  width: 20px !important;
  border-radius: 4px !important;
}
.swiper-button-next, .swiper-button-prev {
  color: white !important;
  transform: scale(0.6);
  font-weight: bold;
}
</style>