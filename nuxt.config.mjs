// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // 1. 模块配置
  modules: [],

  // 2. 【核心修改】修正 CSS 路径
  // 这里的 ~ 符号代表项目根目录。
  // 因为 assets 文件夹已经移动到了根目录下，所以路径不应该再包含 'app/'
  css: ['~/assets/css/main.css'],

  // 3. PostCSS 配置
  postcss: {
    plugins: {
      tailwindcss: { config: './tailwind.config.json' },
      autoprefixer: {},
    },
  },

  app: {
    head: {
      link: [
        { 
          rel: 'stylesheet', 
          href: 'https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css' 
        }
      ]
    }
  },

  future: {
    compatibilityVersion: 3
  },

  devtools: { enabled: true },
  compatibilityDate: '2024-04-03'
})