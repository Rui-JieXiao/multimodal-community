<template>
  <div class="flex flex-col min-h-screen bg-light font-inter text-dark">
    
    <GlobalLoading />

    <AppHeader />

    <main class="flex-1">
      <slot />
    </main>

    <AppFooter />
    
  </div>
</template>

<script setup>
/**
 * 这里的逻辑已由 GlobalLoading 内部通过 useRouter 钩子自动处理。
 * 无需在此处添加额外的控制逻辑。
 */
</script>