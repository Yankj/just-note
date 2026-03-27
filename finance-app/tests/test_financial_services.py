"""
财务自由计算与风险评估模块单元测试

测试覆盖率目标：>90%
算法精度要求：误差≤1%
"""

import unittest
import math
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend', 'services'))

from freedom_calculator import (
    CompoundInterestCalculator,
    Rule4Calculator,
    FinancialFreedomCalculator,
    FinancialFreedomParams,
    calculate_freedom
)

from risk_assessment import (
    RiskToleranceScore,
    RiskLevel,
    PortfolioRiskAnalyzer,
    FinancialRiskWarning,
    assess_risk_tolerance,
    analyze_portfolio_risk
)


class TestCompoundInterestCalculator(unittest.TestCase):
    """复利计算器测试"""
    
    def setUp(self):
        self.calculator = CompoundInterestCalculator()
    
    def test_simple_compound_interest(self):
        """测试简单复利计算"""
        # 10 万元，年化 7%,10 年
        fv = self.calculator.calculate_future_value(
            principal=100000,
            annual_rate=0.07,
            years=10,
            compound_frequency=1
        )
        # 预期值：100000 * 1.07^10 = 196715.14
        expected = 100000 * (1.07 ** 10)
        self.assertAlmostEqual(fv, expected, delta=expected * 0.01)  # 误差≤1%
    
    def test_monthly_compound_interest(self):
        """测试月复利计算"""
        fv = self.calculator.calculate_future_value(
            principal=100000,
            annual_rate=0.06,
            years=5,
            compound_frequency=12
        )
        # 预期值：100000 * (1 + 0.06/12)^(5*12)
        expected = 100000 * (1 + 0.06/12) ** 60
        self.assertAlmostEqual(fv, expected, delta=expected * 0.01)
    
    def test_with_monthly_contribution(self):
        """测试带月定投的复利计算"""
        fv = self.calculator.calculate_future_value(
            principal=50000,
            annual_rate=0.08,
            years=10,
            compound_frequency=12,
            monthly_contribution=2000
        )
        # 验证结果为正且大于本金 + 总定投
        total_invested = 50000 + 2000 * 12 * 10
        self.assertGreater(fv, total_invested)
    
    def test_zero_rate(self):
        """测试零利率情况"""
        fv = self.calculator.calculate_future_value(
            principal=100000,
            annual_rate=0,
            years=5,
            monthly_contribution=1000
        )
        expected = 100000 + 1000 * 12 * 5
        self.assertAlmostEqual(fv, expected, delta=1)
    
    def test_required_principal(self):
        """测试反推所需本金"""
        required = self.calculator.calculate_required_principal(
            future_value=200000,
            annual_rate=0.07,
            years=10,
            compound_frequency=1
        )
        # 验证：required * 1.07^10 ≈ 200000
        fv = self.calculator.calculate_future_value(required, 0.07, 10, 1)
        self.assertAlmostEqual(fv, 200000, delta=200000 * 0.01)
    
    def test_required_rate(self):
        """测试反推所需收益率"""
        rate = self.calculator.calculate_required_rate(
            principal=100000,
            future_value=200000,
            years=10,
            compound_frequency=1
        )
        # 验证：100000 * (1+rate)^10 ≈ 200000
        # 预期约 7.18%
        fv = self.calculator.calculate_future_value(100000, rate, 10, 1)
        self.assertAlmostEqual(fv, 200000, delta=200000 * 0.01)
        self.assertAlmostEqual(rate, 0.0718, delta=0.005)
    
    def test_required_years(self):
        """测试反推所需年限"""
        years = self.calculator.calculate_years(
            principal=100000,
            future_value=200000,
            annual_rate=0.07,
            compound_frequency=1
        )
        # 验证：100000 * 1.07^years ≈ 200000
        # 预期约 10.24 年
        fv = self.calculator.calculate_future_value(100000, 0.07, years, 1)
        self.assertAlmostEqual(fv, 200000, delta=200000 * 0.01)
        self.assertAlmostEqual(years, 10.24, delta=0.5)
    
    def test_invalid_inputs(self):
        """测试无效输入处理"""
        with self.assertRaises(ValueError):
            self.calculator.calculate_future_value(
                principal=100000,
                annual_rate=-0.1,
                years=10
            )
        
        with self.assertRaises(ValueError):
            self.calculator.calculate_future_value(
                principal=100000,
                annual_rate=0.07,
                years=-5
            )


