# 财务自由之路 - 技术架构设计

**版本**：MVP 1.0  
**日期**：2026-03-20  
**设计原则**：轻前端、重后端、多端复用

---

## 一、整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    前端层（薄客户端）                     │
├─────────────────────────────────────────────────────────┤
│  Web (React)  │  Telegram Bot  │  小程序  │  App (未来)  │
└─────────────────────────────────────────────────────────┘
                          │
                          │ REST API / WebSocket
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    API 网关层                              │
├─────────────────────────────────────────────────────────┤
│  认证鉴权  │  限流  │  日志  │  路由  │  数据格式转换    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   业务逻辑层（后端核心）                   │
├─────────────────────────────────────────────────────────┤
│  财务规划服务  │  投资复盘服务  │  心理诊断服务          │
│  资产视图服务  │  被动收入服务  │  AI 对话中枢           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   AI Agent 层                             │
├─────────────────────────────────────────────────────────┤
│  编排 Agent  │  规划 Agent  │  复盘 Agent  │  心理 Agent  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   数据层                                  │
├─────────────────────────────────────────────────────────┤
│  金融数据 API  │  向量库  │  关系库  │  缓存  │  文件存储  │
└─────────────────────────────────────────────────────────┘
```

---

## 二、技术选型

### 前端层（薄客户端）

| 组件 | 技术 | 说明 |
|------|------|------|
| **Web** | React + Vite | 快速开发，热更新 |
| **UI 组件** | Ant Design / MUI | 成熟组件库 |
| **状态管理** | Zustand | 轻量级 |
| **图表** | Recharts / ECharts | 数据可视化 |
| **构建** | Vite | 快速构建 |

**核心原则**：
- 前端只负责渲染和交互
- 所有业务逻辑在后端
- 通过 API 调用获取数据
- 未来多端只需换 UI 层

---

### API 网关层

| 组件 | 技术 | 说明 |
|------|------|------|
| **框架** | FastAPI (Python) | 快速开发，自动文档 |
| **认证** | JWT | 无状态认证 |
| **限流** | Redis + 令牌桶 | 防止滥用 |
| **日志** | Structlog | 结构化日志 |
| **文档** | Swagger / OpenAPI | 自动生成 |

---

### 业务逻辑层

| 服务 | 技术 | 说明 |
|------|------|------|
| **框架** | FastAPI (Python) | 与网关一致 |
| **财务规划** | Python + NumPy | 计算密集型 |
| **投资复盘** | Python + NLP | 文本分析 |
| **心理诊断** | Python + ML | 情感分析 |
| **资产视图** | Python + 缓存 | 数据聚合 |
| **AI 对话** | OpenClaw SDK | Agent 调用 |

---

### AI Agent 层

| Agent | 实现 | 说明 |
|-------|------|------|
| **编排 Agent** | OpenClaw | 任务分发 |
| **规划 Agent** | OpenClaw Skill | 财务自由路径 |
| **复盘 Agent** | OpenClaw Skill | 投资日记分析 |
| **心理 Agent** | OpenClaw Skill | 情绪识别 |
| **资产 Agent** | OpenClaw Skill | 数据聚合 |
| **对话 Agent** | OpenClaw | 自然语言交互 |

**大模型**：
- 推理：Claude 3.5 / Qwen-Max
- 嵌入：text-embedding-3-large
- 向量库：Pinecone / 本地 FAISS

---

### 数据层

| 组件 | 技术 | 说明 |
|------|------|------|
| **金融数据** | 新浪财经 API / akshare | 免费实时数据 |
| **关系库** | PostgreSQL | 用户数据/交易记录 |
| **向量库** | FAISS (MVP) / Pinecone | 投资日记检索 |
| **缓存** | Redis | 会话/热点数据 |
| **文件存储** | 本地/MINIO | 截图/语音文件 |

---

## 三、金融数据 API 清单

### 国内数据

| 数据 | 来源 | API | 成本 |
|------|------|-----|------|
| A 股行情 | 新浪财经 | 免费 | 0 |
| 港股行情 | 新浪财经 | 免费 | 0 |
| 美股行情 | 新浪财经 | 免费 | 0 |
| 基金净值 | 天天基金 | 免费 | 0 |
| 宏观数据 | 国家统计局 | 免费 | 0 |
| 财经新闻 | 新华财经 | 企业 API | 2 万/年 |

### 国际数据

| 数据 | 来源 | API | 成本 |
|------|------|-----|------|
| 全球股票 | Yahoo Finance | yfinance 库 | 免费 |
| 加密货币 | CoinGecko | 免费 API | 0 |
| 外汇 | 新浪财经 | 免费 | 0 |
| 黄金/大宗 | 新浪财经 | 免费 | 0 |

### API 封装

```python
# 统一数据接口
class FinanceDataAPI:
    def get_stock_price(self, symbol: str) -> dict
    def get_fund_nav(self, code: str) -> dict
    def get_portfolio_value(self, holdings: list) -> dict
    def get_market_news(self, category: str) -> list
