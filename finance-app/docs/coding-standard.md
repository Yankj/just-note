# 代码规范文档

**项目**: 财务自由之路 (Finance App)  
**后端**: Python 3.11+ / FastAPI  
**前端**: TypeScript 5+ / React 18+  
**数据库**: PostgreSQL 15+

---

## 一、目录结构规范

### 1.1 后端目录结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   │
│   ├── api/                    # API 路由层
│   │   ├── __init__.py
│   │   ├── deps.py             # 依赖注入
│   │   ├── auth.py             # 认证相关
│   │   ├── assets.py           # 资产相关
│   │   ├── transactions.py     # 交易相关
│   │   ├── diaries.py          # 日记相关
│   │   └── analytics.py        # 分析相关
│   │
│   ├── core/                   # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py           # 配置管理
│   │   ├── security.py         # 安全相关 (JWT/密码)
│   │   └── exceptions.py       # 自定义异常
│   │
│   ├── db/                     # 数据库层
│   │   ├── __init__.py
│   │   ├── base.py             # Base 类
│   │   ├── session.py          # 会话管理
│   │   └── init_db.py          # 数据库初始化
│   │
│   ├── models/                 # 数据模型层 (ORM)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── asset.py
│   │   ├── transaction.py
│   │   └── diary.py
│   │
│   ├── schemas/                # Pydantic 模式层
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── asset.py
│   │   ├── transaction.py
│   │   └── diary.py
│   │
│   ├── services/               # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── asset.py
│   │   ├── transaction.py
│   │   ├── diary.py
│   │   └── market_data.py      # 市场数据服务
│   │
│   └── utils/                  # 工具函数
│       ├── __init__.py
│       ├── pagination.py
│       └── helpers.py
│
├── tests/                      # 测试目录
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_assets.py
│   └── ...
│
├── alembic/                    # 数据库迁移
│   ├── versions/
│   └── env.py
│
├── .env                        # 环境变量
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── README.md
```

### 1.2 前端目录结构

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
│
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   ├── index.css
│   │
│   ├── components/             # 可复用组件
│   │   ├── ui/                 # 基础 UI 组件
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── ...
│   │   ├── layout/             # 布局组件
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   └── features/           # 业务组件
│   │       ├── assets/
│   │       ├── transactions/
│   │       └── diaries/
│   │
│   ├── pages/                  # 页面组件
│   │   ├── Dashboard.tsx
│   │   ├── Assets.tsx
│   │   ├── Transactions.tsx
│   │   ├── Diaries.tsx
│   │   ├── Analytics.tsx
│   │   └── Settings.tsx
│   │
│   ├── hooks/                  # 自定义 Hooks
│   │   ├── useAuth.ts
│   │   ├── useAssets.ts
│   │   ├── useTransactions.ts
│   │   └── useDiaries.ts
│   │
│   ├── services/               # API 服务
│   │   ├── api.ts              # Axios 实例
│   │   ├── auth.ts
│   │   ├── assets.ts
│   │   ├── transactions.ts
│   │   └── diaries.ts
│   │
│   ├── store/                  # 状态管理 (Zustand/Redux)
│   │   ├── index.ts
│   │   ├── authSlice.ts
│   │   ├── assetSlice.ts
│   │   └── ...
│   │
│   ├── types/                  # TypeScript 类型
│   │   ├── index.ts
│   │   ├── user.ts
│   │   ├── asset.ts
│   │   └── transaction.ts
│   │
│   └── utils/                  # 工具函数
│       ├── format.ts           # 格式化函数
│       ├── validation.ts       # 验证函数
│       └── constants.ts        # 常量定义
│
├── .eslintrc.cjs
├── .prettierrc
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── package.json
└── README.md
```

---

## 二、命名规范

### 2.1 Python 命名规范

```python
# 变量和函数 - snake_case
user_id = 123
def get_user_by_id(user_id: int) -> User:
    pass

# 类名 - PascalCase
class UserService:
    pass

class AssetModel(Base):
    pass

# 常量 - UPPER_SNAKE_CASE
MAX_PAGE_SIZE = 100
DEFAULT_CURRENCY = "CNY"

# 私有方法/变量 - 单下划线前缀
def _internal_helper():
    pass

_internal_cache = {}

# 模块级私有 - 双下划线前缀 (名称修饰)
class User:
    __secret_key = "xxx"  # 名称修饰

# 文件名 - snake_case
user_service.py
asset_model.py
```