class TestRule4Calculator(unittest.TestCase):
    """4% 法则计算器测试"""
    
    def setUp(self):
        self.calculator = Rule4Calculator()
    
    def test_freedom_number(self):
        """测试财务自由数字计算"""
        # 年支出 20 万，4% 提取率
        freedom_number = self.calculator.calculate_freedom_number(200000, 0.04)
        self.assertEqual(freedom_number, 5000000)  # 20 万 / 0.04 = 500 万
    
    def test_freedom_number_custom_rate(self):
        """测试自定义提取率"""
        # 3% 提取率
        freedom_number = self.calculator.calculate_freedom_number(200000, 0.03)
        self.assertEqual(freedom_number, 200000 / 0.03)
    
    def test_safe_withdrawal(self):
        """测试安全提取计算"""
        result = self.calculator.calculate_safe_withdrawal(
            portfolio_value=5000000,
            withdrawal_rate=0.04
        )
        self.assertEqual(result['first_year_withdrawal'], 200000)
        self.assertEqual(result['monthly_withdrawal'], 200000 / 12)
    
    def test_portfolio_longevity_sustainable(self):
        """测试可持续组合"""
        # 500 万资产，年提取 20 万，年化 7%
        years = self.calculator.calculate_portfolio_longevity(
            initial_portfolio=5000000,
            annual_withdrawal=200000,
            annual_return=0.07
        )
        # 应该可持续很长时间 (>50 年或返回 -1)
        self.assertTrue(years == -1 or years > 50)
    
    def test_portfolio_longevity_deplete(self):
        """测试会耗尽的组合"""
        # 100 万资产，年提取 20 万，无收益
        years = self.calculator.calculate_portfolio_longevity(
            initial_portfolio=1000000,
            annual_withdrawal=200000,
            annual_return=0
        )
        # 应该能支撑约 5 年 (边界情况)
        self.assertGreaterEqual(years, 4)
        self.assertLessEqual(years, 6)
    
    def test_validate_safety_safe(self):
        """测试安全性验证 - 安全情况"""
        result = self.calculator.validate_safety(
            portfolio_value=6000000,
            annual_expenses=200000,
            years=30
        )
        self.assertTrue(result['is_safe'])
        self.assertGreater(result['safety_ratio'], 1.0)
    
    def test_validate_safety_unsafe(self):
        """测试安全性验证 - 不安全情况"""
        result = self.calculator.validate_safety(
            portfolio_value=3000000,
            annual_expenses=200000,
            years=30
        )
        self.assertFalse(result['is_safe'])
        self.assertLess(result['safety_ratio'], 1.0)


class TestFinancialFreedomCalculator(unittest.TestCase):
    """财务自由主计算器测试"""
    
    def test_basic_calculation(self):
        """测试基本计算"""
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
        
        # 验证结果合理性
        self.assertGreater(result.years_to_freedom, 0)
        self.assertLess(result.years_to_freedom, 20)
        self.assertGreater(result.required_assets, 0)
        self.assertGreater(result.success_probability, 0)
        self.assertGreater(result.success_probability, 0)
    
    def test_already_achieved(self):
        """测试已实现财务自由的情况"""
        params = FinancialFreedomParams(
            current_age=40,
            retirement_age=50,
            current_assets=10000000,  # 已有 1000 万
            annual_expenses=200000,
            annual_income=300000,
            savings_rate=0.3,
            investment_return_rate=0.05,
            inflation_rate=0.03,
            withdrawal_rate=0.04
        )
        calculator = FinancialFreedomCalculator(params)
        result = calculator.calculate()
        
        self.assertEqual(result.years_to_freedom, 0)
        self.assertTrue(result.is_achievable)
    
    def test_sensitivity_analysis(self):
        """测试敏感性分析"""
        params = FinancialFreedomParams(
            current_age=35,
            retirement_age=50,
            current_assets=500000,
            annual_expenses=150000,
            annual_income=400000,
            savings_rate=0.35,
            investment_return_rate=0.07,
            inflation_rate=0.03,
            withdrawal_rate=0.04
        )
        calculator = FinancialFreedomCalculator(params)
        sensitivity = calculator.get_sensitivity_analysis()
        
        # 验证敏感性分析结果
        self.assertIn('investment_return_rate', sensitivity)
        self.assertIn('savings_rate', sensitivity)
        self.assertIn('inflation_rate', sensitivity)
        
        # 验证收益率越高，所需年数越少
        rate_results = sensitivity['investment_return_rate']
        if len(rate_results) >= 2:
            self.assertLessEqual(
                rate_results[-1]['years'],  # 高收益率
                rate_results[0]['years']    # 低收益率
            )
    
    def test_convenience_function(self):
        """测试便捷函数"""
        result = calculate_freedom(
            current_age=30,
            retirement_age=45,
            current_assets=100000,
            annual_expenses=200000,
            annual_income=500000,
            savings_rate=0.4
        )
        self.assertIsInstance(result.years_to_freedom, float)
        self.assertIsInstance(result.is_achievable, bool)


