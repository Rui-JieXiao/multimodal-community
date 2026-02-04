<template>
  <div class="stat-ticker-main h-20 w-[550px] relative overflow-hidden mask-v">
    <client-only>
      <swiper
        v-if="allUpcomingStages.length > 0"
        :modules="[Autoplay, Mousewheel]"
        direction="vertical"
        :slides-per-view="1"
        :loop="true"
        :mousewheel="true"
        :speed="600"
        :autoplay="{ delay: 5000, disableOnInteraction: false }"
        class="h-full w-full"
      >
        <swiper-slide v-for="(item, index) in allUpcomingStages" :key="index" class="!flex items-center">
          <div class="flex items-center justify-between w-full h-full px-4 pt-1">
            
            <div class="flex items-baseline shrink-0">
              <span class="text-[#8c90ad] text-[15px] font-medium mr-3">距离</span>
              <div class="flex items-baseline gap-1">
                <span class="text-[#5a3da0] font-black text-[19px] tracking-tighter">{{ item.title }}</span>
                <span class="text-[#5a3da0] font-bold text-[13px] uppercase tracking-tight">'{{ item.year % 100 }}</span>
                <span class="text-[#8c90ad] mx-1.5">-</span>
                <span class="text-[#5a3da0] font-bold text-[17px] tracking-wide">{{ item.stageLabel }}</span>
              </div>
            </div>

            <div class="flex items-center gap-2.5">
              <div v-for="(val, unit) in item.countdown" :key="unit" class="flex items-end gap-1.5 relative">
                <div class="flex flex-col items-center">
                  <div class="glass-cube w-[44px] h-[44px] flex items-center justify-center rounded-[6px] relative z-10">
                    <span class="text-[26px] font-black text-[#2b2052] font-mono leading-none pt-1">{{ val }}</span>
                  </div>
                  <div class="glass-cube w-[44px] h-[44px] flex items-center justify-center rounded-[6px] absolute top-[45px] opacity-15 reflection-transform pointer-events-none">
                    <span class="text-[26px] font-black text-[#2b2052] font-mono leading-none pt-1">{{ val }}</span>
                  </div>
                </div>
                <div class="flex flex-col items-center relative h-[44px]">
                  <div class="flex items-center justify-center h-full">
                    <span v-if="unit === 'd'" class="text-[#5a3da0] text-[14px] font-bold mx-1 mb-1">天</span>
                    <span v-else-if="unit !== 's'" class="text-[#dedbf5] font-black text-[26px] -mt-1 mx-0.5">:</span>
                  </div>
                  <div class="flex items-center justify-center h-full absolute top-[45px] opacity-10 reflection-transform">
                    <span v-if="unit === 'd'" class="text-[#5a3da0] text-[14px] font-bold mx-1 mb-1">天</span>
                    <span v-else-if="unit !== 's'" class="text-[#dedbf5] font-black text-[26px] -mt-1 mx-0.5">:</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </swiper-slide>
      </swiper>
      <div v-else class="h-full flex items-center justify-center text-gray-300 text-sm">
        加载学术日历中...
      </div>
    </client-only>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Autoplay, Mousewheel } from 'swiper/modules'
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import rawDeadlines from '@/assets/data/top_deadlines.json'

const nowTs = ref(Date.now())
let timer = null

const LABEL_MAP = {
  'abstract': '摘要提交',
  'paper': '正文截稿',
  'submission': '正文截稿',
  'notification': '论文开奖 🎰',       // 增加幽默感
  'final_decision_date': '论文开奖 🎰', // 增加幽默感
  '录用通知': '论文开奖 🎰',            // 兼容中文 Key
  'review_release': '评审发布',
  'rebuttal_start': '反驳开始',
  'rebuttal_end': '反驳截止',
  'supplementary': '补充材料',
  'camera_ready': '终稿提交'
}

const allUpcomingStages = computed(() => {
  const result = []
  const currentTs = nowTs.value

  rawDeadlines.forEach(conf => {
    const rawEvents = []
    
    // 扫描顶层字段
    if (conf.abstract_deadline) rawEvents.push({ type: 'abstract', date: conf.abstract_deadline, tz: conf.timezone })
    if (conf.deadline) rawEvents.push({ type: 'submission', date: conf.deadline, tz: conf.timezone })
    if (conf.final_decision_date) rawEvents.push({ type: 'notification', date: conf.final_decision_date, tz: conf.timezone })

    // 扫描数组字段
    if (conf.deadlines && Array.isArray(conf.deadlines)) {
      conf.deadlines.forEach(d => {
        // 修改：兼容新 JSON 的 label 和 time 字段
        rawEvents.push({ 
          type: d.type || d.label, 
          date: d.date || d.time, 
          tz: d.timezone || conf.timezone 
        })
      })
    }

    const processedEvents = new Map()
    rawEvents.forEach(evt => {
      if (!evt.date) return
      
      const tz = evt.tz || 'AoE'
      let offset = 0
      if (tz === 'AoE' || tz.includes('UTC-12')) offset = -12
      else if (tz.includes('UTC-8')) offset = -8

      const targetTs = new Date(evt.date.replace(/-/g, '/')).getTime() - (offset * 3600 * 1000)

      if (targetTs > currentTs) {
        const label = LABEL_MAP[evt.type] || evt.type || '关键节点'
        const uniqueKey = `${label}-${targetTs}`
        if (!processedEvents.has(uniqueKey)) {
          processedEvents.set(uniqueKey, {
            title: conf.title,
            year: conf.year,
            stageLabel: label,
            ts: targetTs
          })
        }
      }
    })

    processedEvents.forEach(evt => {
      const diff = evt.ts - currentTs
      result.push({
        ...evt,
        countdown: {
          d: String(Math.floor(diff / 86400000)).padStart(2, '0'),
          h: String(Math.floor((diff / 3600000) % 24)).padStart(2, '0'),
          m: String(Math.floor((diff / 60000) % 60)).padStart(2, '0'),
          s: String(Math.floor((diff / 1000) % 60)).padStart(2, '0')
        }
      })
    })
  })

  return result.sort((a, b) => a.ts - b.ts)
})

onMounted(() => {
  timer = setInterval(() => { nowTs.value = Date.now() }, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
/* 样式保持原样 */
.glass-cube {
  background: linear-gradient(180deg, #FFFFFF 0%, #f7f5ff 100%);
  border: 1px solid #e9e4ff;
  box-shadow: 0 2px 8px rgba(90, 61, 160, 0.04);
}
.reflection-transform {
  transform: scaleY(-1);
  mask-image: linear-gradient(to top, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 80%);
  -webkit-mask-image: linear-gradient(to top, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 80%);
}
.mask-v {
  mask-image: linear-gradient(to bottom, transparent 0%, black 15%, black 85%, transparent 100%);
  -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 15%, black 85%, transparent 100%);
}
.font-mono {
  font-family: 'JetBrains Mono', 'DIN Alternate', monospace;
}
</style>