```

---

## 四、核心模块设计

### 模块 1：财务自由规划

**输入**：
- 当前资产（现金/股票/基金/房产）
- 月收入/支出
- 目标被动收入
- 风险偏好

**处理**：
```python
def calculate_freedom_path(current_assets, monthly_saving, target_passive_income, risk_level):
    # 计算储蓄率
    # 计算预期收益率（基于风险偏好）
    # 计算财务自由年限
    # 生成动态路径
    return {
        "years_to_freedom": 10,
        "required_saving_rate": 0.4,
        "required_return_rate": 0.08,
        "milestones": [...]
    }
```

**输出**：
- 财务自由年限
- 所需储蓄率
- 所需收益率
- 里程碑路径

---

### 模块 2：投资日记&AI 复盘

**输入**：
- 交易记录（截图/语音/文本）
- 当时想法（日记）
- 市场数据（自动获取）

**处理**：
```python
def analyze_trade(trade_record, diary_entry, market_context):
    # OCR/语音识别
    # 情感分析（贪婪/恐惧）
    # 交易逻辑分析
    # 盈亏归因
    return {
        "emotion": "贪婪",
        "logic_score": 7,
        "mistake": "追高",
        "suggestion": "等待回调"
    }
```

**输出**：
- 情绪识别
- 逻辑评分
- 错误分析
- 改进建议

---

### 模块 3：交易心理诊断

**输入**：
- 历史交易记录
- 投资日记
- 行为模式

**处理**：
```python
def diagnose_psychology(trade_history, diaries):
    # 识别行为模式（过度交易/损失厌恶）
    # 计算心理评分
    # 生成矫正方案
    return {
        "biases": ["损失厌恶", "过度自信"],
        "score": 65,
        "action_plan": [...]
    }
```

**输出**：
- 认知偏差识别
- 心理评分
- 行为矫正方案

---

### 模块 4：全资产统一视图

**输入**：
- 各平台持仓（手动/自动同步）
- 房产/副业（手动录入）

**处理**：
```python
def aggregate_assets(holdings):
    # 聚合多平台数据
    # 计算总净值
    # 计算收益率
    # 资产配置分析
    return {
        "total_net_worth": 1000000,
        "total_return": 0.15,
        "allocation": {"股票": 0.4, "基金": 0.3, ...}
    }
```

**输出**：
- 总净值
- 总收益率
- 资产配置饼图
- 收益趋势图

---

### 模块 5：被动收入追踪

**输入**：
- 被动收入来源（股息/房租/版税）
- 月度支出

**处理**：
```python
def track_passive_income(income_sources, monthly_expenses):
    # 计算被动收入总额
    # 计算覆盖率（被动收入/支出）
    # 预测达到 100% 覆盖时间
    return {
        "monthly_passive": 10000,
        "coverage_rate": 0.6,
        "months_to_100": 24
    }
```

**输出**：
- 月度被动收入
- 覆盖率进度条
- 预测时间
- 优化建议

---

### 模块 6：AI 对话中枢

**输入**：
- 用户自然语言问题

**处理**：
```python
def chat_with_agent(user_input, context):
    # 意图识别
    # 任务分发到对应 Agent
    # 聚合结果
    # 生成自然语言回复
    return {
        "response": "根据你的情况，建议...",
        "action": "show_planning_board",
        "data": {...}
    }
