#!/usr/bin/env python3
"""
AI News Aggregator - 基于AI跟踪框架的新闻收集器
按框架要求分类：核心突破、分类快讯、技术关联、Agent & OpenClaw专题
"""

import feedparser
import json
import re
from datetime import datetime
from collections import defaultdict

# AI跟踪框架 - 新闻源配置
RSS_SOURCES = {
    "AI综合": [
        "https://news.google.com/rss/search?q=AI+artificial+intelligence&hl=zh-CN",
        "https://news.google.com/rss/search?q=AI+LLM+GPT&hl=en",
    ],
    "学界研究": [
        "https://huggingface.co/papers/trending",
    ],
    "商业动态": [
        "https://news.google.com/rss/search?q=OpenAI&hl=en",
        "https://news.google.com/rss/search?q=Anthropic+Claude&hl=en",
        "https://news.google.com/rss/search?q=NVIDIA+GTC&hl=en",
    ],
    "Agent": [
        "https://news.google.com/rss/search?q=AI+agent+framework&hl=en",
        "https://news.google.com/rss/search?q=OpenClaw&hl=en",
    ]
}

def parse_date(date_str):
    """解析各种日期格式"""
    if not date_str:
        return None
    try:
        return feedparser.parse(date_str).get('updated_parsed') or feedparser.parse(date_str).get('published_parsed')
    except:
        return None

def categorize_news(items):
    """按AI跟踪框架分类新闻"""
    categories = {
        "core_breakthrough": [],      # 核心突破
        "commercial": [],            # 商业产品
        "research": [],              # 研究学界
        "people": [],                # 关键人物
        "technical": [],             # 技术关联
        "agent_openclaw": [],        # Agent & OpenClaw
    }
    
    # 关键词匹配规则
    keywords = {
        "core_breakthrough": ["scaling law", "breakthrough", "breakthrough", "reasoning", "AGI", "superhuman", "GPT-5", "GPT5", "Claude 4", "Gemini 3"],
        "commercial": ["launch", "release", "announce", "product", "model", "api", "pricing", "enterprise"],
        "research": ["paper", "arxiv", "ICLR", "NeurIPS", "ICML", "ACL", "research", "study"],
        "people": ["CEO", "founder", "researcher", "sama", "altman", "lecun", "karpathy", "amodei", "hinton"],
        "technical": ["MoE", "mixture", "RAG", "transformer", "architecture", "benchmark", "training"],
        "agent_openclaw": ["agent", "openclaw", "langchain", "autogen", "crewai", "tool use"],
    }
    
    for item in items:
        title = item.get("title", "").lower()
        description = item.get("description", "").lower()
        text = title + " " + description
        
        # 分类
        if any(kw in text for kw in keywords["core_breakthrough"]):
            categories["core_breakthrough"].append(item)
        elif any(kw in text for kw in keywords["agent_openclaw"]):
            categories["agent_openclaw"].append(item)
        elif any(kw in text for kw in keywords["people"]):
            categories["people"].append(item)
        elif any(kw in text for kw in keywords["technical"]):
            categories["technical"].append(item)
        elif any(kw in text for kw in keywords["research"]):
            categories["research"].append(item)
        elif any(kw in text for kw in keywords["commercial"]):
            categories["commercial"].append(item)
    
    return categories

def should_exclude(item):
    """内容过滤：排除低质量内容"""
    title = item.get("title", "").lower()
    description = item.get("description", "").lower()
    text = title + " " + description
    
    # 排除规则
    exclude_patterns = [
        "xx行业要消失", "行业要完蛋", "要失业了", "即将消亡",
        "套壳", "wrapper", "launches yet another",
        "promo", "advertisement", "sponsored",
    ]
    
    # 包含营销推广情绪的内容
    emotion_patterns = [
        "震惊", "炸裂", "颠覆", "彻底改变", "新时代", "革命性",
    ]
    
    for pattern in exclude_patterns:
        if pattern in text:
            return True
    
    # 过度情绪化的标题
    emotion_count = sum(1 for p in emotion_patterns if p in text)
    if emotion_count >= 2:
        return True
    
    return False

def fetch_all_news():
    """获取所有新闻源"""
    all_items = []
    seen_links = set()
    
    for category, urls in RSS_SOURCES.items():
        for url in urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:10]:  # 每个源取前10条
                    link = entry.get("link", "")
                    if link and link not in seen_links:
                        seen_links.add(link)
                        
                        item = {
                            "title": entry.get("title", "").strip(),
                            "link": link,
                            "pubDate": entry.get("published", ""),
                            "source": entry.get("source", {}).get("title", category) if isinstance(entry.get("source"), dict) else entry.get("source", category),
                            "description": re.sub(r'<[^>]+>', '', entry.get("summary", ""))[:200],
                            "category": category
                        }
                        
                        # 过滤低质量内容
                        if not should_exclude(item):
                            all_items.append(item)
            except Exception as e:
                print(f"Error fetching {url}: {e}")
    
    return all_items

def generate_markdown_report(news_data):
    """生成Markdown格式的报告"""
    categories = categorize_news(news_data["items"])
    
    md = f"""# 🤖 AI 每日资讯 {datetime.now().strftime('%Y-%m-%d')}

## 一、核心突破 (High Impact)

"""
    
    # 核心突破 - 取最重要的3-5条
    core = categories["core_breakthrough"][:5]
    if core:
        for i, item in enumerate(core, 1):
            md += f"**{i}. {item['title']}**\n"
            md += f"- 来源: {item['source']} | [查看原文]({item['link']})\n"
            if item.get("description"):
                md += f"- {item['description'][:100]}...\n"
            md += "\n"
    else:
        md += "暂无核心突破资讯\n\n"
    
    md += """## 二、分类快讯

### [商业产品]
"""
    comm = categories["commercial"][:8]
    for item in comm:
        md += f"- [{item['title']}]({item['link']}) - {item['source']}\n"
    if not comm:
        md += "- 暂无\n"
    
    md += "\n### [研究学界]\n"
    research = categories["research"][:8]
    for item in research:
        md += f"- [{item['title']}]({item['link']}) - {item['source']}\n"
    if not research:
        md += "- 暂无\n"
    
    md += "\n### [关键人物]\n"
    people = categories["people"][:5]
    for item in people:
        md += f"- [{item['title']}]({item['link']}) - {item['source']}\n"
    if not people:
        md += "- 暂无\n"
    
    md += "\n## 三、技术关联\n"
    tech = categories["technical"][:5]
    for item in tech:
        md += f"- [{item['title']}]({item['link']})\n"
    if not tech:
        md += "- 暂无技术更新\n"
    
    md += "\n## 四、Agent & OpenClaw 专题\n"
    agent = categories["agent_openclaw"][:8]
    for item in agent:
        md += f"- [{item['title']}]({item['link']}) - {item['source']}\n"
    if not agent:
        md += "- 暂无\n"
    
    md += f"""
---
*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*基于 AI 跟踪框架 | 信源: Google News RSS*
"""
    
    return md

def main():
    print("📥 Fetching AI news...")
    news_items = fetch_all_news()
    
    news_data = {
        "status": "ok",
        "last_updated": datetime.now().isoformat(),
        "total_items": len(news_items),
        "items": news_items
    }
    
    # 保存JSON
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    # 生成Markdown报告
    md_report = generate_markdown_report(news_data)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(md_report)
    
    print(f"✅ Updated {len(news_items)} news items")
    print("📝 Generated README.md")

if __name__ == "__main__":
    main()