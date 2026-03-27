# 测试计划 - 财务自由之路

## 1. 概述

本文档定义财务自由之路应用的完整测试策略，涵盖单元测试、集成测试和端到端测试。

### 1.1 测试目标

- 确保后端 API 功能的正确性和可靠性
- 验证前端组件的渲染和交互逻辑
- 保证数据库操作的数据一致性
- 确保认证授权机制的安全性
- 验证整体业务流程的完整性

### 1.2 测试范围

| 模块 | 单元测试 | 集成测试 | E2E 测试 |
|------|----------|----------|----------|
| 认证模块 (auth) | ✅ | ✅ | ✅ |
| 资产管理 (assets) | ✅ | ✅ | ✅ |
| 交易记录 (transactions) | ✅ | ✅ | ✅ |
| 投资日记 (diaries) | ✅ | ✅ | ✅ |
| 数据分析 (analytics) | ✅ | ✅ | ✅ |
| 前端组件 | ✅ | - | ✅ |
| 前端页面 | ✅ | - | ✅ |

---

## 2. 单元测试

### 2.1 后端单元测试

**测试框架**: pytest + pytest-asyncio

**测试目录**: `/tests/unit/backend/`

#### 2.1.1 认证模块测试

| 测试文件 | 测试内容 |
|----------|----------|
| `test_auth_schema.py` | UserCreate, User, Token, LoginRequest 数据验证 |
| `test_auth_security.py` | 密码哈希、JWT token 生成与验证 |
| `test_auth_api.py` | 注册、登录、获取用户信息 API |

#### 2.1.2 资产管理测试

| 测试文件 | 测试内容 |
|----------|----------|
| `test_asset_schema.py` | Asset, AssetCreate, AssetUpdate 数据验证 |
| `test_asset_service.py` | 资产 CRUD 操作、估值计算 |
| `test_asset_api.py` | 资产列表、详情、创建、更新、删除 API |

#### 2.1.3 交易记录测试

| 测试文件 | 测试内容 |
|----------|----------|
| `test_transaction_schema.py` | Transaction 数据验证 |
| `test_transaction_service.py` | 交易记录管理、盈亏计算 |
| `test_transaction_api.py` | 交易 API 端点 |

#### 2.1.4 投资日记测试

| 测试文件 | 测试内容 |
|----------|----------|
| `test_diary_schema.py` | Diary 数据验证 |
| `test_diary_service.py` | 日记 CRUD、情绪分析 |
| `test_diary_api.py` | 日记 API 端点 |

#### 2.1.5 配置与安全测试

| 测试文件 | 测试内容 |
|----------|----------|
| `test_config.py` | 配置加载、环境变量解析 |
| `test_security.py` | 密码验证、token 加密解密 |

### 2.2 前端单元测试

**测试框架**: Jest + React Testing Library

**测试目录**: `/tests/unit/frontend/`

#### 2.2.1 组件测试

| 测试文件 | 测试内容 |
|----------|----------|
| `test_Button.test.tsx` | 按钮渲染、点击事件、禁用状态 |
| `test_Input.test.tsx` | 输入框渲染、值绑定、验证 |
| `test_Modal.test.tsx` | 模态框显示/隐藏、内容渲染 |
| `test_Table.test.tsx` | 表格数据渲染、排序、分页 |

#### 2.2.2 页面测试

| 测试文件 | 测试内容 |
|----------|----------|
| `test_AssetsOverview.test.tsx` | 资产总览页面渲染、数据加载 |
| `test_InvestmentDiary.test.tsx` | 投资日记页面交互 |
| `test_FinancialPlanning.test.tsx` | 财务规划页面计算逻辑 |

#### 2.2.3 服务测试

| 测试文件 | 测试内容 |
|----------|----------|
| `test_api.test.ts` | API 请求封装、拦截器 |
| `test_assets.test.ts` | 资产相关 API 调用 |

#### 2.2.4 工具函数测试

| 测试文件 | 测试内容 |
|----------|----------|
| `test_formatters.test.ts` | 金额格式化、日期格式化 |
| `test_validators.test.ts` | 表单验证逻辑 |