### 2.2 TypeScript 命名规范

```typescript
// 变量和函数 - camelCase
const userId = 123;
function getUserById(id: number): User { }

// 组件名 - PascalCase
function UserProfile() { }
const AssetList = () => { }

// 类名 - PascalCase
class UserService { }

// 接口和类型 - PascalCase
interface User { }
type AssetType = 'STOCK' | 'FUND';

// 常量 - UPPER_SNAKE_CASE
const MAX_PAGE_SIZE = 100;
const DEFAULT_CURRENCY = 'CNY';

// 私有成员 - # 前缀 (ES2022)
class User {
  #secretKey = 'xxx';
}

// 文件名 - PascalCase (组件) / camelCase (工具)
UserProfile.tsx
userService.ts
user.types.ts
```

### 2.3 数据库命名规范

```sql
-- 表名 - 复数 snake_case
CREATE TABLE users (...);
CREATE TABLE investment_diaries (...);

-- 列名 - snake_case
user_id, created_at, full_name

-- 索引名 - idx_表名_列名
CREATE INDEX idx_users_email ON users(email);

-- 主键约束 - pk_表名
CONSTRAINT pk_users PRIMARY KEY (id)

-- 外键约束 - fk_表名_关联表
CONSTRAINT fk_assets_user FOREIGN KEY (user_id) REFERENCES users(id)

-- 唯一约束 - uk_表名_列名
CONSTRAINT uk_users_email UNIQUE (email)

-- 检查约束 - chk_表名_列名
CONSTRAINT chk_quantity_positive CHECK (quantity >= 0)
```

---

## 三、代码风格规范

### 3.1 Python 代码规范

```python
# 导入顺序：标准库 -> 第三方库 -> 本地模块
import os
import sys
from datetime import datetime

import jwt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.user import User

# 类型注解 (必须)
def calculate_pnl(entry_price: float, exit_price: float, quantity: int) -> float:
    """计算盈亏"""
    return (exit_price - entry_price) * quantity

# 类定义
class AssetService:
    """资产管理服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_asset(self, asset_id: UUID) -> Asset | None:
        """获取资产详情"""
        return await self.db.get(Asset, asset_id)
    
    async def create_asset(self, data: AssetCreate) -> Asset:
        """创建新资产"""
        asset = Asset(**data.model_dump())
        self.db.add(asset)
        await self.db.commit()
        return asset

# 异常处理
from app.core.exceptions import NotFoundError, ValidationError

async def get_user_or_raise(user_id: UUID) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundError(f"User {user_id} not found")
    return user

# 文档字符串 (必须)
def format_currency(amount: float, currency: str = "CNY") -> str:
    """
    格式化货币金额
    
    Args:
        amount: 金额数值
        currency: 货币代码 (默认 CNY)
    
    Returns:
        格式化后的货币字符串
    
    Raises:
        ValueError: 当金额为负数时
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return f"{currency} {amount:,.2f}"
```

### 3.2 TypeScript 代码规范

```typescript
// 导入顺序：React -> 第三方库 -> 本地模块
import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Button } from '@/components/ui/Button';

import { useAuth } from '@/hooks/useAuth';
import { AssetService } from '@/services/assets';
import type { Asset } from '@/types/asset';

// 类型定义 (优先使用 interface)
interface Asset {
  id: string;
  symbol: string;
  name: string;
  quantity: number;
  marketValue: number;
}

interface AssetProps {
  asset: Asset;
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
}

// 函数组件 (使用箭头函数)
const AssetCard: React.FC<AssetProps> = ({ asset, onEdit, onDelete }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const handleEdit = useCallback(() => {
    onEdit?.(asset.id);
  }, [asset.id, onEdit]);
  
  return (
    <div className="asset-card">
      <h3>{asset.symbol}</h3>
      <p>{asset.name}</p>
    </div>
  );
};

// 自定义 Hook
export function useAssets() {
  const query = useQuery({
    queryKey: ['assets'],
    queryFn: () => AssetService.getAll(),
  });
  
  const createMutation = useMutation({
    mutationFn: (data: AssetCreate) => AssetService.create(data),
    onSuccess: () => {
      query.invalidate();
    },
  });
  
  return {
    ...query,
    createAsset: createMutation.mutateAsync,
  };
}

// JSDoc 注释
/**
 * 格式化货币金额
 * @param amount - 金额数值
 * @param currency - 货币代码 (默认 CNY)
 * @returns 格式化后的货币字符串
 * @throws {Error} 当金额为负数时
 */
export function formatCurrency(amount: number, currency = 'CNY'): string {
  if (amount < 0) {
    throw new Error('Amount cannot be negative');
  }
  return `${currency} ${amount.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}`;
}
```

