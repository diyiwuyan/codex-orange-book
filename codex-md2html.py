#!/usr/bin/env python3
"""
Codex 橙皮书 Markdown → 精美 HTML 转换器
复用 md2html.py 的转换逻辑，生成后替换封面为 Codex 版本 + 优化排版分页 v2
"""

import sys
import re
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md2html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 先生成 HTML
md2html.md_to_html(
    os.path.join(BASE_DIR, 'Codex橙皮书.md'),
    os.path.join(BASE_DIR, 'Codex橙皮书.html')
)

# 读取生成的 HTML
with open(os.path.join(BASE_DIR, 'Codex橙皮书.html'), 'r', encoding='utf-8') as f:
    content = f.read()

# 替换封面内容
old_cover = '''    <div class="cover">
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
    </div>'''

new_cover = '''    <div class="cover">
      <div class="cover-sub">CODEX · ORANGE BOOK &nbsp;&nbsp;|&nbsp;&nbsp; NON-OFFICIAL GUIDE / 非官方指南</div>
      <div class="cover-title">Codex</div>
      <div class="cover-sub2">写给开发者、办公人群与 AI 工具重度用户的使用手册</div>
      <div class="cover-line"></div>
      <div class="cover-book">橙皮书</div>
      <div class="cover-desc">从安装到实战案例的全链路使用指南</div>
      <div class="cover-desc2">非官方开源指南 · 持续更新版</div>
      <div class="cover-author">编 著 / BY 武小森</div>
      <div class="cover-sections">
        <div class="cover-section"><span class="cs-num">01</span>认识 Codex</div>
        <div class="cover-section"><span class="cs-num">02</span>安装与配置</div>
        <div class="cover-section"><span class="cs-num">03</span>核心功能</div>
        <div class="cover-section"><span class="cs-num">04</span>标准工作流</div>
        <div class="cover-section"><span class="cs-num">05</span>实战案例库</div>
      </div>
      <div class="cover-footer">v2.0 &nbsp;·&nbsp; 2026 · 07</div>
    </div>'''

if old_cover in content:
    content = content.replace(old_cover, new_cover)
    print('✅ 封面已替换为 Codex 版本')
else:
    print('⚠️ 未找到原封面，可能已被修改')

# 替换 title
content = content.replace('<title>WorkBuddy 橙皮书</title>', '<title>Codex 橙皮书</title>')

# ===== 排版优化 v2：精准分页控制 =====

# 1. 删除封面后多余的 page-break div（封面已有 page-break-after: always，再加 page-break div 会导致空白页）
content = content.replace('    <div class="page-break"></div>\n', '')
print('✅ 已移除封面后多余的 page-break div')

# 2. 移除旧版分页 CSS（如果有）
old_css_patterns = [
    r'  /\* ===== Codex 分页优化 ===== \*/.*?p \{ orphans: 2; widows: 2; \}\n',
]
for pattern in old_css_patterns:
    content = re.sub(pattern, '', content, flags=re.DOTALL)

# 2b. 修复 @media print 中的冲突规则
# md2html.py 的 @media print 里有 .contact-page { page-break-after: always; }，会和我们的 auto 冲突
content = content.replace(
    '.contact-page { page-break-after: always; padding: 30px 20px; }',
    '.contact-page { padding: 30px 20px; }'
)
# @media print 里的 h1, h2, h3 { page-break-after: avoid; } 保留，和我们的规则一致
print('✅ 已修复 @media print 中的冲突规则')