---

## 3. 集成测试

### 3.1 后端集成测试

**测试目录**: `/tests/integration/`

#### 3.1.1 数据库集成测试

| 测试文件 | 测试内容 |
|----------|----------|
| `test_db_connection.py` | 数据库连接、连接池 |
| `test_db_models.py` | ORM 模型、关系映射、级联操作 |
| `test_db_migrations.py` | 数据库迁移、版本管理 |

#### 3.1.2 API 集成测试

| 测试文件 | 测试内容 |
|----------|----------|
| `test_auth_flow.py` | 完整认证流程（注册→登录→访问受保护资源） |
| `test_asset_flow.py` | 资产完整生命周期 |
| `test_transaction_flow.py` | 交易记录完整流程 |

#### 3.1.3 缓存集成测试（如使用 Redis）

| 测试文件 | 测试内容 |
|----------|----------|
| `test_cache.py` | 缓存读写、过期策略 |

---

## 4. 端到端测试 (E2E)

### 4.1 E2E 测试框架

**推荐工具**: Playwright 或 Cypress

**测试目录**: `/tests/e2e/`

### 4.2 E2E 测试场景

| 测试文件 | 测试场景 |
|----------|----------|
| `test_auth.e2e.ts` | 用户注册、登录、登出、密码重置 |
| `test_asset_management.e2e.ts` | 添加资产、编辑资产、删除资产、查看资产列表 |
| `test_transaction_recording.e2e.ts` | 记录交易、查看交易历史、筛选交易 |
| `test_diary_writing.e2e.ts` | 写日记、编辑日记、查看日记列表 |
| `test_dashboard.e2e.ts` | 仪表盘数据展示、图表交互 |
| `test_responsive.e2e.ts` | 移动端适配、不同屏幕尺寸 |

### 4.3 E2E 测试配置

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 30000,
  use: {
    baseURL: 'http://localhost:5173',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
    { name: 'webkit', use: { browserName: 'webkit' } },
  ],
});
```

---

## 5. 测试执行策略

### 5.1 本地开发

```bash
# 运行所有单元测试
npm run test:unit          # 前端
pytest tests/unit/         # 后端

# 运行集成测试
pytest tests/integration/

# 运行 E2E 测试
npm run test:e2e
```

### 5.2 CI/CD 流程

| 触发条件 | 执行的测试 |
|----------|------------|
| Pull Request | 单元测试 + 集成测试 |
| 主分支合并 | 单元测试 + 集成测试 + E2E 测试 |
| 定时任务 (每日) | 完整测试套件 + 性能测试 |

### 5.3 测试覆盖率要求

| 模块 | 最低覆盖率 |
|------|------------|
| 后端业务逻辑 | 80% |
| 前端组件 | 70% |
| 核心算法 | 90% |
| API 端点 | 85% |

---

## 6. 测试数据管理

### 6.1 测试数据工厂

使用工厂模式创建测试数据，确保数据一致性和可重复性。

### 6.2 测试数据清理

- 每次测试前清空测试数据库
- 使用事务回滚确保测试隔离
- E2E 测试后清理产生的数据

---

## 7. 持续改进

### 7.1 测试评审

- 新功能必须附带测试用例
- 代码审查时同步审查测试
- 定期回顾测试覆盖率报告

### 7.2 测试维护

- 及时更新失效的测试
- 重构重复的测试代码
- 优化慢测试的执行时间

---

## 8. 附录

### 8.1 测试命令速查

```bash
# 后端
pytest                                    # 运行所有测试
pytest -v                                 # 详细输出
pytest --cov=app                          # 覆盖率报告
pytest tests/unit/test_auth_api.py -v     # 运行指定测试

# 前端
npm run test                              # 运行测试
npm run test:coverage                     # 覆盖率报告
npm run test:watch                        # 监听模式
```

### 8.2 相关文档

- [架构文档](../architecture.md)
- [API 文档](./api-docs.md)
- [开发指南](./development-guide.md)

---

*文档版本: 1.0.0*
*最后更新: 2026-03-20*
