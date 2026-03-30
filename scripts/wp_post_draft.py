#!/usr/bin/env python3
"""
wp_post_draft.py — Post a markdown blog file to levinelegal.ca as a WordPress draft.

Usage:
    python3 scripts/wp_post_draft.py <path_to_blog_post.md>

Reads WordPress credentials from .env (WORDPRESS_BASE_URL, WORDPRESS_USERNAME,
WORDPRESS_APP_PASSWORD). Posts the content as a draft pending ML1 review in WP admin.

The script reads the frontmatter to extract title and tags. Body is converted from
markdown to HTML using the markdown library (install: pip install markdown).
"""

import argparse
import base64
import json
import os
import re
import sys
import urllib.request
import urllib.error

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False


def load_env(env_path=".env"):
    """Load key=value pairs from .env file into os.environ."""
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def parse_frontmatter(content):
    """Extract YAML frontmatter and body from a markdown file."""
    frontmatter = {}
    body = content

    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            fm_block = content[3:end].strip()
            body = content[end + 4:].strip()
            for line in fm_block.splitlines():
                if ":" in line:
                    key, _, value = line.partition(":")
                    frontmatter[key.strip()] = value.strip().strip('"')

    return frontmatter, body


def extract_tags(frontmatter):
    """Parse tags list from frontmatter string like '[funnel-03, blog, msb]'."""
    raw = frontmatter.get("tags", "")
    raw = raw.strip("[]")
    return [t.strip() for t in raw.split(",") if t.strip()]


def md_to_html(text):
    """Convert markdown to HTML."""
    if HAS_MARKDOWN:
        return markdown.markdown(text, extensions=["extra", "nl2br"])
    # Fallback: wrap in pre if markdown not available
    return "<pre>" + text + "</pre>"


def post_draft(file_path):
    load_env()

    base_url = os.environ.get("WORDPRESS_BASE_URL", "").rstrip("/")
    username = os.environ.get("WORDPRESS_USERNAME", "")
    app_password = os.environ.get("WORDPRESS_APP_PASSWORD", "")

    if not base_url or not username or not app_password:
        print("ERROR: Missing WordPress credentials in .env", file=sys.stderr)
        sys.exit(1)

    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)
    title = frontmatter.get("title", os.path.basename(file_path))
    tags_raw = extract_tags(frontmatter)

    html_body = md_to_html(body)

    # Build post payload — status=draft
    payload = {
        "title": title,
        "content": html_body,
        "status": "draft",
        "meta": {
            "source_file": file_path,
            "entry_offer": frontmatter.get("entry_offer", ""),
            "content_type": frontmatter.get("content_type", ""),
        },
    }

    # Tag resolution: look up or create each tag by slug
    credentials = base64.b64encode(f"{username}:{app_password}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; SB_Bot/1.0; +https://levinelegal.ca)",
        "Accept": "application/json",
    }

    tag_ids = []
    for tag_name in tags_raw:
        slug = tag_name.lower().replace(" ", "-")
        tag_id = get_or_create_tag(base_url, headers, tag_name, slug)
        if tag_id:
            tag_ids.append(tag_id)

    if tag_ids:
        payload["tags"] = tag_ids

    # POST to WordPress REST API
    api_url = f"{base_url}/wp-json/wp/v2/posts"
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(api_url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            post_id = result.get("id")
            post_link = result.get("link")
            edit_link = f"{base_url}/wp-admin/post.php?post={post_id}&action=edit"
            print(f"Draft created successfully.")
            print(f"  Post ID : {post_id}")
            print(f"  Preview : {post_link}")
            print(f"  Edit    : {edit_link}")
    except urllib.error.HTTPError as e:
        body_err = e.read().decode()
        print(f"ERROR {e.code}: {e.reason}", file=sys.stderr)
        print(body_err, file=sys.stderr)
        sys.exit(1)


def get_or_create_tag(base_url, headers, name, slug):
    """Return tag ID, creating it if it doesn't exist."""
    search_url = f"{base_url}/wp-json/wp/v2/tags?slug={slug}"
    req = urllib.request.Request(search_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            tags = json.loads(resp.read().decode())
            if tags:
                return tags[0]["id"]
    except Exception:
        pass

    # Create tag
    data = json.dumps({"name": name, "slug": slug}).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/wp-json/wp/v2/tags",
        data=data,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            tag = json.loads(resp.read().decode())
            return tag.get("id")
    except Exception:
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post a markdown blog file to levinelegal.ca as a draft.")
    parser.add_argument("file", help="Path to the markdown blog post file")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"ERROR: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    post_draft(args.file)
