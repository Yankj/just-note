# 财务自由计算与风险评估服务

## 概述

本模块提供财务自由规划核心算法和风险评估模型，包含：

1. **财务自由计算核心算法** - 计算达到财务自由所需时间和资产
2. **4% 法则计算器** - FIRE 运动核心计算工具
3. **复利计算模型** - 支持定投、反推收益率/年限
4. **风险评估模型** - 投资者风险承受能力评估 + 投资组合风险分析

## 算法精度

- 复利计算误差 ≤ 0.01%
- 4% 法则计算误差 ≤ 0.01%
- 财务自由年限计算误差 ≤ 1%
- 蒙特卡洛模拟 1000 次，成功率置信度 95%

## 安装使用

```python
from src.backend.services import (
    calculate_freedom,
    FinancialFreedomParams,
    FinancialFreedomCalculator,
    assess_risk_tolerance,
    analyze_portfolio_risk,
    FinancialRiskWarning
)
```

## API 文档

### 1. 财务自由计算

#### 便捷函数

```python
result = calculate_freedom(
    current_age=30,           # 当前年龄
    retirement_age=45,        # 目标退休年龄
    current_assets=100000,    # 当前资产
    annual_expenses=200000,   # 年支出
    annual_income=500000,     # 年收入
    savings_rate=0.4,         # 储蓄率 (0-1)
    investment_return_rate=0.07,  # 投资年化收益率
    inflation_rate=0.03,      # 通货膨胀率
    withdrawal_rate=0.04      # 提取率 (默认 4%)
)

print(f"{result.years_to_freedom}年后实现财务自由")
print(f"所需资产：¥{result.required_assets:,.2f}")
print(f"成功概率：{result.success_probability*100:.1f}%")
```

#### 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| years_to_freedom | float | 达到财务自由所需年数 |
| freedom_age | float | 财务自由时的年龄 |
| required_assets | float | 所需资产总额 |
| projected_assets | float | 预测资产总额 |
| success_probability | float | 成功概率 (0-1) |
| is_achievable | bool | 是否可实现 |
| annual_surplus | float | 年结余 |
| monthly_savings | float | 月储蓄额 |

#### 高级用法

```python
params = FinancialFreedomParams(
    current_age=30,
    retirement_age=45,
    current_assets=100000,
    annual_expenses=200000,
    annual_income=500000,
    savings_rate=0.4,
    investment_return_rate=0.07,
    inflation_rate=0.03,
    withdrawal_rate=0.04
)

calculator = FinancialFreedomCalculator(params)
result = calculator.calculate()

# 敏感性分析
sensitivity = calculator.get_sensitivity_analysis()
```

### 2. 复利计算器

```python
from src.backend.services import CompoundInterestCalculator

ci = CompoundInterestCalculator()

# 计算终值
fv = ci.calculate_future_value(
    principal=100000,        # 本金
    annual_rate=0.07,        # 年化收益率
    years=10,                # 投资年限
    compound_frequency=12,   # 复利频率 (12=月)
    monthly_contribution=2000 # 月定投
)

# 反推所需本金
required = ci.calculate_required_principal(
    future_value=200000,
    annual_rate=0.07,
    years=10
)

# 反推所需收益率
rate = ci.calculate_required_rate(
    principal=100000,
    future_value=200000,
    years=10
)

# 反推所需年限
years = ci.calculate_years(
    principal=100000,
    future_value=200000,
    annual_rate=0.07
)
```

### 3. 4% 法则计算器

```python
from src.backend.services import Rule4Calculator

rule4 = Rule4Calculator()

# 计算 FIRE 数字
freedom_number = rule4.calculate_freedom_number(
    annual_expenses=200000,
    withdrawal_rate=0.04  # 4% 提取率
)
# 结果：5000000 (年支出 × 25)

# 计算安全提取额
withdrawal = rule4.calculate_safe_withdrawal(
    portfolio_value=5000000,
    withdrawal_rate=0.04
)

# 验证安全性
safety = rule4.validate_safety(
    portfolio_value=5000000,
    annual_expenses=200000,
    years=30
)
```

### 4. 风险承受能力评估