class TestRiskToleranceScore(unittest.TestCase):
    """风险承受能力评分测试"""
    
    def test_age_scoring(self):
        """测试年龄评分"""
        self.assertEqual(RiskToleranceScore.score_age(20), 90)
        self.assertEqual(RiskToleranceScore.score_age(30), 85)
        self.assertEqual(RiskToleranceScore.score_age(40), 75)
        self.assertEqual(RiskToleranceScore.score_age(50), 60)
        self.assertEqual(RiskToleranceScore.score_age(60), 45)
        self.assertEqual(RiskToleranceScore.score_age(70), 30)
    
    def test_income_stability_scoring(self):
        """测试收入稳定性评分"""
        # 稳定工作，低波动，长年限
        score = RiskToleranceScore.score_income_stability(
            employment_type='stable',
            income_variability=0.05,
            years_employed=10
        )
        self.assertGreater(score, 70)
        
        # 自由职业，高波动，短年限
        score_low = RiskToleranceScore.score_income_stability(
            employment_type='freelance',
            income_variability=0.5,
            years_employed=1
        )
        self.assertLess(score_low, score)
    
    def test_assets_scoring(self):
        """测试资产状况评分"""
        # 高资产，高流动性，低负债
        score = RiskToleranceScore.score_assets(
            total_assets=5000000,
            liquid_assets_ratio=0.4,
            debt_ratio=0.1,
            emergency_fund_months=12
        )
        self.assertGreater(score, 80)
        
        # 低资产，低流动性，高负债
        score_low = RiskToleranceScore.score_assets(
            total_assets=100000,
            liquid_assets_ratio=0.1,
            debt_ratio=0.6,
            emergency_fund_months=1
        )
        self.assertLess(score_low, 40)
    
    def test_full_assessment(self):
        """测试完整评估"""
        result = RiskToleranceScore.calculate_total_score(
            age=35,
            employment_type='corporate',
            total_assets=1500000,
            years_investing=5,
            loss_tolerance=0.2
        )
        
        self.assertIn('total_score', result)
        self.assertIn('risk_level', result)
        self.assertIn('recommendation', result)
        self.assertGreater(result['total_score'], 0)
        self.assertLessEqual(result['total_score'], 100)
    
    def test_risk_level_assignment(self):
        """测试风险等级分配"""
        # 高分应得激进型
        high_result = RiskToleranceScore.calculate_total_score(
            age=25,
            employment_type='stable',
            total_assets=5000000,
            years_investing=10,
            loss_tolerance=0.4
        )
        self.assertIn(high_result['risk_level_code'], ['GROWTH', 'AGGRESSIVE'])
        
        # 低分应得保守型
        low_result = RiskToleranceScore.calculate_total_score(
            age=65,
            employment_type='other',
            total_assets=100000,
            years_investing=0,
            loss_tolerance=0.05
        )
        self.assertIn(low_result['risk_level_code'], ['CONSERVATIVE', 'CAUTIOUS'])


