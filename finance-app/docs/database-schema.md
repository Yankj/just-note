# 数据库 Schema 设计

**数据库**: PostgreSQL 15+  
**字符集**: UTF-8  
**时区**: Asia/Shanghai

---

## 核心表结构

### 1. users（用户表）

存储用户基本信息和认证数据。

```sql
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) NOT NULL UNIQUE,
    username        VARCHAR(50) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    full_name       VARCHAR(100),
    avatar_url      VARCHAR(500),
    
    -- 财务相关
    base_currency   VARCHAR(3) NOT NULL DEFAULT 'CNY',
    net_worth_target DECIMAL(18,2),
    financial_freedom_date DATE,
    
    -- 状态
    is_active       BOOLEAN NOT NULL DEFAULT true,
    is_verified     BOOLEAN NOT NULL DEFAULT false,
    last_login_at   TIMESTAMPTZ,
    
    -- 审计
    created_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- 约束
    CONSTRAINT chk_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- 索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_active ON users(is_active);

-- 更新时间触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

### 2. assets（资产表）

存储用户持有的各类资产（股票、基金、现金等）。

```sql
CREATE TABLE assets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- 资产标识
    asset_type      VARCHAR(20) NOT NULL, -- STOCK, FUND, CASH, CRYPTO, OTHER
    symbol          VARCHAR(50) NOT NULL, -- 股票代码/基金代码
    name            VARCHAR(200) NOT NULL, -- 资产名称
    market          VARCHAR(20), -- 市场：A 股/港股/美股
    
    -- 持仓信息
    quantity        DECIMAL(18,6) NOT NULL DEFAULT 0,
    avg_cost        DECIMAL(18,4) NOT NULL DEFAULT 0, -- 平均成本
    current_price   DECIMAL(18,4), -- 当前价格（缓存）
    market_value    DECIMAL(18,2), -- 市值（缓存）
    
    -- 盈亏
    unrealized_pnl  DECIMAL(18,2), -- 浮动盈亏
    unrealized_pnl_pct DECIMAL(6,4), -- 浮动盈亏率
    realized_pnl    DECIMAL(18,2) NOT NULL DEFAULT 0, -- 已实现盈亏
    
    -- 状态
    is_active       BOOLEAN NOT NULL DEFAULT true,
    is_hidden       BOOLEAN NOT NULL DEFAULT false,
    
    -- 审计
    created_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_synced_at  TIMESTAMPTZ,
    
    -- 约束
    CONSTRAINT chk_asset_type CHECK (asset_type IN ('STOCK', 'FUND', 'CASH', 'CRYPTO', 'OTHER')),
    CONSTRAINT chk_quantity_positive CHECK (quantity >= 0),
    CONSTRAINT chk_avg_cost_positive CHECK (avg_cost >= 0),
    UNIQUE (user_id, asset_type, symbol, market)
);

-- 索引
CREATE INDEX idx_assets_user_id ON assets(user_id);
CREATE INDEX idx_assets_type ON assets(asset_type);
CREATE INDEX idx_assets_symbol ON assets(symbol);
CREATE INDEX idx_assets_active ON assets(user_id, is_active);

-- 触发器
CREATE TRIGGER update_assets_updated_at
    BEFORE UPDATE ON assets
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

### 3. transactions（交易记录表）

存储所有买卖交易记录。

```sql
CREATE TABLE transactions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    asset_id        UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    
    -- 交易信息
    tx_type         VARCHAR(10) NOT NULL, -- BUY, SELL, DIVIDEND, TRANSFER, FEE
    tx_date         DATE NOT NULL,
    tx_time         TIME NOT NULL DEFAULT '00:00:00',
    
    -- 交易详情
    quantity        DECIMAL(18,6) NOT NULL,
    price           DECIMAL(18,4) NOT NULL, -- 成交单价
    amount          DECIMAL(18,2) NOT NULL, -- 成交金额
    fee             DECIMAL(18,2) NOT NULL DEFAULT 0, -- 手续费
    currency        VARCHAR(3) NOT NULL DEFAULT 'CNY',
    
    -- 交易场所
    broker          VARCHAR(100), -- 券商/平台
    order_id        VARCHAR(100), -- 订单号
    notes           TEXT,
    
    -- 审计
    created_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- 约束
    CONSTRAINT chk_tx_type CHECK (tx_type IN ('BUY', 'SELL', 'DIVIDEND', 'TRANSFER', 'FEE')),
    CONSTRAINT chk_quantity_positive CHECK (quantity > 0),
    CONSTRAINT chk_price_positive CHECK (price >= 0),
    CONSTRAINT chk_amount_positive CHECK (amount >= 0)
);

-- 索引
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_asset_id ON transactions(asset_id);
CREATE INDEX idx_transactions_date ON transactions(tx_date);
CREATE INDEX idx_transactions_type ON transactions(tx_type);
CREATE INDEX idx_transactions_user_date ON transactions(user_id, tx_date DESC);

-- 触发器
CREATE TRIGGER update_transactions_updated_at
    BEFORE UPDATE ON transactions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

### 4. investment_diaries（投资日记表）

存储投资日记、交易反思、市场分析。

```sql
CREATE TABLE investment_diaries (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- 日记内容
    title           VARCHAR(200) NOT NULL,
    content         TEXT NOT NULL,
    diary_type      VARCHAR(20) NOT NULL DEFAULT 'REFLECTION', -- REFLECTION, ANALYSIS, PLAN, SUMMARY
    
    -- 关联
    related_assets  UUID[], -- 关联的资产 ID 数组
    related_tx_ids  UUID[], -- 关联的交易 ID 数组
    
    -- 标签与分类
    tags            VARCHAR(50)[], -- 标签数组
    category        VARCHAR(50), -- 分类
    
    -- 情绪与评分
    sentiment       VARCHAR(20), -- POSITIVE, NEUTRAL, NEGATIVE
    confidence_score INTEGER CHECK (confidence_score >= 1 AND confidence_score <= 10),
    
    -- 状态
    is_private      BOOLEAN NOT NULL DEFAULT true,
    is_pinned       BOOLEAN NOT NULL DEFAULT false,
    
    -- 审计
    created_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    diary_date      DATE NOT NULL DEFAULT CURRENT_DATE,
    
    -- 约束
    CONSTRAINT chk_diary_type CHECK (diary_type IN ('REFLECTION', 'ANALYSIS', 'PLAN', 'SUMMARY')),
    CONSTRAINT chk_sentiment CHECK (sentiment IN ('POSITIVE', 'NEUTRAL', 'NEGATIVE'))
);

