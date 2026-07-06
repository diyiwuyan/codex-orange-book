#!/usr/bin/env python3
"""
WorkBuddy 橙皮书 Markdown → 精美 HTML 转换器
产出单文件 HTML，橙皮书风格，可直接浏览器打印为 PDF
"""

import re
import sys
import html

def md_to_html(md_path, html_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    body_parts = []
    in_code_block = False
    in_table = False
    table_rows = []
    code_lang = ""
    code_lines = []

    def flush_table():
        nonlocal table_rows, in_table
        if not table_rows:
            return ""
        html = '<div class="table-wrap"><table>\n'
        for i, row in enumerate(table_rows):
            tag = 'th' if i == 0 else 'td'
            # row is a list of cell strings
            cells = ''.join(f'<{tag}>{c}</{tag}>' for c in row)
            html += f'<tr>{cells}</tr>\n'
        html += '</table></div>\n'
        table_rows = []
        in_table = False
        return html

    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')

        # Fenced code block
        if line.startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lang = line[3:].strip()
                code_lines = []
            else:
                in_code_block = False
                lang_class = f' class="language-{code_lang}"' if code_lang else ''
                code_content = html.escape('\n'.join(code_lines))
                body_parts.append(f'<pre><code{lang_class}>{code_content}</code></pre>\n')
                code_lang = ""
                code_lines = []
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Table detection
        if '|' in line and line.strip().startswith('|'):
            # Check if it's a separator line
            cleaned = line.strip().strip('|')
            if re.match(r'^[\s\-\|:]+$', cleaned):
                # Skip separator line
                i += 1
                continue
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            # Convert markdown in cells
            cells = [convert_inline_md(c) for c in cells]
            table_rows.append(cells)
            in_table = True
            i += 1
            continue
        else:
            if in_table:
                body_parts.append(flush_table())

        # HTML div blocks (e.g., contact-page, etc.)
        if line.strip().startswith('<div') and not line.strip().startswith('</div>'):
            # Collect until closing div
            div_content = [line]
            i += 1
            depth = 1
            while i < len(lines) and depth > 0:
                l = lines[i].rstrip('\n')
                if '<div' in l and '</div>' not in l:
                    depth += 1
                elif '</div>' in l and '<div' not in l:
                    depth -= 1
                div_content.append(l)
                i += 1
            body_parts.append(''.join(div_content) + '\n')
            continue

        if line.strip() == '</div>':
            body_parts.append(line + '\n')
            i += 1
            continue

        # Image handling: ![alt](path)
        m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$', line)
        if m:
            alt = m.group(1)
            src = m.group(2)
            body_parts.append(f'<figure class="img-figure"><img src="{src}" alt="{alt}"><figcaption>{alt}</figcaption></figure>\n')
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^---+$', line.strip()):
            body_parts.append('<hr>\n')
            i += 1
            continue

        # Headings
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text = convert_inline_md(m.group(2))
            anchor = re.sub(r'[^\w\u4e00-\u9fff-]', '', text)
            body_parts.append(f'<h{level} id="{anchor}">{text}</h{level}>\n')
            i += 1
            continue

        # Blockquote
        if line.startswith('> '):
            content = convert_inline_md(line[2:])
            body_parts.append(f'<blockquote>{content}</blockquote>\n')
            i += 1
            continue

        # Unordered list
        if re.match(r'^\s*[-*+]\s+', line):
            content = convert_inline_md(re.sub(r'^\s*[-*+]\s+', '', line))
            body_parts.append(f'<ul><li>{content}</li></ul>\n')
            i += 1
            continue

        # Empty line - skip
        if not line.strip():
            i += 1
            continue

        # Paragraph (merge consecutive normal lines)
        para_lines = [line]
        i += 1
        while i < len(lines) and is_paragraph_line(lines[i].rstrip('\n')):
            para_lines.append(lines[i].rstrip('\n'))
            i += 1
        content = ' '.join(convert_inline_md(l) for l in para_lines)
        body_parts.append(f'<p>{content}</p>\n')

    if in_table:
        body_parts.append(flush_table())

    body = ''.join(body_parts)

    # Cover page HTML
    cover = """
    <div class="cover">
      <div class="cover-sub">WORKBUDDY · ORANGE BOOK &nbsp;&nbsp;|&nbsp;&nbsp; NON-OFFICIAL GUIDE / 非官方指南</div>
      <div class="cover-title">WorkBuddy</div>
      <div class="cover-sub2">写给创作者、开发者与 AI 工具重度用户的使用手册</div>
      <div class="cover-line"></div>
      <div class="cover-book">橙皮书</div>
      <div class="cover-desc">从安装到实战案例的全链路使用指南</div>
      <div class="cover-desc2">非官方开源指南 · 持续更新版</div>
      <div class="cover-author">编 著 / BY 武小森</div>
      <div class="cover-sections">
        <div class="cover-section"><span class="cs-num">01</span>认识 WorkBuddy</div>
        <div class="cover-section"><span class="cs-num">02</span>安装与配置</div>
        <div class="cover-section"><span class="cs-num">03</span>核心功能</div>
        <div class="cover-section"><span class="cs-num">04</span>标准工作流</div>
        <div class="cover-section"><span class="cs-num">05</span>实战案例库</div>
      </div>
      <div class="cover-footer">v0.2.0 &nbsp;·&nbsp; 2026 · 07</div>
    </div>
    <div class="page-break"></div>
    """

    full_html = HTML_TEMPLATE.replace('{{BODY}}', cover + '\n' + body)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"✅ 已生成 HTML 文件：{html_path}")
    print(f"   在浏览器中打开后，按 ⌘+P 打印为 PDF")