---

## 四、Git 提交规范

### 4.1 Commit Message 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 4.2 Type 类型

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `style` | 代码格式 (不影响功能) |
| `refactor` | 重构 (既不是新功能也不是 bug 修复) |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建/工具/配置更新 |
| `ci` | CI 配置 |
| `revert` | 回滚提交 |

### 4.3 Scope 范围

```
auth        # 认证模块
assets      # 资产模块
transactions # 交易模块
diaries     # 日记模块
analytics   # 分析模块
ui          # UI 组件
api         # API 接口
db          # 数据库
config      # 配置
deps        # 依赖
```

### 4.4 提交示例

```bash
# 新功能
git commit -m "feat(assets): 添加资产批量导入功能"

# Bug 修复
git commit -m "fix(transactions): 修复交易记录分页计算错误"

# 文档更新
git commit -m "docs: 更新 API 文档和 README"

# 重构
git commit -m "refactor(auth): 重构 JWT 认证逻辑，提升可测试性"

# 性能优化
git commit -m "perf(analytics): 优化投资组合查询性能，减少 50% 查询时间"

# 测试
git commit -m "test(assets): 添加资产服务单元测试"

# 配置
git commit -m "chore: 更新 ESLint 配置规则"
```

### 4.5 Git 工作流

```bash
# 分支命名
main              # 主分支 (生产)
develop           # 开发分支
feature/xxx       # 功能分支
bugfix/xxx        # Bug 修复分支
release/v1.0.0    # 发布分支
hotfix/xxx        # 紧急修复分支

# 提交流程
git checkout develop
git checkout -b feature/add-asset-import

# 开发...

git add .
git commit -m "feat(assets): 添加资产批量导入功能"

git push origin feature/add-asset-import

# 创建 Pull Request -> 代码审查 -> 合并到 develop
```

---

## 五、API 设计规范

### 5.1 RESTful 规范

```python
# 资源命名 - 复数名词
GET    /api/v1/assets          # 获取资产列表
POST   /api/v1/assets          # 创建资产
GET    /api/v1/assets/{id}     # 获取资产详情
PUT    /api/v1/assets/{id}     # 更新资产
DELETE /api/v1/assets/{id}     # 删除资产

# 子资源
GET    /api/v1/assets/{id}/transactions  # 获取资产交易记录

# 操作类 - 使用 POST
POST   /api/v1/assets/{id}/sync          # 同步资产价格
POST   /api/v1/auth/login                # 登录
POST   /api/v1/auth/refresh              # 刷新 Token
```

### 5.2 响应格式

```python
# 成功响应
{
  "data": {...},
  "message": "操作成功"
}

# 列表响应
{
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "page_size": 20
  }
}

# 错误响应
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": [
      {"field": "email", "message": "邮箱格式不正确"}
    ]
  }
}
```

### 5.3 状态码使用

| 状态码 | 使用场景 |
|--------|----------|
| 200 | 成功 (GET/PUT) |
| 201 | 创建成功 (POST) |
| 204 | 删除成功 (DELETE) |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 422 | 验证错误 |
| 500 | 服务器错误 |

---

## 六、测试规范

### 6.1 Python 测试

