#!/usr/bin/env python3
"""
AI News Aggregator - 基于AI跟踪框架的新闻收集器
使用Google News RSS + 智能分类
"""

import feedparser
import json
import re
from datetime import datetime
from html import unescape
from urllib.parse import quote

# AI跟踪框架 - Google News RSS查询
RSS_QUERIES = {
    "breakthrough": "AI breakthrough AGI",
    "openai": "OpenAI",
    "anthropic": "Anthropic Claude",
    "google": "Google DeepMind Gemini",
    "meta": "Meta AI LLaMA",
    "nvidia": "NVIDIA GTC",
    "domestic": "DeepSeek Qwen MiniMax",
    "research": "arxiv ICLR NeurIPS",
    "agent": "AI agent OpenClaw LangChain",
    "technical": "MoE RAG transformer",
}

def fetch_rss(query, max_items=8):
    """获取RSS源"""
    try:
        encoded = quote(query)
        url = f"https://news.google.com/rss/search?q={encoded}&hl=zh-CN&gl=CN"
        feed = feedparser.parse(url)
        items = []
        seen = set()
        for entry in feed.entries[:max_items]:
            link = entry.get("link", "")
            if link and link not in seen:
                seen.add(link)
                item = {
                    "title": unescape(entry.get("title", "").strip()),
                    "link": link,
                    "pubDate": entry.get("published", "")[:16],
                    "source": entry.get("source", {}).get("title", "Google News") if isinstance(entry.get("source"), dict) else entry.get("source", "Google News"),
                    "description": re.sub(r'<[^>]+>', '', entry.get("summary", ""))[:150] if entry.get("summary") else "",
                    "category": query
                }
                items.append(item)
        return items
    except Exception as e:
        print(f"  ⚠️ {query}: {e}")
        return []

def should_exclude(item):
    """内容过滤"""
    title = item.get("title", "").lower()
    text = title
    
    exclude_patterns = ["xx行业要消失", "行业要完", "要失业", "套壳", "promo", "advertisement"]
    emotion_patterns = ["震惊", "炸裂", "颠覆", "彻底改变", "新时代", "革命性"]
    
    for pattern in exclude_patterns:
        if pattern in text:
            return True
    
    if sum(1 for p in emotion_patterns if p in text) >= 1:
        return True
    
    return False

def categorize_news(all_items):
    """分类新闻"""
    categories = {
        "core_breakthrough": [],
        "commercial": [],
        "research": [],
        "people": [],
        "technical": [],
        "agent_openclaw": [],
        "domestic": [],
    }
    
    keywords = {
        "core_breakthrough": ["breakthrough", "reasoning", "agi", "gpt-5", "gpt5", "claude 4", "gemini 3", "superhuman"],
        "commercial": ["launch", "release", "announce", "product", "model", "api", "enterprise", "pricing"],
        "research": ["arxiv", "iclr", "neurips", "icml", "paper", "research", "study", "benchmark"],
        "people": ["sama", "altman", "lecun", "karpathy", "amodei", "hinton", "schulman", "ceo"],
        "technical": ["moe", "mixture", "rag", "transformer", "architecture", "training", "inference"],
        "agent_openclaw": ["agent", "openclaw", "langchain", "autogen", "crewai", "tool", "agentic"],
        "domestic": ["deepseek", "qwen", "minimax", "moonshot", "zhipu", "bytedance", "alibaba", "tencent", "baidu", "智谱", "月之暗面"],
    }
    
    for item in all_items:
        title = item.get("title", "").lower()
        source = item.get("source", "").lower()
        link = item.get("link", "").lower()
        text = title + " " + source + " " + link
        
        if any(kw in text for kw in keywords["core_breakthrough"]):
            categories["core_breakthrough"].append(item)
        elif any(kw in text for kw in keywords["agent_openclaw"]):
            categories["agent_openclaw"].append(item)
        elif any(kw in text for kw in keywords["domestic"]) and "arxiv" not in text:
            categories["domestic"].append(item)
        elif any(kw in text for kw in keywords["people"]):
            categories["people"].append(item)
        elif any(kw in text for kw in keywords["technical"]):
            categories["technical"].append(item)
        elif any(kw in text for kw in keywords["research"]):
            categories["research"].append(item)
        else:
            categories["commercial"].append(item)
    
    return categories

def generate_report(categories):
    """生成Markdown报告"""
    md = f"""# 🤖 AI 每日资讯 {datetime.now().strftime('%Y-%m-%d')}

## 一、核心突破 (High Impact)
_过去24小时最重要的AI进展_

"""
    
    core = categories["core_breakthrough"][:5]
    if core:
        for i, item in enumerate(core, 1):
            md += f"**{i}. {item['title']}**\n"
            md += f"- 来源: {item['source']} | [查看原文]({item['link']})\n\n"
    else:
        md += "_暂无_\n\n"
    
    md += "## 二、分类快讯\n\n"
    
    md += "### [商业产品]\n"
    comm = categories["commercial"][:10]
    for item in comm:
        md += f"- [{item['title']}]({item['link']})\n"
    if not comm:
        md += "- 暂无\n"
    
    md += "\n### [研究学界]\n"
    research = categories["research"][:8]
    for item in research:
        md += f"- [{item['title']}]({item['link']})\n"
    if not research:
        md += "- 暂无\n"
    
    md += "\n### [国内动态]\n"
    domestic = categories["domestic"][:8]
    for item in domestic:
        md += f"- [{item['title']}]({item['link']})\n"
    if not domestic:
        md += "- 暂无\n"
    
    md += "\n### [关键人物]\n"
    people = categories["people"][:5]
    for item in people:
        md += f"- [{item['title']}]({item['link']})\n"
    if not people:
        md += "- 暂无\n"
    
    md += "\n## 三、技术关联\n"
    tech = categories["technical"][:5]
    for item in tech:
        md += f"- [{item['title']}]({item['link']})\n"
    if not tech:
        md += "_暂无_\n"
    
    md += "\n## 四、Agent & OpenClaw 专题\n"
    agent = categories["agent_openclaw"][:10]
    for item in agent:
        md += f"- [{item['title']}]({item['link']})\n"
    if not agent:
        md += "- 暂无\n"
    
    md += f"""
---
*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*基于 AI 跟踪框架 | 信源: Google News RSS*
"""
    return md

def main():
    print("📥 Fetching AI news based on tracking framework...")
    all_items = []
    seen_links = set()
    
    for name, query in RSS_QUERIES.items():
        print(f"  🔍 {name}...")
        items = fetch_rss(query, max_items=8)
        for item in items:
            if item["link"] not in seen_links and not should_exclude(item):
                seen_links.add(item["link"])
                item["category"] = name
                all_items.append(item)
    
    print(f"  📊 Total: {len(all_items)} items")
    
    categories = categorize_news(all_items)
    
    news_data = {
        "status": "ok",
        "last_updated": datetime.now().isoformat(),
        "total_items": len(all_items),
        "items": all_items,
        "categories": {k: len(v) for k, v in categories.items()}
    }
    
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    report = generate_report(categories)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"✅ Complete!")
    print(f"   🔥 核心突破: {len(categories['core_breakthrough'])}")
    print(f"   💼 商业: {len(categories['commercial'])}")
    print(f"   🔬 研究: {len(categories['research'])}")
    print(f"   🇨🇳 国内: {len(categories['domestic'])}")
    print(f"   🤖 Agent/OpenClaw: {len(categories['agent_openclaw'])}")
    print("📝 Generated README.md & news.json")

if __name__ == "__main__":
    main()