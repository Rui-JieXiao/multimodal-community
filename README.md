# Multimodal Intelligence Community (多模态智能社区)

这是一个专注于多模态大模型（MLLM）前沿论文收录与展示的开源社区项目。本项目采用 **Nuxt 3 + Vue 3 + TailwindCSS** 构建前端，配合 **Python** 脚本进行数据自动化采集。

## 📂 目录结构与功能说明 (Directory Structure)

为了确保开发规范与资源路径正确，请严格遵守以下文件夹职能划分：

### 1. 核心资源目录 (关键区别)

这是项目中最容易混淆的两个目录，请务必区分使用场景：

#### 🔹 `assets/` (编译期资源)
* **职能**：存放需要经过构建工具 (Vite/Webpack) **编译、压缩、哈希化** 的源代码资源。
* **特性**：这里的资源必须通过 `import` 语句引入，文件名在打包后会改变（如 `style.css` 变成 `style.2f9a.css`）。
* **包含内容**：
    * `assets/css/`：全局样式表 (main.css)。
    * `assets/data/`：**核心数据源** (`papers_data.json`)。前端组件将其视为代码模块导入。
    * `assets/icons/`：UI 组件用到的小图标 (SVG 等)。

#### 🔸 `public/` (运行时静态资源)
* **职能**：存放**不需要编译**、希望被浏览器直接通过 URL 访问的静态文件。
* **特性**：Vite 会将这里的文件**原封不动**地复制到根目录。路径即 URL。
* **包含内容**：
    * `public/paper_images/`：**论文封面图仓库**。
        * 前端引用方式：直接使用字符串路径 `/paper_images/default-cover.jpg`。
        * *注意：不要在这里放代码或敏感数据。*
    * `public/favicon.ico`：网站图标。

---

### 2. 业务代码目录

#### 🐍 `scripts/` (自动化脚本)
* **职能**：存放 Python 爬虫与数据处理脚本。
* **核心文件**：
    * `extract_papers.py`：负责从 `README.md` 抓取论文数据，执行“智能合并”逻辑（保护人工填写的作者/图片信息），并生成/更新 `assets/data/papers_data.json`。

#### 🧩 `components/` (Vue 组件)
* **职能**：存放可复用的 UI 模块。
* **核心文件**：
    * `PaperCard.vue`：论文卡片组件（接收 title, authors, tags, image 等 props）。

#### 📄 `pages/` (页面路由)
* **职能**：存放应用的主页面，Nuxt 会根据这里的文件自动生成路由。
* **核心文件**：
    * `index.vue`：首页。包含筛选器、搜索栏、分页逻辑以及卡片列表的容器。

---

## 🛠️ 数据维护工作流 (Workflow)

本项目采用 **“自动化抓取 + 人工精修”** 的混合维护模式：

1.  **抓取新论文**：
    * 运行 `python scripts/extract_papers.py`。
    * 脚本会自动从 README 提取新论文，标记为 `source: "auto-script"`。
2.  **人工精修 (Manual Polish)**：
    * 打开 `assets/data/papers_data.json`。
    * 找到感兴趣的论文，手动补全 `authors` (作者) 和 `description` (摘要)。
    * **添加图片**：
        1.  将图片放入 `public/paper_images/`。
        2.  在 JSON 中修改 `image` 字段为 `/paper_images/你的文件名.jpg`。
3.  **安全机制**：
    * 再次运行脚本时，脚本会自动检测 Link 指纹，**绝不会覆盖** 你手动填写的作者、摘要和图片路径。

---

## 🚀 待办事项 (TODO) & 未来规划

* [ ] **图片资产完善**：为 Top 10 论文添加真实 Teaser 截图，其余使用高质量默认图。
* [ ] **多分类扩展**：扩展脚本以支持 Visual Generation, Embodied AI 等更多章节的抓取。
* [ ] **详情页开发**：点击卡片进入详情页，展示摘要和 BibTeX。
* [ ] **移动端适配优化**：进一步打磨手机端的筛选栏交互。

---
*Last Updated: 2025*