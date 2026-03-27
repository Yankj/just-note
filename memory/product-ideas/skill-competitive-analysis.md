# Skill 竞品调研报告

**创建时间**: 2026-03-26  
**调研范围**: ClawHub、skills.sh、本地已安装 Skills

---

## 一、核心结论（TL;DR）

| 发现 | 说明 | 对我们的启示 |
|------|------|------------|
| **无直接竞品** | 没有「微信/飞书消息输入 → AI 自动整理」的 Skill | ✅ 市场空白，可先行 |
| **有相关能力** | 有笔记管理、知识图谱类 Skill（100-4K 安装量） | ⚠️ 用户有需求，但形态不同 |
| **技术路线差异** | 现有 Skill 多为「手动创建」，非「被动接收」 | ✅ 我们的差异化机会 |
| **OpenClaw 生态早期** | ClawHub 上还没有热门 Skill | ✅ 早期红利，易脱颖而出 |

---

## 二、Skill 市场概览

### 2.1 主要 Skill 平台

| 平台 | URL | 特点 | 成熟度 |
|------|-----|------|--------|
| **skills.sh** | https://skills.sh | 开放生态，支持多 Agent | 🟡 早期（数千 Skill） |
| **ClawHub** | https://clawhub.ai | OpenClaw 官方，版本管理 | 🔴 非常早期（几乎无 Skill） |
| **GitHub** | 搜索 `claude-skill` | 分散，无统一市场 | 🟡 分散 |

### 2.2 我们的本地环境

```
~/.openclaw/skills/ 目录：49 个 Skill
- 财务相关：finance-* 系列
- 数据获取：akshare-stock, stock-research-engine
- 工具类：agent-browser, agent-reach, api-gateway
- 知识管理：ontology（知识图谱）
```

---

## 三、笔记/知识类 Skill 详细对比

### 3.1 安装量 Top 榜（skills.sh 搜索 "note/memo/knowledge"）

| 排名 | Skill 名称 | 安装量 | 功能 | 与我们差异 |
|------|----------|--------|------|-----------|
| 1 | **notebooklm** (pleaseprompto) | 4.0K | Google NotebookLM 集成 | ❌ 需要手动操作 |
| 2 | **jupyter-notebook** (openai) | 716 | Jupyter 笔记本 | ❌ 代码场景 |
| 3 | **notebooklm** (teng-lin) | 937 | NotebookLM Python 库 | ❌ 代码场景 |
| 4 | **xiaohongshu-note-analyzer** | 1.7K | 小红书笔记分析 | ❌ 垂直场景 |
| 5 | **meeting-notes** | 1.1K | 会议纪要生成 | ⚠️ 场景接近，但非灵感记录 |
| 6 | **marimo-notebook** | 1.0K | Marimo 笔记本 | ❌ 代码场景 |
| 7 | **xhs-note-creator** | 725 | 小红书笔记创作 | ❌ 垂直场景 |
| 8 | **apple-notes** (steipete) | 551 | Apple Notes 集成 | ⚠️ 平台绑定 |
| 9 | **bear-notes** (steipete) | 312 | Bear Notes 集成 | ⚠️ 平台绑定 |
| 10 | **knowledge** (boshu2) | 167 | 通用知识管理 | ⚠️ 最接近竞品 |

### 3.2 重点竞品分析

#### 🥇 knowledge (boshu2/agentops) - 167 安装

**功能**: 通用知识管理能力

**实现方式**: 
- 手动创建知识条目
- 支持分类、标签
- 可能基于文件或数据库

**与我们差异**:
| 维度 | knowledge Skill | 我们 |
|------|----------------|------|
| 输入方式 | 手动创建 | 微信/飞书消息（被动接收） |
| 整理方式 | 手动分类 | AI 自动分类 |
| 使用场景 | 主动知识管理 | 灵感捕捉 |
| 摩擦度 | 中（需打开界面） | 低（发消息即可） |

---

#### 🥈 memory-notes (basicmachines-co) - 141 安装

**功能**: Basic Memory 笔记格式规范

**核心能力**:
- 教授如何写结构化笔记
- Frontmatter + Observations + Relations
- 知识图谱友好格式

