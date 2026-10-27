#!/usr/bin/env python3
"""
English Teaching - Static Site Builder
Builds ready-to-deploy static bundles for:
1. GitHub Pages (both /docs folder mode and GitHub Actions mode)
2. Vercel / Cloudflare Pages / Netlify

Usage:
    python3 build_site.py
"""

import os
import shutil
import json
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
DIST_DIR = os.path.join(BASE_DIR, "dist")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

def get_documents_metadata():
    categories = []

    # 1. Guides
    guides = []
    guides_dir = os.path.join(BASE_DIR, "guides")
    if os.path.isdir(guides_dir):
        for fname in sorted(os.listdir(guides_dir)):
            if fname.endswith(".md"):
                title = "英语句子学习核心指南" if "sentence" in fname else ("80/20 学习路线图" if "roadmap" in fname else fname)
                guides.append({
                    "title": title,
                    "filename": fname,
                    "path": f"guides/{fname}"
                })
    if guides:
        categories.append({
            "category": "📘 核心方法论与指南",
            "items": guides
        })

    # 2. Cases
    cases = []
    cases_dir = os.path.join(BASE_DIR, "cases")
    if os.path.isdir(cases_dir):
        for fname in sorted(os.listdir(cases_dir)):
            if fname.endswith(".md"):
                title = "口语高频黄金真句 10 案" if "classic" in fname else fname
                cases.append({
                    "title": title,
                    "filename": fname,
                    "path": f"cases/{fname}"
                })
    if cases:
        categories.append({
            "category": "🧪 真实黄金句库",
            "items": cases
        })

    # 3. Lessons
    lessons = []
    lessons_dir = os.path.join(BASE_DIR, "lessons")
    if os.path.isdir(lessons_dir):
        for fname in sorted(os.listdir(lessons_dir)):
            if fname.endswith(".md"):
                title = f"Lesson {fname.replace('lesson_', '').replace('.md', '')} · 撇清八卦与普通同事" if "01" in fname else fname
                lessons.append({
                    "title": title,
                    "filename": fname,
                    "path": f"lessons/{fname}"
                })
    if lessons:
        categories.append({
            "category": "☕️ 《老友记》精萃微课",
            "items": lessons
        })

    # 4. Overview
    if os.path.isfile(os.path.join(BASE_DIR, "README.md")):
        categories.append({
            "category": "🧭 导航与总览",
            "items": [{
                "title": "项目总览与索引 (README)",
                "filename": "README.md",
                "path": "README.md"
            }]
        })

    return categories

def build_target(target_dir):
    print(f"📦 正在打包静态站点到: {target_dir}")
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir, exist_ok=True)

    # 1. Copy web assets (HTML, CSS, JS, libs)
    for item in ["index.html", "style.css", "app.js", "lib"]:
        src = os.path.join(WEB_DIR, item)
        dst = os.path.join(target_dir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        elif os.path.isfile(src):
            shutil.copy2(src, dst)

    # 2. Copy markdown content directories
    for content_dir in ["guides", "cases", "lessons"]:
        src = os.path.join(BASE_DIR, content_dir)
        dst = os.path.join(target_dir, content_dir)
        if os.path.isdir(src):
            shutil.copytree(src, dst)

    # 3. Copy README.md
    readme_src = os.path.join(BASE_DIR, "README.md")
    if os.path.isfile(readme_src):
        shutil.copy2(readme_src, os.path.join(target_dir, "README.md"))

    # 4. Generate data/documents.json & data/version.json
    data_dir = os.path.join(target_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    docs_meta = get_documents_metadata()
    with open(os.path.join(data_dir, "documents.json"), "w", encoding="utf-8") as f:
        json.dump(docs_meta, f, ensure_ascii=False, indent=2)

    version_info = {
        "build_time": int(time.time()),
        "build_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "version": "1.0.0"
    }
    with open(os.path.join(data_dir, "version.json"), "w", encoding="utf-8") as f:
        json.dump(version_info, f, indent=2)

    # 5. Add .nojekyll for GitHub Pages (ensures directories like _ or special files aren't ignored)
    with open(os.path.join(target_dir, ".nojekyll"), "w") as f:
        pass

    print(f"✅ 成功构建完成！包含 {sum(len(c['items']) for c in docs_meta)} 篇讲义与文档。")

def main():
    # Build both dist/ (for Vercel/Cloudflare) and docs/ (for GitHub Pages /docs branch mode)
    build_target(DIST_DIR)
    build_target(DOCS_DIR)
    print("\n🎉 全部打包完成！随时可推送到 GitHub 或发布至 Vercel。")

if __name__ == "__main__":
    main()