-- 索引
CREATE INDEX idx_diaries_user_id ON investment_diaries(user_id);
CREATE INDEX idx_diaries_date ON investment_diaries(diary_date DESC);
CREATE INDEX idx_diaries_type ON investment_diaries(diary_type);
CREATE INDEX idx_diaries_tags ON investment_diaries USING GIN(tags);
CREATE INDEX idx_diaries_user_date ON investment_diaries(user_id, diary_date DESC);

-- 触发器
CREATE TRIGGER update_diaries_updated_at
    BEFORE UPDATE ON investment_diaries
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## 表关系图

```
┌─────────────┐
│   users     │
│  (用户表)    │
└──────┬──────┘
       │ 1:N
       ├──────────────────┐
       │                  │
       ▼                  ▼
┌─────────────┐    ┌───────────────────┐
│   assets    │    │ investment_diaries│
│  (资产表)    │    │   (投资日记表)     │
└──────┬──────┘    └───────────────────┘
       │ 1:N
       ▼
┌─────────────┐
│transactions │
│ (交易记录表) │
└─────────────┘
```

---

## 扩展表（后续迭代）

### 5. market_data（市场数据表）- 可选

```sql
CREATE TABLE market_data (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol          VARCHAR(50) NOT NULL,
    market          VARCHAR(20) NOT NULL,
    data_date       DATE NOT NULL,
    
    open_price      DECIMAL(18,4),
    high_price      DECIMAL(18,4),
    low_price       DECIMAL(18,4),
    close_price     DECIMAL(18,4) NOT NULL,
    volume          BIGINT,
    amount          DECIMAL(18,2),
    
    pe_ratio        DECIMAL(10,4),
    pb_ratio        DECIMAL(10,4),
    dividend_yield  DECIMAL(6,4),
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE (symbol, market, data_date)
);

CREATE INDEX idx_market_data_symbol_date ON market_data(symbol, market, data_date DESC);
```

### 6. user_settings（用户设置表）- 可选

```sql
CREATE TABLE user_settings (
    user_id         UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    
    theme           VARCHAR(20) NOT NULL DEFAULT 'light',
    language        VARCHAR(10) NOT NULL DEFAULT 'zh-CN',
    timezone        VARCHAR(50) NOT NULL DEFAULT 'Asia/Shanghai',
    
    -- 通知设置
    email_notifications BOOLEAN NOT NULL DEFAULT false,
    push_notifications  BOOLEAN NOT NULL DEFAULT false,
    
    -- 投资偏好
    risk_level      VARCHAR(20) DEFAULT 'MODERATE', -- CONSERVATIVE, MODERATE, AGGRESSIVE
    default_currency VARCHAR(3) DEFAULT 'CNY',
    
    settings_json   JSONB,
    
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

## 数据库初始化脚本

```sql
-- 启用 UUID 扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 执行上述 CREATE TABLE 语句...

-- 插入示例数据
INSERT INTO users (email, username, password_hash, full_name)
VALUES ('demo@example.com', 'demo', '$2b$12$...', '演示用户');
```

---

## 设计原则

1. **UUID 主键**: 避免 ID 泄露，支持分布式扩展
2. **软删除**: 使用 `is_active` 标记，保留历史数据
3. **审计字段**: 所有表都有 `created_at` / `updated_at`
4. **外键约束**: 确保数据完整性，级联删除
5. **索引优化**: 常用查询字段建立索引
6. **检查约束**: 数据有效性验证
7. **时区处理**: 统一使用 TIMESTAMPTZ，前端转换
