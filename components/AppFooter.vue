<template>
  <footer class="bg-dark text-white pt-12 pb-8">
    <div class="container mx-auto px-4">
      
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
        
        <div class="col-span-1 md:col-span-2">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white">
              <i class="fa fa-cubes"></i>
            </div>
            <span class="font-bold text-lg">Multimodal Open Community</span>
          </div>
          <p class="text-gray-400 text-sm leading-relaxed max-w-sm">
            连接视觉与语言，构建多模态智能社区。
            <br>
            在这里发现最新的多模态前沿工作。
          </p>
        </div>

        <div>
          <h3 class="font-bold mb-4 text-lg">快速导航</h3>
          <ul class="space-y-2 text-sm text-gray-400">
            <li><NuxtLink to="/" class="hover:text-white transition-colors">首页 Home</NuxtLink></li>
            <li><NuxtLink to="/papers" class="hover:text-white transition-colors">前沿论文 Papers</NuxtLink></li>
            <li><NuxtLink to="/datasets" class="hover:text-white transition-colors">数据集 Datasets</NuxtLink></li>
            <li><NuxtLink to="/competitions" class="hover:text-white transition-colors">技术竞赛 Competitions</NuxtLink></li>
            <li><NuxtLink to="/cfp" class="hover:text-white transition-colors">征稿专栏 Call for Papers</NuxtLink></li>
          </ul>
        </div>

        <div>
          <h3 class="font-bold mb-4 text-lg">联系我们</h3>
          <div class="flex flex-col gap-4">
            
            <div class="flex items-center gap-3 group">
              <div class="w-9 h-9 rounded-full bg-white/10 flex items-center justify-center text-gray-300 group-hover:bg-primary group-hover:text-white transition-all duration-300 shrink-0">
                <i class="fa fa-phone text-sm"></i>
              </div>
              <span class="text-gray-400 text-sm font-mono group-hover:text-white transition-colors">158-9221-2703</span>
            </div>

            <div class="flex items-center gap-3 group">
              <div class="w-9 h-9 rounded-full bg-white/10 flex items-center justify-center text-gray-300 group-hover:bg-primary group-hover:text-white transition-all duration-300 shrink-0">
                <i class="fa fa-envelope text-sm"></i>
              </div>
              <a href="mailto:xiaoruijie2001@163.com" class="text-gray-400 text-sm font-mono group-hover:text-white transition-colors">
                xiaoruijie2001@163.com
              </a>
            </div>

          </div>
        </div>

      </div>

      <div class="border-t border-gray-700 my-8"></div>

      <div class="flex flex-col md:flex-row justify-between items-center text-xs text-gray-500">
        <p>&copy; 2026 Multimodal Open Community. All rights reserved.</p>
        <p class="mt-2 md:mt-0">Designed for AI Researchers</p>
      </div>

    </div>
  </footer>
</template>

<script setup>
// 同样，页脚目前是纯静态展示，不需要脚本
</script>