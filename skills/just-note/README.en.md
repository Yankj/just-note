# just-note (记一下)

> Record everything like sending messages. AI auto-classifies and organizes, letting knowledge grow naturally.

## Design Philosophy

**AI as the brain (understanding/classification), CLI as the hands (execution)**

- **Message Mode** (Primary): WeChat/Feishu message → AI understands & classifies → CLI writes
- **CLI Mode** (Backup): Explicit parameters → CLI executes → File saved

## Quick Start

### Installation

```bash
# Copy to OpenClaw skills directory
npx clawhub install just-note-ai

# Or manually
cp -r ~/openclaw/workspace/skills/just-note ~/.openclaw/skills/just-note

# Test installation
just-note help
```

### Usage

#### Method 1: WeChat/Feishu Message (Recommended)

Just send a message, AI auto-classifies:
```
Spent 200 yuan on books
```

AI automatically processes:
- Type: expense
- Amount: 200
- Tags: [book, learning]

#### Method 2: CLI Command (For Debugging)

Specify parameters explicitly:
```bash
just-note write --type expense --amount 200 --tags "book,learning" --content "Bought books"
```

View today's records:
```bash
just-note today
```

Search history:
```bash
just-note search "product"
```

## Features

- ✅ Zero-friction input (WeChat/Feishu messages)
- ✅ AI auto-classification (9 content types)
- ✅ AI tag generation
- ✅ AI title generation
- ✅ Unified storage, multi-view presentation
- ✅ Smart search (keyword + type filter)
- ✅ Diary view (daily aggregation)
- ✅ Weekly/monthly reports (AI-generated)

## Content Types

| Type | Description | Example |
|------|-------------|---------|
| **inspiration** | Ideas, creativity | "This feature could work like..." |
| **idea** | Thoughts, insights | "A quote I read today..." |
| **knowledge** | Knowledge, explanations | "Python decorators work by..." |
| **expense** | Expenses | "Spent ¥200 on books" |
| **income** | Income | "Received ¥5000 freelance fee" |
| **diary** | Diary, feelings | "Met an interesting person today..." |
| **task** | Tasks, todos | "Remember to call doctor next week" |
| **quote** | Quotes, sayings | "XXX said: ..." |
| **other** | Other uncategorized | "Test" |

## Commands

### Recording

| Command | Description |
|---------|-------------|
| `just-note write --type <type> --content "..."` | Record with explicit parameters |
| `just-note quick "content"` | Quick record (type=other) |

### Querying

| Command | Description |
|---------|-------------|
| `just-note today` | View today's records |
| `just-note yesterday` | View yesterday's records |
| `just-note list` | List all records |
| `just-note list --type <type>` | Filter by type |
| `just-note list --from <date> --to <date>` | Filter by date range |
| `just-note search "<keyword>"` | Keyword search |
| `just-note diary --date <date>` | Diary view (daily aggregation) |

### Statistics

| Command | Description |
|---------|-------------|
| `just-note stats` | Overall statistics |
| `just-note stats --type expense` | Statistics by type |
| `just-note weekly` | Weekly summary |
| `just-note monthly` | Monthly summary |
| `just-note daily-summary` | Daily summary |

### Export

| Command | Description |
|---------|-------------|
| `just-note export --format flomo` | Export to flomo format (JSONL) |
| `just-note export --format obsidian` | Export to Obsidian (Markdown files) |
| `just-note export --format excel` | Export to Excel (CSV) |

## Note Format

Uses memory-notes format, supports knowledge graph:

```markdown
---
title: "AI-generated title"
type: inspiration  # One of 9 types
created: 2026-03-26T12:00:00+08:00
day-id: 2026-03-26  # For daily aggregation
tags: [tag1, tag2, tag3]
amount: 200  # Optional, for expense/income
currency: CNY  # Optional
source: wechat  # wechat/feishu/voice/image
---

# AI-generated title

## Original Content
User's original message content...

## AI Summary
- [insight] Core insight 1
- [insight] Core insight 2

## Related Notes
- relates_to [[Related note title]]
```

## Storage Structure

```
~/openclaw/workspace/memory/just-note/
├── 2026-03/
│   ├── 2026-03-26-120000.md
│   ├── 2026-03-26-140000.md
│   └── ...
├── 2026-04/
│   └── ...
└── index.json  # Optional, for faster search
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `JUST_NOTE_STORAGE` | Storage path | `memory/just-note` |
| `JUST_NOTE_LLM_MODEL` | LLM model | `qwen3.5-plus` |
| `JUST_NOTE_AUTO_TAG` | Auto-tagging | `true` |
| `JUST_NOTE_AUTO_RELATE` | Auto-relation | `true` |

### Config File

`~/.just-note/config.yaml`:

```yaml
storage: memory/just-note
llm:
  model: qwen3.5-plus
  temperature: 0.3
features:
  auto_tag: true
  auto_relate: true
  daily_summary: true
  weekly_report: true
notifications:
  daily_summary_time: "21:00"
  weekly_report_time: "Sunday 20:00"
```

## Best Practices

### 1. Recording Tips

- **Keep it short** - 1-3 sentences per record is ideal
- **Record immediately** - Capture ideas as soon as they come
- **Don't organize** - AI will auto-classify and tag
- **Review regularly** - Check weekly/monthly summaries

### 2. Search Tips

- **Search by tag** - `just-note search "#product"`
- **Filter by type** - `just-note list --type expense`
- **Find by date** - `just-note diary --date 2026-03-26`

### 3. Review Tips

- **Daily review** - Check today's records before sleep
- **Weekly summary** - Review on weekends
- **Monthly summary** - Reflect at month end

## Comparison with flomo

| Feature | flomo | just-note-ai |
|---------|-------|--------------|
| **Input** | WeChat/APP | WeChat/Feishu |
| **Classification** | Manual tags | **AI auto-classify** |
| **Content types** | General notes | **9 types (incl. expense)** |
| **Storage** | Cloud | **Local + optional cloud** |
| **Search** | Tags + keyword | **Keyword + type + semantic** |
| **Review** | Daily review | **Daily/weekly/monthly AI summary** |
| **Expense tracking** | ❌ | ✅ |
| **Price** | ¥12/month | **Free** |

## Roadmap

### Phase 1 (MVP) - 1-2 weeks

- ✅ Core recording
- ✅ AI classification
- ✅ Basic search
- ⏳ Daily summary

### Phase 2 (Enhancement) - 2-4 weeks

- ⏳ Semantic search
- ⏳ Smart relations
- ⏳ Expense charts
- ⏳ Export features

### Phase 3 (Productization) - 1-2 months

- ⏳ Web interface
- ⏳ Multi-device sync
- ⏳ Open API
- ⏳ Plugin system

## FAQ

### Q: What are the advantages over flomo?

**A:**
1. AI auto-classification (no manual tagging)
2. Expense tracking and statistics
3. Local storage (full data control)
4. Free and open source

### Q: Will I lose my data?

**A:**
- Data is stored locally in `memory/just-note/`
- Recommend regular Git backup or cloud sync
- Can export to flomo/Obsidian format

### Q: What if AI classification is inaccurate?

**A:**
- You can manually edit the `type` field in notes
- Accuracy improves with usage
- Feedback is welcome!

## License

MIT License

## Contributing

Issues and PRs are welcome!

GitHub: https://github.com/your-org/just-note

## Support

- Documentation: See [SKILL.md](SKILL.md)
- Issues: https://github.com/your-org/just-note/issues
- Discord: https://discord.gg/clawd
