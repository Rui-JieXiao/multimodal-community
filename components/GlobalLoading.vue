<template>
  <transition name="fade">
    <div v-if="isLoading" class="fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-slate-900">
      
      <div class="relative w-40 h-40">
        <div class="absolute inset-0 border-2 border-transparent border-t-blue-500 border-b-blue-500 rounded-full animate-spin-slow"></div>
        
        <div class="absolute inset-4 border-2 border-transparent border-l-purple-500 border-r-purple-500 rounded-full animate-spin-reverse"></div>
        
        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <div class="text-2xl font-black text-white tracking-tighter">
            {{ progress }}<span class="text-xs ml-0.5 text-blue-400">%</span>
          </div>
          <div class="text-[8px] text-slate-500 uppercase tracking-[0.2em] mt-1 font-bold">Initializing</div>
        </div>

        <div class="absolute top-0 left-1/2 -translate-x-1/2 w-1.5 h-1.5 bg-blue-400 rounded-full shadow-[0_0_12px_rgba(59,130,246,0.8)]"></div>
      </div>

      <div class="mt-10 flex flex-col items-center">
        <div class="text-[10px] text-blue-500/50 font-mono tracking-[0.3em] uppercase animate-pulse">
          Quantum Computing System
        </div>
        <div class="w-48 h-[1px] bg-slate-800 mt-4 relative overflow-hidden">
          <div 
            class="absolute inset-y-0 left-0 bg-gradient-to-r from-transparent via-blue-500 to-transparent transition-all duration-300"
            :style="{ width: progress + '%' }"
          ></div>
        </div>
      </div>

    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const isLoading = ref(false)
const progress = ref(0)
const router = useRouter()

const startLoading = () => {
  isLoading.value = true
  progress.value = 0
  
  // 1. 频率缩短至 40ms：大幅提升更新频率，让跳动更有紧迫感
  const timer = setInterval(() => {
    // 2. 步长增加到 15-25：单次跳跃幅度更大，减少中间停留的帧数
    const step = Math.floor(Math.random() * 6) + 10 
    
    // 3. 取消“最后阶段减速”，只要没到 100 就继续大步快走
    if (progress.value + step < 100) {
      progress.value += step
    } else {
      // 4. 一旦溢出直接满格
      progress.value = 100
      clearInterval(timer)
      
      // 5. 保持你觉得舒服的 50ms 极速消失
      setTimeout(() => {
        isLoading.value = false
      }, 100)
    }
  }, 100) // 这里的 40ms 配合上面的大步长，会让转场非常凌厉
}

onMounted(() => {
  startLoading()

  router.beforeEach((to, from, next) => {
    if (to.path !== from.path) {
      startLoading()
    }
    next()
  })
})
</script>

<style scoped>
/* 动画定义 */
.animate-spin-slow {
  animation: spin 3s linear infinite;
}

.animate-spin-reverse {
  animation: spin-reverse 1.5s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes spin-reverse {
  from { transform: rotate(360deg); }
  to { transform: rotate(0deg); }
}

/* 进场和退场淡化效果 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>