# Codex 橙皮书 · Orange Book

> 非官方开源指南 · 持续更新版
> 编著：武小森

一份写给开发者、办公人群与 AI 工具重度用户的 OpenAI Codex 使用指南，覆盖从安装配置到实战案例的全链路内容。

## 📖 阅读入口

| 格式 | 链接 | 说明 |
|------|------|------|
| **在线阅读** | [GitHub Pages](https://diyiwuyan.github.io/codex-orange-book/) | 精美排版，无需下载 |
| **PDF 下载** | [Codex橙皮书.pdf](Codex橙皮书.pdf) | 64 页 · 5MB |
| **Markdown 原稿** | [Codex橙皮书.md](Codex橙皮书.md) | 完整源文件 |

## 内容结构

| 篇章 | 内容 |
|---|---|
| 使用说明 | 重要声明 · 适合人群 · 阅读路线 · **已知限制与诚实建议** |
| 第一篇 | 先搞懂 Codex 是什么（基础认知 / 同类工具对比 / 适用场景） |
| 第二篇 | 安装、配置与界面认识（App / CLI / IDE Extension / 目录管理） |
| 第三篇 | 核心功能详解（对话 / 计划模式 / 插件 / Skill / MCP / Git / 记忆 / 自动化 / 云端） |
| 第四篇 | 标准工作流（7 步链路 + 8 个任务模板） |
| 第五篇 | 场景化最佳实践（新手第一周 / 做网站 / 做 PPT / 代码审查） |
| 第六篇 | 实战案例库（7 个案例：产品官网 / 招商 PPT / 宣传视频 / 代码审查 / 数据分析 / 自动化测试 / 技术文档） |
| 附录 | 第三方模型接入 · 推荐 Skill 清单 · 指令速查表 · 常见问题避坑 · 版本记录 |

## 本书特点

- **7 个实战案例** + **8 个任务模板**，不是只讲功能，更讲怎么用
- **不回避"坑"**：专门设有「已知限制与诚实建议」章节，诚实标注 Codex 的实际问题
- **非官方开源**，持续更新，欢迎 Star ⭐ 关注

## 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | GitHub Pages 在线阅读入口页 |
| `Codex橙皮书.md` | Markdown 原稿 |
| `Codex橙皮书.html` | 精美排版 HTML |
| `Codex橙皮书.pdf` | PDF 版本（64 页） |
| `codex-md2html.py` | Markdown → HTML 转换脚本（含分页优化） |
| `codex-generate-pdf.js` | Playwright PDF 生成脚本 |
| `md2html.py` | 基础 Markdown → HTML 转换器 |
| `contact-*.jpg` | 联系方式二维码图片 |

## 自行构建

```bash
# 1. Markdown → HTML（含封面替换 + 分页优化）
python3 codex-md2html.py

# 2. HTML → PDF（需安装 Playwright）
node codex-generate-pdf.js
```

依赖：
- Python 3.10+
- Node.js 22+（Playwright）

## 联系方式

- 编著：**武小森**
- GitHub 仓库：https://github.com/diyiwuyan/codex-orange-book
- 知识星球 / 公众号 / 视频号 / 个人微信：见橙皮书联系方式页

## 声明

本橙皮书为非官方指南，不代表 OpenAI 官方文档或产品承诺。所有功能以 OpenAI 官方文档和 Codex 实际版本为准。Codex 更新很快，安装方式、模型名称、额度、入口位置和命令参数都可能变化。

## License

CC BY-NC-SA 4.0（署名-非商业性使用-相同方式共享）

## 版本

- v2.1 · 2026.07.06 — 新增「已知限制与诚实建议」章节；GitHub Pages 在线阅读上线；优化 PDF 分页排版
- v2.0 · 2026.07.06 — 全面迭代：精简内容、删除不存在功能、聚焦 Codex 实际能力；增加实战案例至 7 个；新增推荐 Skill 清单
- v1.0 · 2026.06.22 — 初始版本
