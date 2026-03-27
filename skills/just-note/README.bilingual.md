# just-note (记一下) - Bilingual Quick Reference

---

## 一句话介绍 / One-Liner

**中文**: 像发消息一样记录一切，AI 自动分类整理，让知识自然生长。

**English**: Record everything like sending messages. AI auto-classifies and organizes, letting knowledge grow naturally.

---

## 核心功能 / Core Features

| 中文 | English |
|------|---------|
| ✅ 零摩擦输入（微信/飞书消息） | ✅ Zero-friction input (WeChat/Feishu) |
| ✅ AI 自动分类（9 类内容） | ✅ AI auto-classification (9 types) |
| ✅ AI 标签生成 | ✅ AI tag generation |
| ✅ AI 标题生成 | ✅ AI title generation |
| ✅ 本地存储，数据自主 | ✅ Local storage, data control |
| ✅ 智能检索 | ✅ Smart search |
| ✅ 日记视图（按天聚合） | ✅ Diary view (daily aggregation) |
| ✅ 周报/月报（AI 生成） | ✅ Weekly/monthly reports (AI-generated) |

---

## 快速开始 / Quick Start

### 安装 / Installation

```bash
# 中文用户
npx clawhub install just-note-ai

# English users
npx clawhub install just-note-ai
```

### 使用 / Usage

#### 方式 1：微信/飞书消息 / WeChat/Feishu Message

```
中文：花了 200 块买书
English: Spent 200 yuan on books
```

#### 方式 2：CLI 命令 / CLI Command

```bash
just-note write --type expense --amount 200 --tags "book,learning" --content "Bought books"
```

---

## 内容类型 / Content Types

| 中文 | English | 示例 / Example |
|------|---------|----------------|
| inspiration | 灵感 | "This feature could..." |
| idea | 想法 | "A quote I read..." |
| knowledge | 知识 | "Python decorators..." |
| expense | 支出 | "Spent ¥200" |
| income | 收入 | "Received ¥5000" |
| diary | 日记 | "Met someone..." |
| task | 待办 | "Remember to..." |
| quote | 引用 | "XXX said: ..." |
| other | 其他 | "Test" |

---

## 常用命令 / Common Commands

```bash
# 记录 / Record
just-note write --type expense --amount 200 --content "Lunch"

# 今日记录 / Today
just-note today

# 搜索 / Search
just-note search "product"

# 统计 / Stats
just-note stats

# 导出 / Export
just-note export --format obsidian
```

---

## 对比 flomo / vs flomo

| 维度 / Feature | flomo | just-note-ai |
|----------------|-------|--------------|
| 输入方式 / Input | 微信/APP | 微信/飞书 |
| 分类方式 / Classification | 手动 / Manual | AI 自动 / AI Auto |
| 数据存储 / Storage | 云端 / Cloud | 本地 / Local |
| 价格 / Price | ¥12/月 | 免费 / Free |

---

## 链接 / Links

- **中文文档**: [SKILL.md](SKILL.md)
- **English Docs**: [README.en.md](README.en.md)
- **ClawHub**: https://clawhub.ai/skills/just-note-ai
- **GitHub**: https://github.com/your-org/just-note

---

## 许可证 / License

MIT License