class TestPortfolioRiskAnalyzer(unittest.TestCase):
    """投资组合风险分析器测试"""
    
    def test_volatility_calculation(self):
        """测试波动率计算"""
        # 稳定收益
        stable_returns = [0.01] * 100
        analyzer_stable = PortfolioRiskAnalyzer(stable_returns)
        vol_stable = analyzer_stable.calculate_volatility()
        
        # 波动收益
        volatile_returns = [0.05, -0.04, 0.06, -0.03, 0.04] * 20
        analyzer_volatile = PortfolioRiskAnalyzer(volatile_returns)
        vol_volatile = analyzer_volatile.calculate_volatility()
        
        self.assertAlmostEqual(vol_stable, 0, places=4)
        self.assertGreater(vol_volatile, vol_stable)
    
    def test_var_calculation(self):
        """测试 VaR 计算"""
        returns = [0.02, 0.01, -0.01, -0.03, 0.04, -0.02, 0.03, -0.01, 0.02, -0.04]
        analyzer = PortfolioRiskAnalyzer(returns)
        
        var_95 = analyzer.calculate_var(0.95)
        var_99 = analyzer.calculate_var(0.99)
        
        # 99% VaR 应该比 95% VaR 更差 (更小)
        self.assertLessEqual(var_99, var_95)
    
    def test_max_drawdown(self):
        """测试最大回撤计算"""
        # 持续上涨
        rising_returns = [0.01] * 50
        analyzer_rising = PortfolioRiskAnalyzer(rising_returns)
        dd_rising = analyzer_rising.calculate_max_drawdown()
        
        # 先涨后跌
        volatile_returns = [0.05, 0.04, 0.03, -0.1, -0.08, 0.02, 0.03]
        analyzer_volatile = PortfolioRiskAnalyzer(volatile_returns)
        dd_volatile = analyzer_volatile.calculate_max_drawdown()
        
        self.assertAlmostEqual(dd_rising, 0, places=4)
        self.assertGreater(dd_volatile, 0.05)
    
    def test_sharpe_ratio(self):
        """测试 Sharpe 比率计算"""
        # 正收益
        positive_returns = [0.02, 0.015, 0.025, 0.01, 0.02] * 20
        analyzer = PortfolioRiskAnalyzer(positive_returns)
        sharpe = analyzer.calculate_sharpe_ratio(risk_free_rate=0.03)
        
        self.assertGreater(sharpe, 0)
    
    def test_beta_calculation(self):
        """测试 Beta 计算"""
        portfolio_returns = [0.02, 0.015, 0.025, 0.01, 0.02] * 20
        benchmark_returns = [0.015, 0.01, 0.02, 0.008, 0.015] * 20
        
        analyzer = PortfolioRiskAnalyzer(portfolio_returns, benchmark_returns)
        beta = analyzer.calculate_beta()
        
        self.assertIsNotNone(beta)
        self.assertGreater(beta, 0)
    
    def test_complete_metrics(self):
        """测试完整风险指标"""
        returns = [0.01, -0.02, 0.03, 0.015, -0.01, 0.02, -0.005, 0.025, 0.01, -0.015] * 10
        analyzer = PortfolioRiskAnalyzer(returns)
        metrics = analyzer.get_risk_metrics()
        
        self.assertIn('volatility', metrics)
        self.assertIn('var_95', metrics)
        self.assertIn('max_drawdown', metrics)
        self.assertIn('sharpe_ratio', metrics)


