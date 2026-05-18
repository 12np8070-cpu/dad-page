#!/usr/bin/env python3
"""Build index.html from content/article.md for GitHub Pages."""

from __future__ import annotations

import re
from pathlib import Path

import markdown
from markdown.extensions import fenced_code, tables

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content" / "article.md"
OUT = ROOT / "index.html"
CSS = "assets/css/main.css"


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"[^\w\u4e00-\u9fff\-]+", "", text, flags=re.UNICODE)
    return text or "section"


def add_heading_ids(html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        level, inner = m.group(1), m.group(2)
        sid = slugify(inner)
        return f'<h{level} id="{sid}">{inner}</h{level}>'

    return re.sub(r"<h([1-4])>(.+?)</h\1>", repl, html, flags=re.DOTALL)


def enhance_html(html: str) -> str:
    # Disclaimer blockquotes at the top
    count = 0

    def quote_repl(m: re.Match[str]) -> str:
        nonlocal count
        count += 1
        cls = "callout callout--disclaimer" if count <= 2 else "callout"
        return f'<blockquote class="{cls}">{m.group(1)}</blockquote>'

    html = re.sub(r"<blockquote>\s*(.*?)\s*</blockquote>", quote_repl, html, flags=re.DOTALL)

    # Key-point paragraphs: only bold text
    html = re.sub(
        r"<p><strong>(.+?)</strong></p>",
        r'<p class="key-point"><strong>\1</strong></p>',
        html,
        flags=re.DOTALL,
    )

    # Bold label + rest in same paragraph
    html = re.sub(
        r"<p><strong>([^<]+：)</strong>\s*",
        r'<p class="labeled"><span class="label">\1</span> ',
        html,
    )

    # Horizontal rules
    html = re.sub(r"<hr\s*/?>", '<hr class="section-rule" />', html)

    # Highlight the 10-point overview list in section 1
    html = re.sub(
        r'(<h2 id="一整體情況概述">.*?</h2>.*?<p>這位父親的互動方式有幾個明顯特徵：</p>\s*)<ol>',
        r'\1<ol class="overview-list">',
        html,
        count=1,
        flags=re.DOTALL,
    )

    return html


def build_toc(html: str) -> str:
    items: list[str] = []
    for m in re.finditer(r'<h2 id="([^"]+)">(.+?)</h2>', html):
        hid, title = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        items.append(f'    <li><a href="#{hid}">{title}</a></li>')
    if not items:
        return ""
    return (
        '<nav class="toc" aria-label="章節目錄">\n'
        '  <p class="toc__title">目錄</p>\n'
        "  <ol>\n"
        + "\n".join(items)
        + "\n  </ol>\n"
        "</nav>"
    )


def main() -> None:
    md_text = CONTENT.read_text(encoding="utf-8")
    body = markdown.markdown(
        md_text,
        extensions=[
            "extra",
            "smarty",
            fenced_code.FencedCodeExtension(),
            tables.TableExtension(),
        ],
        output_format="html5",
    )
    body = add_heading_ids(body)
    body = enhance_html(body)
    toc_html = build_toc(body)

    title_match = re.search(r"<h1[^>]*>(.+?)</h1>", body)
    page_title = (
        re.sub(r"<[^>]+>", "", title_match.group(1)) if title_match else "文章"
    )

    template = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="家庭中長期否定型互動模式的整理與心理學分析" />
  <meta name="robots" content="index, follow" />
  <title>{page_title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@400;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{CSS}" />
</head>
<body>
  <a class="skip-link" href="#main">跳到正文</a>
  <header class="site-header">
    <motion-wrap>
    <p class="site-header__eyebrow">家庭互動 · 心理學觀察</p>
    <h1 class="site-header__title">{page_title}</h1>
    <p class="site-header__note">第三方觀察整理 · 非臨床診斷 · 供閱讀與回顧脈絡</p>
    </motion-wrap>
  </header>
  <motion-wrap>
  <motion-wrap>
  <div class="layout">
    <aside class="sidebar">
      {toc_html}
    </aside>
    <main id="main" class="article">
      {body}
    </main>
  </div>
  </motion-wrap>
  <footer class="site-footer">
    <p>本文為個人整理與分析，僅供參考。如需臨床判斷請諮詢合格專業人員。</p>
  </footer>
  <script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    # Fix accidental motion-wrap tags from f-string - I used wrong placeholder
    template = template.replace("<motion-wrap>", "").replace("</motion-wrap>", "")

    OUT.write_text(template, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
