#!/usr/bin/env python3
"""
Sync AI news from Obsidian vault to blog _posts directory.
Run this script to convert new ainews/*.md files into blog-ready _posts/*.md format.
"""

import os, re, sys
from datetime import datetime

VAULT_NEWS_DIR = os.path.expanduser("~/hermes/obsidian-vault/learn/tech/ai/ainews")
BLOG_DIR = os.path.expanduser("~/ai-news-blog")
POSTS_DIR = os.path.join(BLOG_DIR, "_posts")

def convert_news_to_post(src_path):
    """Convert a single news file to blog post format."""
    fname = os.path.basename(src_path)
    if not fname.endswith('.md') or fname == 'README.md':
        return None
    
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find front matter
    fm_boundaries = [m.end() for m in re.finditer(r'^---$', content, re.MULTILINE)]
    if len(fm_boundaries) < 2:
        return None
    
    fm_text = content[fm_boundaries[0]:fm_boundaries[1]-4]
    body = content[fm_boundaries[1]:].strip()
    
    # Parse date
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', fname)
    if not date_match:
        date_match = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', fm_text)
    if not date_match:
        return None
    date_str = date_match.group(1)
    
    # Parse title
    title_match = re.search(r'title:\s*"([^"]+)"', fm_text)
    if not title_match:
        title_match = re.search(r"title:\s*'([^']+)'", fm_text)
    if not title_match:
        title_match = re.search(r'title:\s*(.+)', fm_text)
    title = title_match.group(1).strip().strip('"').strip("'") if title_match else fname.replace('.md', '').replace('-', ' ').title()
    
    # Parse description
    desc_match = re.search(r'description:\s*"([^"]*)"', fm_text)
    description = desc_match.group(1) if desc_match else ""
    
    # Parse tags
    tags_match = re.search(r'tags:\s*\[(.*?)\]', fm_text)
    tags = tags_match.group(1) if tags_match else "ai-news"
    
    # Build post
    slug = fname.replace('.md', '')
    post_filename = f"{date_str}-{slug}.md"
    
    new_fm = f'---\ntitle: "{title}"\ndate: {date_str}\ndescription: "{description}"\ntags: [{tags}]\n---\n\n'
    new_content = new_fm + body
    
    return post_filename, new_content

def sync_all():
    """Sync all news files to blog posts."""
    os.makedirs(POSTS_DIR, exist_ok=True)
    
    existing_posts = set(os.listdir(POSTS_DIR)) if os.path.exists(POSTS_DIR) else set()
    converted = 0
    skipped = 0
    
    for fname in sorted(os.listdir(VAULT_NEWS_DIR)):
        if not fname.endswith('.md') or fname == 'README.md':
            continue
        
        src_path = os.path.join(VAULT_NEWS_DIR, fname)
        result = convert_news_to_post(src_path)
        if result is None:
            skipped += 1
            continue
        
        post_filename, new_content = result
        post_path = os.path.join(POSTS_DIR, post_filename)
        
        # Only write if file doesn't exist or content changed
        if post_filename not in existing_posts:
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            converted += 1
            print(f"  + {post_filename}")
    
    return converted, skipped

if __name__ == "__main__":
    if not os.path.exists(VAULT_NEWS_DIR):
        print(f"Error: Vault news directory not found: {VAULT_NEWS_DIR}")
        sys.exit(1)
    
    print("Syncing AI news to blog...")
    converted, skipped = sync_all()
    print(f"\nDone: {converted} new posts, {skipped} skipped")