# 3. 在 </style> 前添加新的分页 CSS
page_break_css = """
  /* ===== Codex 分页优化 v2 ===== */
  /* 压缩标题和正文的间距，让整体排版更紧凑 */
  h1 { page-break-before: auto; margin: 24px 0 12px; }
  h2 { margin: 20px 0 10px; }
  h3 { margin: 16px 0 8px; }
  blockquote { padding: 10px 14px; margin: 12px 0; }
  /* 只让"第X篇"和"附录"的 h1 新起一页 */
  h1[id*="篇"], h1[id*="附录"] { page-break-before: always; margin-top: 24px; }
  /* 使用说明单独起一页，保证 0.1/0.2/0.3 在同一页 */
  h1[id*="0使用说明"] { page-break-before: always; margin-top: 24px; }
  /* 联系方式页：新起一页，但不加 page-break-after（避免和下一篇 h1 的 page-break-before 叠加产生空白页） */
  .contact-page { page-break-before: always; page-break-after: auto; }
  /* h2/h3 标题不独占页底 */
  h2, h3, h4 { page-break-after: avoid; }
  /* 表格、代码块、引用块、图片尽量不跨页 */
  .table-wrap, pre, blockquote, figure { page-break-inside: avoid; }
  /* 段落不在页底/页首只剩一行 */
  p { orphans: 2; widows: 2; }
  /* no-break 容器：内容不跨页（用于使用说明的子节） */
  .no-break { page-break-inside: avoid; }
  /* 使用说明的 no-break 容器不强制（内容可能超一页，允许自然分页） */
  .no-break.allow-break { page-break-inside: auto; }
  /* hr 分隔线不在页首，同时缩小间距 */
  hr { page-break-after: avoid; margin: 20px 0; }
  /* 列表尽量不跨页 */
  ul, ol { page-break-inside: auto; }
  /* 避免标题 + 第一个元素分离 */
  h2 + p, h2 + table, h2 + ul, h2 + ol, h2 + pre, h2 + blockquote,
  h3 + p, h3 + table, h3 + ul, h3 + ol, h3 + pre, h3 + blockquote { page-break-before: avoid; }
  /* 压缩联系方式页，让全部内容在一页内 */
  .contact-page { padding: 16px 20px; margin: 0; page-break-inside: avoid; font-size: 14px; }
  .contact-page h2 { margin-bottom: 8px; font-size: 22px; }
  .contact-page h3 { margin-top: 12px; margin-bottom: 4px; font-size: 16px; }
  .contact-page img { max-width: 90px; max-height: 90px; }
  .contact-page blockquote { margin: 6px auto; padding: 6px 10px; font-size: 12px; }
  .contact-page p { margin-bottom: 6px; }
  .contact-page table { margin: 8px auto; }
  .contact-page table td { padding: 4px; font-size: 12px; }
  .contact-page a[style*="display:inline-block"] { padding: 6px 20px !important; font-size: 15px !important; margin: 8px 0 !important; }
  .contact-page p[style*="border: 2px dashed"] { padding: 8px 14px !important; margin: 8px 0 !important; }
  .contact-page p[style*="border: 2px dashed"] strong { font-size: 15px !important; }
  .contact-page p[style*="border: 2px dashed"] br { display: none; }
  .contact-page p[style*="border: 2px dashed"] br + br { display: none; }
  /* 压缩标题页间距，让标题信息尽量集中在一页 */
  #CODEXORANGEBOOK { margin-top: 0; margin-bottom: 12px; }
  #Codex橙皮书从安装到实战案例的全链路使用指南 { margin-top: 8px; margin-bottom: 12px; }
"""
content = content.replace('</style>', page_break_css + '\n</style>')

# 4. 把"0. 使用说明"到"联系方式"之前的内容包裹在 no-break 容器里
#    使用 allow-break 类：优先不分页，但如果内容超一页则允许自然分页
pattern = r'(<h1[^>]*>0\.\s*使用说明</h1>.*?)(<div class="contact-page">)'
match = re.search(pattern, content, re.DOTALL)
if match:
    old_section = match.group(0)
    new_section = '<div class="no-break allow-break">\n' + match.group(1) + '</div>\n' + match.group(2)
    content = content.replace(old_section, new_section)
    print('✅ 使用说明部分已包裹为分页容器（允许自然分页）')

# 5. 清理可能存在的旧 no-break 包裹（防止重复包裹）
# 检查是否有嵌套的 no-break
nested_pattern = r'<div class="no-break(?: allow-break)?>\s*<div class="no-break(?: allow-break)?>'
if re.search(nested_pattern, content):
    print('⚠️ 检测到嵌套 no-break，已跳过（请检查 HTML）')

with open(os.path.join(BASE_DIR, 'Codex橙皮书.html'), 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Codex 橙皮书 HTML 已生成（分页优化 v2）')