**笔记格式示例**:
```markdown
---
title: API Design Decisions
tags: [api, architecture, decisions]
---

# API Design Decisions

## Observations
- [decision] Use REST over GraphQL for simplicity #api
- [requirement] Must support versioning from day one
- [risk] Rate limiting needed for public endpoints

## Relations
- implements [[API Specification]]
- depends_on [[Authentication System]]
```

**与我们差异**:
| 维度 | memory-notes | 我们 |
|------|-------------|------|
| 定位 | 笔记格式教学 | 自动笔记生成 |
| 输入方式 | 手动编写 | 消息自动转换 |
| AI 参与 | 无 | AI 自动分类 + 标签 |
| 学习成本 | 高（需学格式） | 低（无感使用） |

**可借鉴点**:
- ✅ Frontmatter 结构（title, tags, type）
- ✅ Observations 分类语法（[category] content）
- ✅ Relations 双向链接（[[Note Title]]）

---

#### 🥉 second-brain (sundial-org/awesome-openclaw-skills) - 24 安装

**功能**: 第二大脑/知识管理

**状态**: GitHub 404（可能已删除或私有化）

**启示**: 
- ⚠️ 这个方向有人尝试，但可能没坚持
- 需要验证是否技术问题还是需求问题

---

#### 其他相关 Skill

| Skill | 安装量 | 功能 | 状态 |
|------|--------|------|------|
| **notion-knowledge-capture** | 248 | Notion 知识捕获 | ✅ 活跃 |
| **knowledge-management** | 68 | 知识管理 | ⚠️ 低安装 |
| **local-knowledge** | 49 | 本地知识库 | ⚠️ 低安装 |
| **internal-memo-creator** | 45 | 内部备忘录 | ⚠️ 企业场景 |
| **zettelkasten-note-creation** | 38 | 卡片盒笔记 | ⚠️ 垂直方法 |
| **sqlite-notes** | 11 | SQLite 存储笔记 | ⚠️ 技术导向 |

---

## 四、技术路线对比

### 4.1 持久化方式

| Skill | 存储方式 | 优点 | 缺点 |
|------|---------|------|------|
| **memory-notes** | Markdown 文件 | 可读、可 Git | 检索慢 |
| **sqlite-notes** | SQLite 数据库 | 检索快 | 需工具查看 |
| **notion-knowledge-capture** | Notion API | 跨平台 | 依赖第三方 |
| **apple-notes** | Apple Notes API | 原生集成 | 平台绑定 |
| **knowledge** | 未知 | - | - |

**我们的选择**: Markdown 文件 + SQLite 索引（混合方案）

---

### 4.2 输入方式

| Skill | 输入方式 | 摩擦度 |
|------|---------|--------|
| **knowledge** | 手动创建 | 🔴 高 |
| **memory-notes** | 手动编写 | 🔴 高 |
| **notion-knowledge-capture** | 浏览器插件/手动 | 🟡 中 |
| **meeting-notes** | 会议录音/文字 | 🟡 中 |
| **我们** | 微信/飞书消息 | 🟢 低 |

---

### 4.3 AI 参与程度

| Skill | AI 角色 | 自动化程度 |
|------|--------|-----------|
| **knowledge** | 无 | 🔴 手动 |
| **memory-notes** | 无（格式教学） | 🔴 手动 |
| **meeting-notes** | 摘要生成 | 🟡 半自动 |
| **notion-knowledge-capture** | 内容提取 | 🟡 半自动 |
| **我们** | AI 自动分类 + 标签 | 🟢 全自动 |

---

## 五、市场机会分析

### 5.1 市场空白

✅ **验证过的需求**:
- 笔记类 Skill 有 100-4K 安装量 → 需求存在
- knowledge-management 类 Skill 多个 → 需求存在
- meeting-notes 1.1K 安装 → 自动整理有需求

❌ **市场空白**:
- **无「消息输入」Skill** — 没有利用微信/飞书等 IM 工具
- **无「AI 自动分类」Skill** — 大多是手动整理
- **无「灵感捕捉」定位** — 大多是正式笔记管理

### 5.2 我们的差异化

| 维度 | 现有 Skill | 我们 | 优势 |
|------|----------|------|------|
| **输入方式** | 手动创建 | 微信/飞书消息 | ✅ 摩擦更低 |
| **整理方式** | 手动分类 | AI 自动分类 | ✅ 更智能 |
| **使用场景** | 正式笔记 | 灵感捕捉 | ✅ 更轻量 |
| **学习成本** | 需学格式 | 无感使用 | ✅ 更简单 |
| **数据主权** | 依赖第三方 | 本地文件 | ✅ 更自主 |

