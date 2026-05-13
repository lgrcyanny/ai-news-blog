# 🤖 AI News Blog

每日 AI 新闻与技术解读，自动从 Obsidian 知识库同步。

👉 **访问博客**: https://lgrcyanny.github.io/ai-news-blog

## 📡 内容方向

- **每日 AI 新闻**：聚合当天 AI 领域的重要新闻与进展
- **论文深度解读**：精选 arXiv 热门论文，拆解核心方法与实验结果
- **技术趋势分析**：跟踪 AI 技术发展脉络

## 🛠 技术栈

- 博客基于 [Jekyll](https://jekyllrb.com/) + [GitHub Pages](https://pages.github.com/)
- 内容由 Hermes Agent 自动生成，自动同步到 Obsidian 知识库
- 使用 `minima` 主题，轻量高效

## 🔄 自动同步流程

```
Hermes Agent 生成新闻 → Obsidian vault (ainews/) → sync_news.py → _posts/ → git push → GitHub Pages
```

## 📁 项目结构

```
├── _config.yml              # Jekyll 配置
├── _posts/                  # 博客文章
├── scripts/
│   └── sync_news.py         # 新闻同步脚本
├── index.md                 # 首页
├── about.md                 # 关于页面
└── .github/workflows/
    └── deploy.yml           # GitHub Pages 自动部署
```

## 🚀 部署

推送 main 分支即触发自动部署：

```bash
git push origin main
```

博客地址：https://lgrcyanny.github.io/ai-news-blog
