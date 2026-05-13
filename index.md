---
layout: default
title: Home
---

<div class="home">
  <header class="hero">
    <h1 class="site-title">🤖 AI News Blog</h1>
    <p class="site-description">每日 AI 新闻与技术解读</p>
  </header>

  <section class="posts-list">
    {% for post in site.posts %}
    <article class="post-card">
      <span class="post-date">{{ post.date | date: "%Y-%m-%d" }}</span>
      <h2 class="post-title">
        <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
      </h2>
      {% if post.description %}
      <p class="post-excerpt">{{ post.description }}</p>
      {% else %}
      <p class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 30 }}</p>
      {% endif %}
      {% if post.tags %}
      <div class="post-tags">
        {% for tag in post.tags limit: 3 %}
        <span class="tag">{{ tag }}</span>
        {% endfor %}
      </div>
      {% endif %}
    </article>
    {% endfor %}

    {% if site.posts.size == 0 %}
    <p class="no-posts">暂无文章，即将更新...</p>
    {% endif %}
  </section>
</div>

<style>
  .hero {
    text-align: center;
    padding: 2rem 0 1rem;
    border-bottom: 1px solid #e1e4e8;
    margin-bottom: 2rem;
  }
  .hero .site-title {
    font-size: 2.5rem;
    margin: 0;
    color: #24292e;
  }
  .site-description {
    color: #586069;
    font-size: 1.1rem;
    margin-top: 0.5rem;
  }
  .posts-list {
    max-width: 800px;
    margin: 0 auto;
  }
  .post-card {
    padding: 1.5rem 0;
    border-bottom: 1px solid #e1e4e8;
  }
  .post-date {
    color: #6a737d;
    font-size: 0.85rem;
  }
  .post-title {
    margin: 0.3rem 0;
  }
  .post-title a {
    color: #0366d6;
    text-decoration: none;
    font-size: 1.3rem;
  }
  .post-title a:hover {
    text-decoration: underline;
  }
  .post-excerpt {
    color: #586069;
    line-height: 1.6;
  }
  .post-tags {
    margin-top: 0.5rem;
  }
  .tag {
    display: inline-block;
    background: #f1f8ff;
    color: #0366d6;
    padding: 0.1rem 0.5rem;
    border-radius: 3px;
    font-size: 0.8rem;
    margin-right: 0.3rem;
  }
  .no-posts {
    text-align: center;
    color: #999;
    padding: 2rem;
  }
</style>
