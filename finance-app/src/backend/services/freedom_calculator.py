"""
财务自由计算核心算法模块

包含：
1. 财务自由计算核心算法
2. 4% 法则计算器
3. 复利计算模型

算法要求：
- 误差≤1%
- 支持动态调整
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import math


@dataclass
class FinancialFreedomParams:
    """财务自由计算参数"""
    current_age: int  # 当前年龄
    retirement_age: int  # 目标退休年龄
    current_assets: float  # 当前资产
    annual_expenses: float  # 年支出
    annual_income: float  # 年收入
    savings_rate: float  # 储蓄率 (0-1)
    investment_return_rate: float  # 投资年化收益率 (0-1)
    inflation_rate: float  # 通货膨胀率 (0-1)
    withdrawal_rate: float  # 提取率 (0-1), 默认 4%
    life_expectancy: int = 85  # 预期寿命


@dataclass
class FreedomResult:
    """财务自由计算结果"""
    years_to_freedom: float  # 达到财务自由所需年数
    freedom_age: float  # 财务自由时的年龄
    required_assets: float  # 所需资产总额
    projected_assets: float  # 预测资产总额
    success_probability: float  # 成功概率 (0-1)
    is_achievable: bool  # 是否可实现
    annual_surplus: float  # 年结余
    monthly_savings: float  # 月储蓄额


class CompoundInterestCalculator:
    """复利计算器"""
    
    @staticmethod
    def calculate_future_value(
        principal: float,
        annual_rate: float,
        years: int,
        compound_frequency: int = 12,
        monthly_contribution: float = 0
    ) -> float:
        """
        计算复利终值
        
        Args:
            principal: 本金
            annual_rate: 年化收益率
            years: 投资年限
            compound_frequency: 复利频率 (1=年，4=季，12=月)
            monthly_contribution: 每月定投金额
            
        Returns:
            终值
        """
        if annual_rate < 0:
            raise ValueError("年化收益率不能为负")
        if years < 0:
            raise ValueError("投资年限不能为负")
            
        periodic_rate = annual_rate / compound_frequency
        total_periods = years * compound_frequency
        
        # 本金复利部分
        fv_principal = principal * (1 + periodic_rate) ** total_periods
        
        # 定投部分 (期末年金)
        if monthly_contribution > 0:
            # 将月定投转换为对应复利频率的定投
            contribution_per_period = monthly_contribution * (compound_frequency / 12)
            if periodic_rate > 0:
                fv_contribution = contribution_per_period * (
                    ((1 + periodic_rate) ** total_periods - 1) / periodic_rate
                )
            else:
                fv_contribution = contribution_per_period * total_periods
        else:
            fv_contribution = 0
            
        return fv_principal + fv_contribution
    
    @staticmethod
    def calculate_required_principal(
        future_value: float,
        annual_rate: float,
        years: int,
        compound_frequency: int = 12,
        monthly_contribution: float = 0
    ) -> float:
        """
        计算达到目标终值所需的本金
        
        Returns:
            所需本金
        """
        periodic_rate = annual_rate / compound_frequency
        total_periods = years * compound_frequency
        
        # 计算定投部分的终值
        if monthly_contribution > 0 and periodic_rate > 0:
            contribution_per_period = monthly_contribution * (compound_frequency / 12)
            fv_contribution = contribution_per_period * (
                ((1 + periodic_rate) ** total_periods - 1) / periodic_rate
            )
        else:
            fv_contribution = 0
            
        # 反推所需本金
        remaining_fv = future_value - fv_contribution
        if remaining_fv <= 0:
            return 0
            
        required_principal = remaining_fv / ((1 + periodic_rate) ** total_periods)
        return max(0, required_principal)
    
    @staticmethod
    def calculate_required_rate(
        principal: float,
        future_value: float,
        years: int,
        compound_frequency: int = 12,
        monthly_contribution: float = 0,
        tolerance: float = 0.0001
    ) -> float:
        """
        使用二分法计算达到目标所需的年化收益率
        
        Returns:
            所需年化收益率
        """
        if years <= 0:
            return 0
            
        # 二分法搜索
        low, high = -0.5, 0.5  # -50% 到 50%
        
        for _ in range(100):  # 最多迭代 100 次
            mid = (low + high) / 2
            fv = CompoundInterestCalculator.calculate_future_value(
                principal, mid, years, compound_frequency, monthly_contribution
            )
            
            if abs(fv - future_value) / future_value < tolerance:
                return mid
                
            if fv < future_value:
                low = mid
            else:
                high = mid
                
        return mid
    
    @staticmethod
    def calculate_years(
        principal: float,
        future_value: float,
        annual_rate: float,
        compound_frequency: int = 12,
        monthly_contribution: float = 0,
        tolerance: float = 0.0001
    ) -> float:
        """
        计算达到目标所需的年限
        """
        if annual_rate <= 0 and monthly_contribution <= 0:
            return float('inf')
            
        # 使用牛顿法或二分法
        low, high = 0.1, 100  # 0.1 年到 100 年
        
        for _ in range(100):
            mid = (low + high) / 2
            fv = CompoundInterestCalculator.calculate_future_value(
                principal, annual_rate, mid, compound_frequency, monthly_contribution
            )
            
            if abs(fv - future_value) / future_value < tolerance:
                return mid
                
            if fv < future_value:
                low = mid
            else:
                high = mid
                
        return mid


class Rule4Calculator:
    """4% 法则计算器"""
    
    @staticmethod
    def calculate_freedom_number(
        annual_expenses: float,
        withdrawal_rate: float = 0.04
    ) -> float:
        """
        计算财务自由所需资产总额 (FIRE 数字)
        
        公式：FIRE 数字 = 年支出 / 提取率
        默认 4% 提取率下：FIRE 数字 = 年支出 × 25
        """
        if withdrawal_rate <= 0:
            raise ValueError("提取率必须大于 0")
        return annual_expenses / withdrawal_rate
    
    @staticmethod
    def calculate_safe_withdrawal(
        portfolio_value: float,
        withdrawal_rate: float = 0.04,
        inflation_rate: float = 0.03
    ) -> Dict[str, float]:
        """
        计算安全提取金额
        
        Returns:
            包含首年提取额、经通胀调整的提取额等信息
        """
        first_year_withdrawal = portfolio_value * withdrawal_rate
        
        return {
            'portfolio_value': portfolio_value,
            'withdrawal_rate': withdrawal_rate,
            'first_year_withdrawal': first_year_withdrawal,
            'monthly_withdrawal': first_year_withdrawal / 12,
            'inflation_adjusted_rate': max(0, withdrawal_rate - inflation_rate),
            'real_return_rate': inflation_rate  # 实际购买力增长率
        }
    
    @staticmethod
    def calculate_portfolio_longevity(
        initial_portfolio: float,
        annual_withdrawal: float,
        annual_return: float,
        inflation_rate: float = 0.03,
        withdrawal_growth: bool = True
    ) -> int:
        """
        计算资产组合能支撑多少年
        
        Args:
            initial_portfolio: 初始资产
            annual_withdrawal: 首年提取额
            annual_return: 年化收益率
            inflation_rate: 通胀率
            withdrawal_growth: 提取额是否随通胀增长
            
        Returns:
            资产耗尽前的年数，-1 表示永久可持续
        """
        portfolio = initial_portfolio
        withdrawal = annual_withdrawal
        
        for year in range(1, 101):  # 最多计算 100 年
            # 年初提取
            portfolio -= withdrawal
            if portfolio <= 0:
                return year - 1
                
            # 年末收益
            portfolio *= (1 + annual_return)
            
            # 下一年提取额随通胀增长
            if withdrawal_growth:
                withdrawal *= (1 + inflation_rate)
                
        return -1  # 100 年后仍未耗尽
    
    @staticmethod
    def validate_safety(
        portfolio_value: float,
        annual_expenses: float,
        years: int = 30,
        success_threshold: float = 0.95
    ) -> Dict[str, any]:
        """
        验证 4% 法则的安全性
        
        Returns:
            安全性评估结果
        """
        freedom_number = Rule4Calculator.calculate_freedom_number(annual_expenses)
        safety_ratio = portfolio_value / freedom_number
        
        # 简单蒙特卡洛模拟 (1000 次)
        import random
        success_count = 0
        
        for _ in range(1000):
            portfolio = portfolio_value
            withdrawal = annual_expenses
            
            for year in range(years):
                # 随机收益率 (假设正态分布，均值 7%, 标准差 15%)
                annual_return = random.gauss(0.07, 0.15)
                portfolio = (portfolio - withdrawal) * (1 + annual_return)
                withdrawal *= 1.03  # 通胀调整
                
                if portfolio <= 0:
                    break
            else:
                success_count += 1
        
        success_rate = success_count / 1000
        
        return {
            'freedom_number': freedom_number,
            'safety_ratio': safety_ratio,
            'is_safe': safety_ratio >= 1.0,
            'success_rate': success_rate,
            'meets_threshold': success_rate >= success_threshold,
            'recommended_portfolio': freedom_number * (1 if safety_ratio >= 1 else 1.2)
        }


class FinancialFreedomCalculator:
    """财务自由主计算器"""
    
    def __init__(self, params: FinancialFreedomParams):
        self.params = params
        self.ci_calculator = CompoundInterestCalculator()
        self.rule4_calculator = Rule4Calculator()
    
    def calculate_annual_surplus(self) -> float:
        """计算年结余"""
        return self.params.annual_income * self.params.savings_rate
    
    def calculate_required_assets(self) -> float:
        """计算所需资产总额 (考虑通胀)"""
        # 计算退休时的年支出 (经通胀调整)
        years_to_retirement = self.params.retirement_age - self.params.current_age
        future_expenses = self.params.annual_expenses * (
            (1 + self.params.inflation_rate) ** years_to_retirement
        )
        
        # 使用 4% 法则计算所需资产
        required_assets = self.rule4_calculator.calculate_freedom_number(
            future_expenses,
            self.params.withdrawal_rate
        )
        
        return required_assets
    
    def calculate_years_to_freedom(self) -> float:
        """
        计算达到财务自由所需年数
        
        使用迭代法精确计算
        """
        current_assets = self.params.current_assets
        annual_savings = self.params.annual_income * self.params.savings_rate
        monthly_savings = annual_savings / 12
        
        # 计算目标资产 (当前币值)
        target_assets = self.calculate_required_assets()
        
        # 如果已经达到财务自由
        if current_assets >= target_assets:
            return 0
        
        # 使用二分法计算所需年数
        low, high = 0.1, 50  # 0.1 年到 50 年
        tolerance = 0.001  # 精度要求
        
        for _ in range(100):
            mid = (low + high) / 2
            
            # 计算 mid 年后的资产
            future_assets = self.ci_calculator.calculate_future_value(
                principal=current_assets,
                annual_rate=self.params.investment_return_rate,
                years=mid,
                compound_frequency=12,
                monthly_contribution=monthly_savings
            )
            
            # 计算 mid 年后的目标资产 (经通胀调整)
            future_target = self.params.annual_expenses * (
                (1 + self.params.inflation_rate) ** mid
            ) / self.params.withdrawal_rate
            
            relative_error = abs(future_assets - future_target) / future_target
            
            if relative_error < tolerance:
                return mid
                
            if future_assets < future_target:
                low = mid
            else:
                high = mid
        
        return mid
    
    def calculate_success_probability(
        self,
        simulations: int = 1000
    ) -> float:
        """
        使用蒙特卡洛模拟计算成功概率
        """
        import random
        
        years_to_freedom = self.calculate_years_to_freedom()
        target_assets = self.calculate_required_assets()
        
        success_count = 0
        
        for _ in range(simulations):
            assets = self.params.current_assets
            annual_savings = self.params.annual_income * self.params.savings_rate
            
            for year in range(int(math.ceil(years_to_freedom))):
                # 随机收益率
                annual_return = random.gauss(
                    self.params.investment_return_rate,
                    self.params.investment_return_rate * 0.3  # 30% 波动
                )
                
                assets = assets * (1 + annual_return) + annual_savings
            
            if assets >= target_assets:
                success_count += 1
        
        return success_count / simulations
    
    def calculate(self) -> FreedomResult:
        """执行完整计算"""
        years_to_freedom = self.calculate_years_to_freedom()
        freedom_age = self.params.current_age + years_to_freedom
        required_assets = self.calculate_required_assets()
        
        # 计算预测资产
        annual_savings = self.params.annual_income * self.params.savings_rate
        projected_assets = self.ci_calculator.calculate_future_value(
            principal=self.params.current_assets,
            annual_rate=self.params.investment_return_rate,
            years=years_to_freedom,
            compound_frequency=12,
            monthly_contribution=annual_savings / 12
        )
        
        success_prob = self.calculate_success_probability()
        
        # 判断是否可实现
        is_achievable = (
            years_to_freedom <= (self.params.retirement_age - self.params.current_age) and
            years_to_freedom <= 50 and
            success_prob >= 0.5
        )
        
        return FreedomResult(
            years_to_freedom=round(years_to_freedom, 2),
            freedom_age=round(freedom_age, 2),
            required_assets=round(required_assets, 2),
            projected_assets=round(projected_assets, 2),
            success_probability=round(success_prob, 4),
            is_achievable=is_achievable,
            annual_surplus=round(annual_savings, 2),
            monthly_savings=round(annual_savings / 12, 2)
        )
    
    def get_sensitivity_analysis(self) -> Dict[str, List[Dict]]:
        """
        敏感性分析：分析各参数对结果的影响
        """
        base_result = self.calculate()
        
        sensitivity = {
            'investment_return_rate': [],
            'savings_rate': [],
            'inflation_rate': []
        }
        
        # 投资收益率敏感性
        for delta in [-0.03, -0.02, -0.01, 0, 0.01, 0.02, 0.03]:
            new_params = FinancialFreedomParams(
                **{**self.params.__dict__, 'investment_return_rate': self.params.investment_return_rate + delta}
            )
            if new_params.investment_return_rate >= 0:
                result = FinancialFreedomCalculator(new_params).calculate()
                sensitivity['investment_return_rate'].append({
                    'rate': new_params.investment_return_rate,
                    'years': result.years_to_freedom
                })
        
        # 储蓄率敏感性
        for delta in [-0.1, -0.05, 0, 0.05, 0.1]:
            new_rate = max(0.01, min(0.9, self.params.savings_rate + delta))
            new_params = FinancialFreedomParams(
                **{**self.params.__dict__, 'savings_rate': new_rate}
            )
            result = FinancialFreedomCalculator(new_params).calculate()
            sensitivity['savings_rate'].append({
                'rate': new_rate,
                'years': result.years_to_freedom
            })
        
        # 通胀率敏感性
        for delta in [-0.02, -0.01, 0, 0.01, 0.02]:
            new_rate = max(0, self.params.inflation_rate + delta)
            new_params = FinancialFreedomParams(
                **{**self.params.__dict__, 'inflation_rate': new_rate}
            )
            result = FinancialFreedomCalculator(new_params).calculate()
            sensitivity['inflation_rate'].append({
                'rate': new_rate,
                'years': result.years_to_freedom
            })
        
        return sensitivity


# 便捷函数
def calculate_freedom(
    current_age: int,
    retirement_age: int,
    current_assets: float,
    annual_expenses: float,
    annual_income: float,
    savings_rate: float,
    investment_return_rate: float = 0.07,
    inflation_rate: float = 0.03,
    withdrawal_rate: float = 0.04
) -> FreedomResult:
    """
    便捷函数：计算财务自由
    
    示例:
        result = calculate_freedom(
            current_age=30,
            retirement_age=45,
            current_assets=100000,
            annual_expenses=200000,
            annual_income=500000,
            savings_rate=0.4,
            investment_return_rate=0.07
        )
        print(f"{result.years_to_freedom}年后实现财务自由")
    """
    params = FinancialFreedomParams(
        current_age=current_age,
        retirement_age=retirement_age,
        current_assets=current_assets,
        annual_expenses=annual_expenses,
        annual_income=annual_income,
        savings_rate=savings_rate,
        investment_return_rate=investment_return_rate,
        inflation_rate=inflation_rate,
        withdrawal_rate=withdrawal_rate
    )
    calculator = FinancialFreedomCalculator(params)
    return calculator.calculate()


if __name__ == '__main__':
    # 示例使用
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
    
    print(f"财务自由计算结果:")
    print(f"  所需年数：{result.years_to_freedom}年")
    print(f"  自由年龄：{result.freedom_age}岁")
    print(f"  所需资产：¥{result.required_assets:,.2f}")
    print(f"  成功概率：{result.success_probability*100:.1f}%")
    print(f"  是否可实现：{'是' if result.is_achievable else '否'}")