---

## 六、可借鉴的 Skill 设计

### 6.1 memory-notes 的笔记格式

**推荐采用**:
```markdown
---
title: {{AI 生成标题}}
tags: [{{AI 生成标签 1}}, {{AI 生成标签 2}}]
type: {{AI 分类：inspiration/decision/note}}
created: {{ISO 时间戳}}
---

# {{标题}}

## 原始内容
{{用户消息原文}}

## AI 整理
- [category] {{AI 提取的关键点 1}}
- [category] {{AI 提取的关键点 2}}

## 关联笔记
- relates_to [[{{AI 推荐关联}}]]
```

**优点**:
- Frontmatter 机器可读
- Observations 结构化和搜索友好
- Relations 建立知识网络

---

### 6.2 knowledge 的通用设计

**推测功能**（基于名称和安装量）:
- 创建知识条目
- 分类管理
- 检索查询

**可借鉴**:
- 简单的 API 设计
- 通用的知识模型

---

## 七、竞品调研总结

### 7.1 竞争格局

```
                    自动化程度
                    低 ← → 高
                    ↓
        ┌───────────┼───────────┐
        │ knowledge │           │
        │ 167 installs│           │
  手动  │ memory-   │           │
  整理  │ notes     │   我们    │
        │ 141 installs│   (空白) │
        │           │           │
        ├───────────┼───────────┤
        │ meeting-  │           │
        │ notes     │           │
        │ 1.1K      │           │
  半自动│           │           │
        │ notion-   │           │
        │ capture   │           │
        │ 248       │           │
        └───────────┴───────────┘
```

**结论**: 「高自动化 + 灵感捕捉」是市场空白

---

### 7.2 我们的定位

**一句话**: 
> 第一个「微信/飞书消息输入 → AI 自动整理」的 OpenClaw Skill

**目标**:
- 短期：填补市场空白（1-2 周 MVP）
- 中期：成为 OpenClaw 热门 Skill（1-2 月）
- 长期：独立产品化（3-6 月）

---

### 7.3 风险与应对

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| 大厂抄袭（如 flomo 做 Skill） | 低 | 高 | 快速迭代，建立社区 |
| 已有 Skill 增加 AI 功能 | 中 | 中 | 专注「消息输入」差异化 |
| 用户需求不真实 | 中 | 高 | 快速验证（1 周 MVP） |
| 技术实现困难 | 低 | 中 | 复用现有 OpenClaw 能力 |

---

## 八、下一步行动

### 8.1 本周（验证阶段）

- [ ] **创建笔记 Skill MVP**
  - 输入：微信/飞书消息
  - 处理：AI 自动分类 + 标签
  - 输出：Markdown 文件（memory-notes 格式）

- [ ] **发布到 ClawHub**
  - 第一个「消息输入」Skill
  - 强调差异化（AI 自动整理）

- [ ] **自己深度使用**
  - 记录每次使用体验
  - 修正 AI 分类错误

### 8.2 下周（迭代阶段）

- [ ] **找 3-5 个极客用户试用**
  - 收集反馈
  - 验证「消息输入」是否真的更简单

- [ ] **优化 AI 分类**
  - 根据反馈调整 Prompt
  - 增加规则辅助（提高准确率）

### 8.3 下个月（推广阶段）

- [ ] **发布到 skills.sh**
  - 扩大影响力
  - 吸引更多用户

- [ ] **写推广文章**
  - 少数派、V2EX、知乎
  - 强调「AI 自动整理」+「消息输入」

---

## 九、参考资料

- [skills.sh](https://skills.sh/)
- [ClawHub](https://clawhub.ai/)
- [memory-notes Skill](https://github.com/basicmachines-co/basic-memory-skills)
- [knowledge Skill](https://skills.sh/boshu2/agentops/knowledge)
- [meeting-notes Skill](https://skills.sh/shubhamsaboo/awesome-llm-apps/meeting-notes)

---

> **核心洞察**: 笔记类 Skill 有需求（100-4K 安装量），但现有产品都是「手动创建」，没有「消息输入 + AI 自动整理」。这是我们的市场机会。
