<template>
  <header class="bg-white border-b border-gray-100 sticky top-0 z-50">
    <div class="container mx-auto px-4 h-20 flex items-center justify-between">
      
      <NuxtLink to="/" class="flex items-center gap-3 shrink-0">
        <div class="w-10 h-10 bg-primary rounded-lg flex items-center justify-center text-white shadow-sm shadow-primary/20">
          <i class="fa fa-cubes text-lg"></i>
        </div>
        <div class="flex flex-col">
          <span class="font-bold text-xl leading-none text-dark tracking-tight">Multimodal</span>
          <span class="text-xs text-gray-500 uppercase tracking-wider font-medium mt-0.5">Open Community</span>
        </div>
      </NuxtLink>

      <nav class="hidden md:flex items-center gap-8 lg:gap-10 h-full whitespace-nowrap">
        <NuxtLink 
          to="/" 
          exact
          class="nav-item"
          active-class="nav-item-active"
        >
          首页
        </NuxtLink>

        <NuxtLink 
          to="/papers" 
          class="nav-item"
          active-class="nav-item-active"
        >
          精选文献
        </NuxtLink>

        <NuxtLink 
          to="/datasets" 
          class="nav-item"
          active-class="nav-item-active"
        >
          开源数据
        </NuxtLink>

        <NuxtLink 
          to="/competitions" 
          class="nav-item"
          active-class="nav-item-active"
        >
          竞赛挑战
        </NuxtLink>

        <NuxtLink 
          to="/cfp" 
          class="nav-item"
          active-class="nav-item-active"
        >
          征稿专栏
        </NuxtLink>
      </nav>

      <div class="flex items-center gap-4 shrink-0">
        <div class="hidden xl:block">
          <StatTicker />
        </div>
      </div>

    </div>
  </header>
</template>

<style scoped>
.nav-item {
  /* 修改点6：导航字体由 text-sm 增大至 text-base (16px) */
  @apply h-full inline-flex items-center text-base font-medium text-gray-500 
         border-b-2 border-transparent transition-all duration-200 
         hover:text-primary hover:text-opacity-80;
}

.nav-item-active {
  @apply !text-dark !border-primary font-bold;
}
</style>

<script setup>
// Nuxt 3 自动导入 components/ 目录下的组件
</script>