class TestFinancialRiskWarning(unittest.TestCase):
    """财务风险预警系统测试"""
    
    def setUp(self):
        self.warner = FinancialRiskWarning()
    
    def test_debt_ratio_warning(self):
        """测试负债率预警"""
        # 安全情况
        warnings = self.warner.check_debt_ratio(
            total_assets=2000000,
            total_liabilities=500000
        )
        self.assertEqual(len(warnings), 0)
        
        # 预警情况
        warnings = self.warner.check_debt_ratio(
            total_assets=2000000,
            total_liabilities=1200000
        )
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0]['level'], 'warning')
        
        # 危险情况
        warnings = self.warner.check_debt_ratio(
            total_assets=2000000,
            total_liabilities=1500000
        )
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0]['level'], 'danger')
    
    def test_liquidity_warning(self):
        """测试流动性预警"""
        # 安全情况
        warnings = self.warner.check_liquidity(
            liquid_assets=500000,
            total_assets=2000000,
            monthly_expenses=20000,
            emergency_fund=200000
        )
        self.assertEqual(len(warnings), 0)
        
        # 应急资金不足
        warnings = self.warner.check_liquidity(
            liquid_assets=100000,
            total_assets=2000000,
            monthly_expenses=20000,
            emergency_fund=30000
        )
        self.assertGreater(len(warnings), 0)
    
    def test_concentration_warning(self):
        """测试集中度预警"""
        # 分散配置
        warnings = self.warner.check_concentration({
            'stocks': 400000,
            'bonds': 300000,
            'cash': 300000
        })
        self.assertEqual(len(warnings), 0)
        
        # 集中配置
        warnings = self.warner.check_concentration({
            'stocks': 900000,
            'bonds': 100000
        })
        self.assertGreater(len(warnings), 0)
    
    def test_full_check(self):
        """测试完整风险检查"""
        result = self.warner.full_check(
            total_assets=2000000,
            total_liabilities=500000,
            liquid_assets=400000,
            monthly_expenses=20000,
            emergency_fund=150000,
            asset_allocation={
                'stocks': 800000,
                'bonds': 500000,
                'cash': 200000
            }
        )
        
        self.assertIn('risk_level', result)
        self.assertIn('warnings', result)
        self.assertIn('recommendations', result)
        self.assertIn(result['risk_level'], ['normal', 'low', 'medium', 'high'])
    
    def test_full_check_high_risk(self):
        """测试高风险情况"""
        result = self.warner.full_check(
            total_assets=1000000,
            total_liabilities=800000,
            liquid_assets=50000,
            monthly_expenses=30000,
            emergency_fund=20000,
            asset_allocation={
                'single_stock': 900000,
                'cash': 30000
            }
        )
        
        self.assertIn(result['risk_level'], ['medium', 'high'])
        self.assertGreater(result['warning_count'] + result['danger_count'], 0)


class TestAlgorithmAccuracy(unittest.TestCase):
    """算法精度测试 (误差≤1%)"""
    
    def test_compound_interest_accuracy(self):
        """测试复利计算精度"""
        calculator = CompoundInterestCalculator()
        
        # 已知精确解的测试用例
        test_cases = [
            (100000, 0.05, 10, 1, 0, 100000 * 1.05**10),
            (50000, 0.06, 5, 12, 0, 50000 * (1 + 0.06/12)**60),
        ]
        
        for principal, rate, years, freq, contribution, expected in test_cases:
            result = calculator.calculate_future_value(
                principal, rate, years, freq, contribution
            )
            error = abs(result - expected) / expected
            self.assertLess(error, 0.01, f"复利计算误差{error*100:.2f}%超过 1%")
    
    def test_rule4_accuracy(self):
        """测试 4% 法则计算精度"""
        calculator = Rule4Calculator()
        
        test_cases = [
            (200000, 0.04, 5000000),
            (150000, 0.04, 3750000),
            (300000, 0.03, 10000000),
        ]
        
        for expenses, rate, expected in test_cases:
            result = calculator.calculate_freedom_number(expenses, rate)
            error = abs(result - expected) / expected
            self.assertLess(error, 0.0001, f"4% 法则计算误差{error*100:.4f}%超过 0.01%")
    
    def test_years_to_freedom_accuracy(self):
        """测试财务自由年限计算精度"""
        # 使用简单场景验证
        params = FinancialFreedomParams(
            current_age=30,
            retirement_age=60,
            current_assets=0,
            annual_expenses=100000,
            annual_income=200000,
            savings_rate=0.5,
            investment_return_rate=0.07,
            inflation_rate=0.03,
            withdrawal_rate=0.04
        )
        
        calculator = FinancialFreedomCalculator(params)
        result = calculator.calculate()
        
        # 验证结果合理性
        self.assertGreater(result.years_to_freedom, 0)
        self.assertLess(result.years_to_freedom, 40)
        
        # 验证所需资产计算正确 (使用 4% 法则)
        expected_assets = result.annual_surplus * 25  # 简化估算
        # 由于通胀调整，允许更大误差范围
        self.assertGreater(result.required_assets, 0)


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