```python
# tests/test_assets.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAssetAPI:
    """资产 API 测试"""
    
    def test_create_asset(self, auth_headers):
        """测试创建资产"""
        payload = {
            "asset_type": "STOCK",
            "symbol": "600519",
            "name": "贵州茅台",
            "quantity": 100,
            "avg_cost": 1800.00
        }
        
        response = client.post(
            "/api/v1/assets",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["symbol"] == "600519"
        assert data["quantity"] == 100
    
    def test_get_assets(self, auth_headers):
        """测试获取资产列表"""
        response = client.get(
            "/api/v1/assets",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert "items" in response.json()
    
    @pytest.mark.asyncio
    async def test_asset_service(self, db_session):
        """测试资产服务"""
        service = AssetService(db_session)
        asset = await service.create_asset(
            AssetCreate(
                asset_type="STOCK",
                symbol="00700",
                name="腾讯控股"
            )
        )
        
        assert asset.symbol == "00700"
        assert asset.id is not None
```

### 6.2 TypeScript 测试

```typescript
// src/components/AssetCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import AssetCard from './AssetCard';

describe('AssetCard', () => {
  const mockAsset = {
    id: '1',
    symbol: '600519',
    name: '贵州茅台',
    quantity: 100,
    marketValue: 180000,
  };

  it('渲染资产信息', () => {
    render(<AssetCard asset={mockAsset} />);
    
    expect(screen.getByText('600519')).toBeInTheDocument();
    expect(screen.getByText('贵州茅台')).toBeInTheDocument();
  });

  it('触发编辑回调', () => {
    const onEdit = vi.fn();
    render(<AssetCard asset={mockAsset} onEdit={onEdit} />);
    
    fireEvent.click(screen.getByRole('button', { name: /编辑/i }));
    
    expect(onEdit).toHaveBeenCalledWith('1');
  });
});
```

---

## 七、安全规范

### 7.1 密码安全

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# 密码要求：最少 8 位，包含大小写字母和数字
```

### 7.2 JWT 配置

```python
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### 7.3 CORS 配置

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 生产环境配置实际域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 八、性能优化规范

### 8.1 数据库查询优化

```python
# 使用索引
# CREATE INDEX idx_transactions_user_date ON transactions(user_id, tx_date DESC);

# 避免 N+1 查询
from sqlalchemy.orm import selectinload

# 错误：N+1 查询
assets = await db.scalars(select(Asset))
for asset in assets:
    transactions = await db.scalars(select(Transaction).where(Transaction.asset_id == asset.id))

# 正确：预加载
assets = await db.scalars(
    select(Asset).options(selectinload(Asset.transactions))
)

# 分页查询
offset = (page - 1) * page_size
query = select(Asset).offset(offset).limit(page_size)
```

### 8.2 缓存策略

```python
from functools import lru_cache
from datetime import timedelta

@lru_cache(maxsize=128)
def get_market_data(symbol: str) -> dict:
    # 缓存市场数据
    pass

# Redis 缓存
from redis import Redis

redis = Redis(host='localhost', port=6379)

async def get_asset_price(symbol: str) -> float:
    cached = redis.get(f"price:{symbol}")
    if cached:
        return float(cached)
    
    price = await fetch_price_from_api(symbol)
    redis.setex(f"price:{symbol}", timedelta(minutes=5), str(price))
    return price
```

---

## 九、文档规范

### 9.1 README 模板

```markdown
# 项目名称

简要描述项目功能和目标。

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### 安装

```bash
# 后端
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 配置

# 前端
cd frontend
npm install
```

### 运行

```bash
# 后端
uvicorn app.main:app --reload

# 前端
npm run dev
```

## 项目结构

[链接到目录结构文档]

## API 文档

启动后访问：http://localhost:8000/docs

## 测试

```bash
pytest
npm test
```

## 贡献指南

[链接到贡献指南]

## 许可证

MIT
```

---

## 十、检查清单

### 代码提交前检查

- [ ] 代码通过 lint 检查 (black/flake8/eslint)
- [ ] 所有测试通过
- [ ] 类型检查通过 (mypy/tsc)
- [ ] 文档字符串完整
- [ ] 无硬编码配置 (使用环境变量)
- [ ] 敏感信息已移除
- [ ] Commit message 符合规范

### 代码审查检查

- [ ] 功能符合需求
- [ ] 代码可读性好
- [ ] 错误处理完善
- [ ] 性能考虑充分
- [ ] 安全性检查通过
- [ ] 测试覆盖充分
