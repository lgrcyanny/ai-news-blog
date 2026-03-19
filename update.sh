#!/bin/bash
# AI News Blog - Auto Update Script
# 运行: ./update.sh

BLOG_DIR="/Users/cyanny/.openclaw/workspace/ai-news-blog"
RSS_URL="https://news.google.com/rss/search?q=AI%20artificial%20intelligence%202026&hl=zh-CN&gl=CN"
OUTPUT_FILE="$BLOG_DIR/news.json"

echo "📥 Fetching AI news from Google News RSS..."

# Fetch and parse RSS to JSON
curl -s "https://api.rss2json.com/v1/api.json?rss_url=$(echo $RSS_URL | sed 's/ /%20/g')" > "$OUTPUT_FILE"

if [ -s "$OUTPUT_FILE" ]; then
    echo "✅ News fetched successfully!"
    echo "📝 Items: $(cat $OUTPUT_FILE | grep -o '"title"' | wc -l)"
else
    echo "❌ Failed to fetch news"
    exit 1
fi

# Git operations (if in a git repo)
if [ -d "$BLOG_DIR/.git" ]; then
    cd "$BLOG_DIR"
    git add -A
    git commit -m "Update: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || true
    echo "🔄 Git commit updated"
fi

echo "✨ Done!"