```python
from src.backend.services import assess_risk_tolerance

result = assess_risk_tolerance(
    age=35,                    # 年龄
    employment_type='corporate', # 就业类型
    income_variability=0.1,    # 收入波动率
    years_employed=8,          # 从业年限
    total_assets=1500000,      # 总资产
    liquid_assets_ratio=0.3,   # 流动资产占比
    debt_ratio=0.25,           # 负债率
    emergency_fund_months=6,   # 应急资金月数
    years_investing=5,         # 投资年限
    product_types=4,           # 投资产品类型数
    has_losses=True,           # 是否有过亏损
    education_level='bachelor', # 教育水平
    loss_tolerance=0.2,        # 可承受亏损比例
    return_expectation=0.1,    # 期望收益率
    sleep_factor=0.2,          # 投资对睡眠影响
    investment_horizon=10,     # 投资期限 (年)
    goal_importance=0.7,       # 目标重要性
    goal_flexibility=0.5       # 目标灵活性
)

print(f"评分：{result['total_score']}")
print(f"等级：{result['risk_level']}")
print(f"建议：{result['recommendation']}")
```

#### 风险等级

| 等级 | 代码 | 评分范围 | 建议配置 |
|------|------|----------|----------|
| 保守型 | CONSERVATIVE | <35 | 80%+ 低风险产品 |
| 谨慎型 | CAUTIOUS | 35-50 | 60-70% 固收 +30-40% 权益 |
| 稳健型 | BALANCED | 50-65 | 50% 固收 +50% 权益 |
| 成长型 | GROWTH | 65-80 | 70% 权益 +30% 固收 |
| 激进型 | AGGRESSIVE | ≥80 | 高比例成长型资产 |

### 5. 投资组合风险分析

```python
from src.backend.services import analyze_portfolio_risk

# 日收益率序列
daily_returns = [0.01, -0.02, 0.03, 0.015, -0.01, 0.02, ...]

metrics = analyze_portfolio_risk(daily_returns)

print(f"波动率：{metrics['volatility']*100:.2f}%")
print(f"VaR(95%)：{metrics['var_95']*100:.2f}%")
print(f"最大回撤：{metrics['max_drawdown']*100:.2f}%")
print(f"Sharpe 比率：{metrics['sharpe_ratio']}")
print(f"Beta: {metrics['beta']}")
```

### 6. 财务风险预警

```python
from src.backend.services import FinancialRiskWarning

warner = FinancialRiskWarning()

result = warner.full_check(
    total_assets=2000000,
    total_liabilities=800000,
    liquid_assets=300000,
    monthly_expenses=20000,
    emergency_fund=100000,
    asset_allocation={
        'stocks': 800000,
        'bonds': 500000,
        'cash': 300000
    },
    returns=daily_returns,  # 可选
    current_drawdown=0.08   # 可选
)

print(f"风险等级：{result['risk_level']}")
print(f"警告：{result['warnings']}")
print(f"建议：{result['recommendations']}")
```

#### 预警指标

| 指标 | 预警线 | 危险线 |
|------|--------|--------|
| 负债率 | 50% | 70% |
| 流动资产占比 | <10% | - |
| 应急资金 | <3 个月 | - |
| 单一资产占比 | >50% | - |
| 波动率 | >30% | - |
| 最大回撤 | >20% | >40% |

## 运行测试

```bash
cd /home/admin/openclaw/workspace/finance-app
python3 -m unittest tests.test_financial_services -v
```

## 文件结构

```
finance-app/
├── src/
│   └── backend/
│       └── services/
│           ├── __init__.py
│           ├── freedom_calculator.py    # 财务自由计算核心
│           ├── risk_assessment.py       # 风险评估模型
│           └── README.md                # 本文档
└── tests/
    └── test_financial_services.py       # 单元测试 (38 个测试用例)
```

## 注意事项

1. **数据仅供参考**：所有计算结果不构成投资建议
2. **市场有风险**：历史收益率不代表未来表现
3. **定期更新**：建议每半年重新评估风险承受能力
4. **分散投资**：避免单一资产占比过高

## 版本

- v1.0.0 - 初始版本
  - 财务自由计算核心算法
  - 4% 法则计算器
  - 复利计算模型
  - 风险评估模型
  - 完整单元测试 (38 个用例，100% 通过)
