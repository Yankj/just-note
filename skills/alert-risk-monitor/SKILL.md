# Alert & Risk Monitor Skill

AI Native 的告警配置和项目风险检查工具。

## 理念

- **配置即代码**：告警规则用 Markdown/YAML 描述
- **检查即对话**：风险检查通过自然语言触发
- **结果即行动**：发现问题自动创建任务/通知

## 使用方式

### 1. 配置告警规则

创建 `alerts/alert-rules.md`：

```markdown
## 服务器监控
- [ ] CPU > 80% 持续 5 分钟 → 钉钉通知
- [ ] 内存 > 90% → 钉钉通知 + 自动扩容
- [ ] 磁盘 > 85% → 钉钉通知

## 业务监控
- [ ] API 错误率 > 1% → 钉钉通知
- [ ] 响应时间 P99 > 500ms → 钉钉通知
- [ ] 日活下降 > 10% → 日报提醒

## 代码质量
- [ ] CI 失败 → Slack 通知负责人
- [ ] 覆盖率下降 > 5% → PR 阻塞
- [ ] 安全漏洞 → 立即通知 + 工单
```

### 2. 检查项目风险

```bash
# 检查全组项目风险
openclaw skill run project-risk-check --scope team

# 检查特定项目
openclaw skill run project-risk-check --project finance-app

# 生成风险报告
openclaw skill run project-risk-check --output report.md
```

### 3. 配置告警渠道

```bash
# 添加钉钉机器人
openclaw skill run alert-config --add dingtalk --webhook $WEBHOOK_URL

# 添加 Slack 频道
openclaw skill run alert-config --add slack --channel #alerts

# 添加邮件通知
openclaw skill run alert-config --add email --to team@company.com
```

## 实现结构

```
alert-risk-monitor/
├── SKILL.md              # 本文件
├── src/
│   ├── alert-engine.ts   # 告警引擎
│   ├── risk-checker.ts   # 风险检查器
│   └── notifiers/        # 通知渠道
│       ├── dingtalk.ts
│       ├── slack.ts
│       └── email.ts
├── rules/
│   ├── server-rules.yaml
│   ├── business-rules.yaml
│   └── code-rules.yaml
└── templates/
    ├── alert-template.md
    └── report-template.md
```

## AI Native 特性

1. **自然语言配置**
   ```
   "帮我配置一个告警：当 API 错误率超过 1% 时通知后端团队"
   → 自动生成 YAML 配置 + 测试告警
   ```

2. **智能风险识别**
   ```
   "检查 finance-app 项目有什么潜在风险"
   → 扫描代码/依赖/配置 → 生成风险报告 + 修复建议
   ```

3. **自动修复建议**
   ```
   发现风险 → 生成修复 PR → 指派负责人 → 跟踪进度
   ```

4. **学习型告警**
   ```
   - 记录误报 → 自动调整阈值
   - 分析告警疲劳 → 合并相似告警
   - 学习响应模式 → 优化通知时机
   ```

## 示例输出

### 风险检查报告

```markdown
# 项目风险检查报告 - finance-app
**检查时间**: 2026-03-20 10:00
**检查范围**: 代码/依赖/配置/性能

## 🔴 高风险 (2)

### 1. 依赖漏洞：lodash < 4.17.21
- **文件**: package.json
- **影响**: CVE-2021-23337 原型污染漏洞
- **建议**: `npm update lodash@latest`
- **自动修复**: [创建 PR](link)

### 2. 数据库连接池配置不当
- **文件**: config/database.yaml
- **问题**: max_connections=5 (过低)
- **建议**: 调整为 20-50
- **自动修复**: [创建 PR](link)

## 🟡 中风险 (3)

### 1. 测试覆盖率下降
- **当前**: 72% (-5% vs 上周)
- **建议**: 补充单元测试

### 2. API 响应时间 P99 上升
- **当前**: 450ms (+120ms vs 上周)
- **建议**: 优化慢查询

### 3. 未处理的 Promise Rejection
- **文件**: src/services/api.ts:156
- **建议**: 添加 catch 处理

## 📊 趋势

| 指标 | 本周 | 上周 | 变化 |
|------|------|------|------|
| 高风险 | 2 | 1 | ⚠️ +1 |
| 中风险 | 3 | 5 | ✅ -2 |
| 覆盖率 | 72% | 77% | ⚠️ -5% |
| P99 | 450ms | 330ms | ⚠️ +36% |
```

## 快速开始

```bash
# 1. 安装 Skill
openclaw skill install alert-risk-monitor

# 2. 初始化配置
openclaw skill run alert-config --init

# 3. 运行首次检查
openclaw skill run project-risk-check --scope all

# 4. 设置定时检查 (每天 9:00)
openclaw cron add --schedule "0 9 * * *" --task "project-risk-check --notify"
```

---

**核心理念**: 让 AI 成为团队的"7x24 小时值班工程师"，人只做决策，不做重复检查。