```

**输出**：
- 自然语言回复
- UI 动作指令
- 相关数据

---

## 五、数据库设计

### 用户表

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP,
    risk_level VARCHAR(50),
    financial_goal JSONB
);
```

### 资产表

```sql
CREATE TABLE assets (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    type VARCHAR(50),  -- 股票/基金/房产/现金
    symbol VARCHAR(100),
    amount DECIMAL,
    cost_basis DECIMAL,
    current_value DECIMAL,
    updated_at TIMESTAMP
);
```

### 交易日记表

```sql
CREATE TABLE trade_diaries (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    trade_id UUID,
    entry_text TEXT,
    emotion_score DECIMAL,
    ai_analysis JSONB,
    created_at TIMESTAMP
);
```

### 心理评分表

```sql
CREATE TABLE psychology_scores (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    score DECIMAL,
    biases JSONB,
    action_plan JSONB,
    created_at TIMESTAMP
);
```

---

## 六、API 设计

### 核心 API

```
POST   /api/v1/planning/calculate          # 计算财务自由路径
GET    /api/v1/planning/progress           # 获取进度

POST   /api/v1/diary/create                # 创建投资日记
GET    /api/v1/diary/list                  # 获取日记列表
POST   /api/v1/diary/analyze               # AI 分析日记

GET    /api/v1/psychology/score            # 获取心理评分
POST   /api/v1/psychology/diagnose         # 心理诊断

GET    /api/v1/assets/summary              # 资产汇总
POST   /api/v1/assets/sync                 # 同步资产

GET    /api/v1/passive-income/progress     # 被动收入进度
POST   /api/v1/passive-income/optimize     # 优化建议

POST   /api/v1/chat                        # AI 对话
```

---

## 七、安全设计

### 数据安全

- 传输加密：HTTPS/TLS
- 存储加密：AES-256
- 字段加密：敏感字段（资产金额）单独加密
- 访问控制：JWT + RBAC

### 合规设计

- 免责声明：明确"非投资建议"
- 隐私政策：用户数据使用透明
- 数据最小化：只收集必要数据
- 用户删除权：支持数据导出/删除

---

## 八、部署架构

### MVP 部署（单机）

```
┌─────────────────────┐
│  Nginx (反向代理)    │
└─────────────────────┘
         │
┌─────────────────────┐
│  FastAPI (后端)     │
│  + OpenClaw SDK     │
└─────────────────────┘
         │
┌─────────────────────┐
│  PostgreSQL         │
│  Redis              │
│  FAISS              │
└─────────────────────┘
```

### 生产部署（分布式）

```
┌─────────────────────┐
│  AWS ALB            │
└─────────────────────┘
         │
┌────────┴────────┐
│  ECS (后端 x3)   │
└─────────────────┘
         │
┌────────┴────────┐
│  RDS (PostgreSQL)│
│  ElastiCache     │
└─────────────────┘
```

---

## 九、开发计划

### 阶段 1：核心架构（1 周）

- [ ] 搭建 FastAPI 框架
- [ ] 设计数据库 schema
- [ ] 实现基础 CRUD
- [ ] 接入 OpenClaw SDK

### 阶段 2：6 大模块（2 周）

- [ ] 财务自由规划模块
- [ ] 投资日记模块
- [ ] 心理诊断模块
- [ ] 资产视图模块
- [ ] 被动收入模块
- [ ] AI 对话模块

### 阶段 3：前端开发（2 周）

- [ ] React 框架搭建
- [ ] 6 大模块 UI
- [ ] 数据可视化
- [ ] 响应式设计

### 阶段 4：测试优化（1 周）

- [ ] 单元测试
- [ ] 集成测试
- [ ] 性能优化
- [ ] 安全测试

### 阶段 5：部署上线（1 周）

- [ ] 服务器配置
- [ ] 域名/SSL
- [ ] 监控告警
- [ ] 灰度发布

---

**总计**：7 周 MVP 上线
