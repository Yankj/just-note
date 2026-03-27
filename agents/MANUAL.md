# 多 Agent 架构使用手册

_创建时间：2026-03-18_

---

## 架构概览

```
你 (用户)
  │
  ▼
小贾 (Orchestrator / 大管家)
  │
  ├── 📈 金融 Agent (按需 spawn)
  │     └── 职责：投资分析 + 金融日记 + 复盘
  │
  ├── 📝 生活工作日记 (小贾直管)
  │
  └── 📊 公司日报 (小贾整理，21:00 发送)
```

---

## 如何使用

### 1️⃣ 投资相关问题 → 自动触发金融 Agent

**你说**：
> "我想买入 10 万元腾讯，现在 150 港元，怎么看？"

**小贾**：
1. 判断为投资问题
2. Spawn 金融 Agent
3. 金融 Agent 调用 finance-council 分析
4. 记录分析过程到金融日记
5. 输出建议

---

### 2️⃣ 投资思考记录 → 自动记录到金融日记

**你说**：
> "今天看了宁德的财报，感觉现金流比想象中好，但估值还是偏高"

**小贾**：
1. 判断为投资思考
2. Spawn 金融 Agent
3. 金融 Agent 记录到 `/agents/finance-agent/memory/diary/2026-03-18.md`
4. 提炼核心逻辑和情绪状态

---

### 3️⃣ 生活/工作/规划 → 小贾记录到生活日记

**你说**：
> "最近在思考要不要换工作，现在的工作稳定但成长有限"

**小贾**：
1. 判断为生活规划
2. 记录到 `/memory/life-work/2026-03-18.md`
3. 帮你梳理思路

---

### 4️⃣ 公司日报 → 每天 21:00 自动发送

**内容**：
- 今日 Agent 活动汇总
- 投资思考摘要
- 生活工作思考摘要
- 明日待办

**时间**：每天 21:00（Asia/Shanghai）

---

## 文件位置

| 类型 | 路径 |
|------|------|
| 金融日记 | `/workspace/agents/finance-agent/memory/diary/YYYY-MM-DD.md` |
| 金融画像 | `/workspace/agents/finance-agent/memory/profile.md` |
| 生活日记 | `/workspace/memory/life-work/YYYY-MM-DD.md` |
| 公司日报 | `/workspace/memory/daily-report/YYYY-MM-DD.md` |
| 架构计划 | `/workspace/temp/multi-agent-architecture-plan.md` |

---

## 金融 Agent 触发条件

以下情况会自动 spawn 金融 Agent：

- ✅ 提到股票/基金/加密货币名称或代码
- ✅ 提到"买入"/"卖出"/"持仓"/"建仓"/"减仓"
- ✅ 提到"投资"/"理财"/"交易"
- ✅ 提到"怎么看 XXX"/"XXX 值得买吗"
- ✅ 表达投资相关的思考或复盘

---

## 查看日记

**查看今日金融日记**：
```bash
cat /workspace/agents/finance-agent/memory/diary/2026-03-18.md
```

**查看本周所有金融日记**：
```bash
ls /workspace/agents/finance-agent/memory/diary/
```

**查看你的投资画像**：
```bash
cat /workspace/agents/finance-agent/memory/profile.md
```

---

## 周/月复盘

**周复盘**（每周日）：
- 金融 Agent 读取本周日记
- 提取思维模式和情绪变化
- 输出到 `weekly-review/`

**月复盘**（每月末）：
- 对比预测 vs 实际
- 更新投资画像
- 识别认知优势和盲区

---

## 常见问题

**Q: 金融 Agent 是常驻的吗？**
A: 按需 spawn（Q3=A 决策），用完回收。但有独立记忆，下次 spawn 会读取历史。

**Q: 如果我不想让某些投资思考被记录？**
A: 直接告诉我"这条不要记录"，我会跳过。

**Q: 公司日报太频繁/不频繁？**
A: 可以调整 cron 时间，或改为每周/每月发送。

**Q: 智囊团和营销大师呢？**
A: 目前先聚焦金融 Agent。需要时可以用同样方式创建智囊团 Agent。

---

## 下一步

1. **试用 1 周**：正常使用，记录投资思考
2. **周末复盘**：检查日记质量，调整模板
3. **优化迭代**：根据你的反馈改进

---

## 今天就可以开始

**试试这样说**：
> "我想记录一个投资思考：..."

或

> "帮我分析一下 XXX 股票"

或

> "今天看了 XXX 的财报，我的感觉是..."
