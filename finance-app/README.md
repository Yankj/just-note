# 财务自由之路 (Finance App)

个人投资管理与财务自由规划平台。

## 功能特性

- 📊 **资产管理**: 股票、基金、现金、加密货币等多资产类别
- 📈 **交易记录**: 完整的买卖交易记录与盈亏计算
- 📝 **投资日记**: 记录投资反思、市场分析、交易计划
- 📉 **数据分析**: 投资组合分析、收益趋势、交易统计
- 🔐 **安全可靠**: JWT 认证、数据加密、权限控制

## 技术栈

### 后端
- **框架**: FastAPI (Python 3.11+)
- **数据库**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0 (Async)
- **认证**: JWT (python-jose)
- **迁移**: Alembic

### 前端
- **框架**: React 18 + TypeScript
- **构建**: Vite 5
- **状态**: Zustand + React Query
- **路由**: React Router 6
- **样式**: Tailwind CSS
- **图表**: Recharts

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- (可选) Redis 7+

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，修改数据库配置和 SECRET_KEY

# 初始化数据库
python -m app.db.init_db

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 API 文档：http://localhost:8000/api/v1/docs

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，修改 API 地址

# 启动开发服务器
npm run dev
```

访问前端：http://localhost:5173

## 项目结构

```
finance-app/
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── core/        # 核心配置
│   │   ├── db/          # 数据库
│   │   ├── models/      # 数据模型
│   │   ├── schemas/     # Pydantic Schema
│   │   └── services/    # 业务逻辑
│   └── tests/           # 测试
│
├── frontend/            # React 前端
│   ├── src/
│   │   ├── components/  # 组件
│   │   ├── pages/       # 页面
│   │   ├── hooks/       # Hooks
│   │   ├── services/    # API 服务
│   │   ├── store/       # 状态管理
│   │   └── types/       # TypeScript 类型
│   └── public/
│
└── docs/                # 文档
    ├── database-schema.md
    ├── api-spec.md
    └── coding-standard.md
```

## 文档

- [数据库设计](docs/database-schema.md)
- [API 规范](docs/api-spec.md)
- [代码规范](docs/coding-standard.md)

## 开发规范

### Git 提交

```bash
# 格式：<type>(<scope>): <subject>
git commit -m "feat(assets): 添加资产批量导入功能"
git commit -m "fix(transactions): 修复交易记录分页错误"
```

### 代码检查

```bash
# 后端
cd backend
black app/
flake8 app/
mypy app/
pytest

# 前端
cd frontend
npm run lint
npm test
```

## API 端点

| 模块 | 端点 | 说明 |
|------|------|------|
| 认证 | POST /api/v1/auth/register | 用户注册 |
| 认证 | POST /api/v1/auth/login | 用户登录 |
| 资产 | GET /api/v1/assets | 获取资产列表 |
| 资产 | POST /api/v1/assets | 创建资产 |
| 交易 | GET /api/v1/transactions | 获取交易列表 |
| 交易 | POST /api/v1/transactions | 创建交易 |
| 日记 | GET /api/v1/diaries | 获取日记列表 |
| 日记 | POST /api/v1/diaries | 创建日记 |
| 分析 | GET /api/v1/analytics/portfolio | 投资组合概览 |

## 测试

```bash
# 后端测试
cd backend
pytest --cov=app

# 前端测试
cd frontend
npm test
```

## 部署

### Docker (推荐)

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

### 生产环境

1. 修改 `.env` 配置
2. 设置强密码和 SECRET_KEY
3. 配置 HTTPS
4. 设置数据库备份
5. 配置日志收集

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request!

---

**注意**: 本项目仅供学习和个人使用，不构成投资建议。
