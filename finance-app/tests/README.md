# 测试指南

本目录包含财务自由之路应用的完整测试套件。

## 目录结构

```
tests/
├── README.md                    # 本文件
├── unit/                        # 单元测试
│   ├── backend/                 # 后端单元测试
│   │   ├── conftest.py          # pytest 配置和夹具
│   │   ├── test_config.py       # 配置测试
│   │   ├── test_security.py     # 安全模块测试
│   │   ├── test_auth_schema.py  # 认证 Schema 测试
│   │   ├── test_auth_api.py     # 认证 API 测试
│   │   ├── test_asset_schema.py # 资产 Schema 测试
│   │   └── test_asset_api.py    # 资产 API 测试
│   └── frontend/                # 前端单元测试
│       ├── components/          # 组件测试
│       ├── pages/               # 页面测试
│       ├── services/            # 服务测试
│       └── utils/               # 工具函数测试
├── integration/                 # 集成测试
│   └── test_auth_flow.py        # 认证流程测试
└── e2e/                         # E2E 测试
    ├── playwright.config.ts     # Playwright 配置
    ├── auth.setup.ts            # 认证设置
    ├── test_auth.e2e.ts         # 认证 E2E 测试
    └── test_asset_management.e2e.ts  # 资产管理 E2E 测试
```

## 快速开始

### 后端测试

```bash
# 进入后端目录
cd backend

# 安装测试依赖
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov pytest-mock httpx

# 运行所有单元测试
pytest tests/unit/

# 运行特定测试文件
pytest tests/unit/backend/test_auth_api.py -v

# 运行测试并生成覆盖率报告
pytest tests/unit/ --cov=app --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html
```

### 前端测试

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 运行单元测试
npm run test

# 运行测试（监听模式）
npm run test:watch

# 生成覆盖率报告
npm run test:coverage
```

### E2E 测试

```bash
# 进入前端目录
cd frontend

# 安装 Playwright
npx playwright install

# 运行 E2E 测试
npx playwright test

# 运行特定测试
npx playwright test test_auth.e2e.ts

# 以有头模式运行（显示浏览器）
npx playwright test --headed

# 生成 HTML 报告
npx playwright test --reporter=html
npx playwright show-report
```

## 测试规范

### 命名约定

- **单元测试**: `test_<module>_<function>.py` 或 `<Component>.test.tsx`
- **集成测试**: `test_<feature>_flow.py`
- **E2E 测试**: `test_<feature>.e2e.ts`

### 测试组织原则

1. **单元测试**: 测试单个函数、类或组件
2. **集成测试**: 测试多个模块的协作
3. **E2E 测试**: 测试完整的用户流程

### 测试数据

- 使用工厂模式创建测试数据
- 避免硬编码测试数据
- 每个测试应该独立，不依赖其他测试的状态

### 测试覆盖率目标

| 模块 | 最低覆盖率 |
|------|------------|
| 后端业务逻辑 | 80% |
| 前端组件 | 70% |
| 核心算法 | 90% |
| API 端点 | 85% |

## CI/CD 集成

测试会自动在以下场景运行：

- **Pull Request**: 单元测试 + 集成测试
- **主分支合并**: 完整测试套件 + E2E 测试
- **每日定时**: 完整测试套件 + 性能测试

查看 `.github/workflows/ci.yml` 了解详细配置。

## 常见问题

### Q: 如何跳过特定测试？

```python
@pytest.mark.skip(reason="需要实现认证后启用")
def test_something():
    pass
```

### Q: 如何只运行失败的测试？

```bash
# pytest
pytest --lf

# Playwright
npx playwright test --last-failed
```

### Q: 如何调试测试？

```bash
# pytest 详细输出
pytest -v -s

# Playwright 调试模式
npx playwright test --debug
```

### Q: 如何更新快照？

```bash
# Jest
npm run test -- -u

# Playwright
npx playwright test --update-snapshots
```

## 相关文档

- [测试计划](../docs/test-plan.md)
- [架构文档](../architecture.md)
- [开发指南](../docs/development-guide.md)