def is_paragraph_line(line):
    """Return True if this line is a normal paragraph line (not heading, list, etc.)"""
    if not line.strip():
        return False
    if line.startswith('```'):
        return False
    if line.strip().startswith('|') and '|' in line:
        return False
    if line.strip().startswith('<div') or line.strip() == '</div>':
        return False
    if re.match(r'^#{1,6}\s+', line):
        return False
    if line.startswith('> '):
        return False
    if re.match(r'^\s*[-*+]\s+', line):
        return False
    if re.match(r'^---+$', line.strip()):
        return False
    if re.match(r'^!\[', line.strip()):
        return False
    return True


def convert_inline_md(text):
    """Convert inline markdown: bold, italic, code, links, images"""
    text = html.escape(text)
    # Code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Images: ![alt](path) -> <img src="path" alt="alt" class="inline-img">
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" class="inline-img">', text)
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WorkBuddy 橙皮书</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap');

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    font-size: 15px;
    line-height: 1.8;
    color: #2c2c2c;
    background: #fff;
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 50px;
  }

  /* ===== Cover Page ===== */
  .cover {
    text-align: center;
    padding: 60px 20px 40px;
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    border-radius: 12px;
    margin-bottom: 40px;
    page-break-after: always;
  }
  .cover-sub {
    font-size: 13px;
    color: #e65100;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 30px;
  }
  .cover-title {
    font-size: 72px;
    font-weight: 900;
    color: #e65100;
    letter-spacing: -2px;
    line-height: 1.1;
    margin-bottom: 16px;
  }
  .cover-sub2 {
    font-size: 18px;
    color: #bf360c;
    margin-bottom: 30px;
  }
  .cover-line {
    width: 80px;
    height: 4px;
    background: #e65100;
    margin: 0 auto 30px;
    border-radius: 2px;
  }
  .cover-book {
    font-size: 42px;
    font-weight: 900;
    color: #e65100;
    letter-spacing: 12px;
    margin-bottom: 10px;
  }
  .cover-desc {
    font-size: 20px;
    color: #333;
    margin-bottom: 6px;
  }
  .cover-desc2 {
    font-size: 15px;
    color: #666;
    margin-bottom: 40px;
  }
  .cover-author {
    font-size: 16px;
    color: #e65100;
    letter-spacing: 4px;
    margin-bottom: 50px;
  }
  .cover-sections {
    display: flex;
    justify-content: center;
    gap: 30px;
    flex-wrap: wrap;
    margin-bottom: 50px;
  }
  .cover-section {
    font-size: 13px;
    color: #555;
    text-align: center;
  }
  .cover-section .cs-num {
    display: block;
    font-size: 22px;
    font-weight: 900;
    color: #e65100;
    margin-bottom: 4px;
  }
  .cover-footer {
    font-size: 14px;
    color: #999;
    letter-spacing: 2px;
  }

  /* ===== Typography ===== */
  h1 {
    font-size: 28px;
    font-weight: 900;
    color: #e65100;
    border-bottom: 3px solid #ff9800;
    padding-bottom: 10px;
    margin: 48px 0 20px;
    page-break-after: avoid;
  }
  h2 {
    font-size: 22px;
    font-weight: 700;
    color: #f57c00;
    border-left: 5px solid #ff9800;
    padding-left: 14px;
    margin: 36px 0 14px;
    page-break-after: avoid;
  }
  h3 {
    font-size: 18px;
    font-weight: 700;
    color: #ef6c00;
    margin: 28px 0 10px;
    page-break-after: avoid;
  }
  h4 {
    font-size: 16px;
    font-weight: 700;
    color: #e65100;
    margin: 20px 0 8px;
  }

  p { margin: 10px 0; }

  strong { color: #e65100; font-weight: 700; }

  blockquote {
    border-left: 4px solid #ff9800;
    background: #fff8e1;
    margin: 16px 0;
    padding: 12px 18px;
    border-radius: 0 8px 8px 0;
    color: #5d4037;
    font-style: italic;
  }

  code {
    background: #f5f5f5;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 1px 6px;
    font-size: 13px;
    font-family: 'Fira Code', 'Consolas', monospace;
    color: #d84315;
  }

  pre {
    background: #263238;
    color: #eceff1;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 16px 0;
    overflow-x: auto;
    font-size: 13px;
    line-height: 1.6;
    page-break-inside: avoid;
  }
  pre code {
    background: none;
    border: none;
    padding: 0;
    color: inherit;
    font-size: inherit;
  }

  /* ===== Tables ===== */
  .table-wrap {
    overflow-x: auto;
    margin: 16px 0;
    page-break-inside: avoid;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
  }
  th {
    background: linear-gradient(135deg, #ff9800, #f57c00);
    color: white;
    padding: 10px 14px;
    text-align: left;
    font-weight: 700;
  }
  td {
    padding: 9px 14px;
    border-bottom: 1px solid #eee;
  }
  tr:nth-child(even) td {
    background: #fff8e1;
  }

  /* ===== Lists ===== */
  ul, ol {
    margin: 10px 0 10px 24px;
  }
  li { margin: 5px 0; }

  /* ===== Horizontal Rule ===== */
  hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, #ff9800, transparent);
    margin: 36px 0;
  }

  /* ===== Page Break ===== */
  .page-break {
    page-break-after: always;
  }

  /* ===== Inline Images (in tables, blockquotes, etc.) ===== */
  img.inline-img {
    max-width: 100%;
    max-height: 180px;
    border-radius: 6px;
    vertical-align: middle;
  }

  /* ===== Print Styles ===== */
  @media print {
    @page { size: A4; margin: 12mm; }
    body { padding: 0; }
    .cover { page-break-after: always; padding: 40px 20px; }
    .contact-page { page-break-after: always; padding: 30px 20px; }
    pre, table, blockquote { page-break-inside: avoid; }
    h1, h2, h3 { page-break-after: avoid; }
    figure.img-figure img { max-width: 100%; }
  }

  /* ===== TOC (if present) ===== */
  .toc { margin: 20px 0 40px; }
  .toc h2 { border-left: none; padding-left: 0; }

  /* ===== Contact Page ===== */
  .contact-page {
    text-align: center;
    padding: 50px 30px 40px;
    background: linear-gradient(135deg, #fff8e1 0%, #fff3e0 100%);
    border-radius: 12px;
    margin: 20px 0 40px;
    page-break-after: always;
  }
  .contact-page h2 {
    font-size: 26px;
    border-left: none;
    padding-left: 0;
    color: #e65100;
    margin-bottom: 16px;
    text-align: center;
  }
  .contact-page h3 {
    font-size: 18px;
    color: #f57c00;
    margin-top: 28px;
    margin-bottom: 10px;
    text-align: left;
  }
  .contact-page p,
  .contact-page blockquote {
    text-align: left;
  }
  .contact-page blockquote {
    margin: 12px auto;
    max-width: 500px;
  }
  .contact-page table {
    width: 100%;
    max-width: 680px;
    margin: 16px auto;
  }
  .contact-page td {
    text-align: center;
    vertical-align: top;
    padding: 8px;
    border-bottom: none !important;
    background: transparent !important;
  }
  .contact-page img {
    max-width: 160px;
    max-height: 160px;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(230,81,0,0.12);
  }
  .contact-page figcaption {
    display: none;
  }

  /* ===== Image Figures ===== */
  figure.img-figure {
    margin: 20px 0;
    text-align: center;
    page-break-inside: avoid;
  }
  figure.img-figure img {
    max-width: 100%;
    max-height: 500px;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border: 1px solid #eee;
  }
  figure.img-figure figcaption {
    font-size: 13px;
    color: #888;
    margin-top: 8px;
    font-style: italic;
  }
</style>
</head>
<body>
{{BODY}}
</body>
</html>
"""

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        md_to_html(sys.argv[1], sys.argv[2])
    else:
        md_to_html(
            "/Users/wangxiaoxian/wuyan/WorkBuddy橙皮书.md",
            "/Users/wangxiaoxian/wuyan/WorkBuddy橙皮书.html"
        )
