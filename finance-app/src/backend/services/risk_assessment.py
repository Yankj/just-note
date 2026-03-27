"""
风险评估模型模块

包含：
1. 投资者风险承受能力评估
2. 投资组合风险评估
3. 财务风险预警系统

算法要求：
- 误差≤1%
- 支持动态调整
- 有完整单元测试
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import math


class RiskLevel(Enum):
    """风险等级"""
    CONSERVATIVE = "保守型"  # R1
    CAUTIOUS = "谨慎型"  # R2
    BALANCED = "稳健型"  # R3
    GROWTH = "成长型"  # R4
    AGGRESSIVE = "激进型"  # R5


class RiskToleranceScore:
    """
    风险承受能力评分系统
    
    基于以下维度评估：
    1. 年龄因素
    2. 收入稳定性
    3. 资产状况
    4. 投资经验
    5. 风险态度
    6. 财务目标
    """
    
    # 各维度权重
    WEIGHTS = {
        'age': 0.15,
        'income_stability': 0.20,
        'assets': 0.20,
        'experience': 0.15,
        'attitude': 0.20,
        'goals': 0.10
    }
    
    @staticmethod
    def score_age(age: int) -> float:
        """
        年龄评分 (0-100)
        年轻人风险承受能力更强
        """
        if age < 25:
            return 90
        elif age < 35:
            return 85
        elif age < 45:
            return 75
        elif age < 55:
            return 60
        elif age < 65:
            return 45
        else:
            return 30
    
    @staticmethod
    def score_income_stability(
        employment_type: str,
        income_variability: float,
        years_employed: int
    ) -> float:
        """
        收入稳定性评分 (0-100)
        
        Args:
            employment_type: 就业类型 (stable/freelance/business/other)
            income_variability: 收入波动率 (0-1)
            years_employed: 从业年限
        """
        # 就业类型基础分
        type_scores = {
            'stable': 80,      # 公务员、事业单位、大型国企
            'corporate': 70,   # 大型企业
            'smc': 60,         # 中小企业
            'freelance': 50,   # 自由职业
            'business': 55,    # 企业主
            'other': 45
        }
        base_score = type_scores.get(employment_type, 50)
        
        # 收入波动率调整
        volatility_penalty = income_variability * 30
        
        # 从业年限加分
        tenure_bonus = min(20, years_employed * 2)
        
        return max(0, min(100, base_score - volatility_penalty + tenure_bonus))
    
    @staticmethod
    def score_assets(
        total_assets: float,
        liquid_assets_ratio: float,
        debt_ratio: float,
        emergency_fund_months: float
    ) -> float:
        """
        资产状况评分 (0-100)
        
        Args:
            total_assets: 总资产
            liquid_assets_ratio: 流动资产占比 (0-1)
            debt_ratio: 负债率 (0-1)
            emergency_fund_months: 应急资金覆盖月数
        """
        # 资产规模评分 (对数尺度)
        if total_assets < 100000:
            asset_score = 30
        elif total_assets < 500000:
            asset_score = 50
        elif total_assets < 1000000:
            asset_score = 65
        elif total_assets < 5000000:
            asset_score = 80
        else:
            asset_score = 95
        
        # 流动性调整
        liquidity_bonus = (liquid_assets_ratio - 0.2) * 20
        
        # 负债率惩罚
        debt_penalty = debt_ratio * 40
        
        # 应急资金加分
        emergency_bonus = min(15, emergency_fund_months * 3)
        
        return max(0, min(100, asset_score + liquidity_bonus - debt_penalty + emergency_bonus))
    
    @staticmethod
    def score_experience(
        years_investing: int,
        product_types: int,
        has_losses: bool,
        education_level: str
    ) -> float:
        """
        投资经验评分 (0-100)
        
        Args:
            years_investing: 投资年限
            product_types: 投资过的产品类型数
            has_losses: 是否有过亏损经历
            education_level: 教育水平
        """
        # 投资年限
        experience_score = min(50, years_investing * 10)
        
        # 产品多样性
        diversity_bonus = min(20, product_types * 5)
        
        # 亏损经历 (有经验但谨慎)
        loss_adjustment = 5 if has_losses else 0
        
        # 教育水平
        edu_scores = {
            'high_school': 0,
            'bachelor': 10,
            'master': 15,
            'phd': 20,
            'finance_related': 25
        }
        edu_bonus = edu_scores.get(education_level, 5)
        
        return min(100, experience_score + diversity_bonus + loss_adjustment + edu_bonus)
    
    @staticmethod
    def score_attitude(
        loss_tolerance: float,
        return_expectation: float,
        sleep_factor: float
    ) -> float:
        """
        风险态度评分 (0-100)
        
        Args:
            loss_tolerance: 可承受最大亏损比例 (0-1)
            return_expectation: 期望年化收益率
            sleep_factor: 投资对睡眠影响程度 (0-1, 0=不影响，1=严重失眠)
        """
        # 亏损承受力
        loss_score = loss_tolerance * 100
        
        # 收益期望合理性 (5-15% 为合理)
        if 0.05 <= return_expectation <= 0.15:
            expectation_score = 80
        elif return_expectation < 0.05:
            expectation_score = 60
        elif return_expectation < 0.25:
            expectation_score = 70
        else:
            expectation_score = 40  # 期望过高
        
        # 睡眠因子
        sleep_penalty = sleep_factor * 30
        
        return max(0, min(100, (loss_score + expectation_score) / 2 - sleep_penalty))
    
    @staticmethod
    def score_goals(
        investment_horizon: int,
        goal_importance: float,
        goal_flexibility: float
    ) -> float:
        """
        财务目标评分 (0-100)
        
        Args:
            investment_horizon: 投资期限 (年)
            goal_importance: 目标重要性 (0-1)
            goal_flexibility: 目标灵活性 (0-1)
        """
        # 投资期限 (越长风险承受能力越强)
        if investment_horizon >= 10:
            horizon_score = 90
        elif investment_horizon >= 5:
            horizon_score = 70
        elif investment_horizon >= 3:
            horizon_score = 50
        else:
            horizon_score = 30
        
        # 重要性调整 (越重要越保守)
        importance_adjustment = (1 - goal_importance) * 20
        
        # 灵活性加分
        flexibility_bonus = goal_flexibility * 20
        
        return min(100, horizon_score + importance_adjustment + flexibility_bonus)
    
    @classmethod
    def calculate_total_score(cls, **kwargs) -> Dict[str, any]:
        """
        计算综合风险承受评分
        
        Returns:
            包含总分、等级、各维度得分等信息
        """
        scores = {
            'age': cls.score_age(kwargs.get('age', 35)),
            'income_stability': cls.score_income_stability(
                kwargs.get('employment_type', 'corporate'),
                kwargs.get('income_variability', 0.1),
                kwargs.get('years_employed', 5)
            ),
            'assets': cls.score_assets(
                kwargs.get('total_assets', 500000),
                kwargs.get('liquid_assets_ratio', 0.3),
                kwargs.get('debt_ratio', 0.3),
                kwargs.get('emergency_fund_months', 6)
            ),
            'experience': cls.score_experience(
                kwargs.get('years_investing', 3),
                kwargs.get('product_types', 3),
                kwargs.get('has_losses', False),
                kwargs.get('education_level', 'bachelor')
            ),
            'attitude': cls.score_attitude(
                kwargs.get('loss_tolerance', 0.2),
                kwargs.get('return_expectation', 0.08),
                kwargs.get('sleep_factor', 0.2)
            ),
            'goals': cls.score_goals(
                kwargs.get('investment_horizon', 5),
                kwargs.get('goal_importance', 0.7),
                kwargs.get('goal_flexibility', 0.5)
            )
        }
        
        # 加权总分
        total_score = sum(
            scores[dim] * cls.WEIGHTS[dim]
            for dim in scores.keys()
        )
        
        # 确定风险等级
        if total_score >= 80:
            risk_level = RiskLevel.AGGRESSIVE
        elif total_score >= 65:
            risk_level = RiskLevel.GROWTH
        elif total_score >= 50:
            risk_level = RiskLevel.BALANCED
        elif total_score >= 35:
            risk_level = RiskLevel.CAUTIOUS
        else:
            risk_level = RiskLevel.CONSERVATIVE
        
        return {
            'total_score': round(total_score, 2),
            'risk_level': risk_level.value,
            'risk_level_code': risk_level.name,
            'dimension_scores': scores,
            'weights': cls.WEIGHTS,
            'recommendation': cls._get_recommendation(risk_level)
        }
    
    @staticmethod
    def _get_recommendation(level: RiskLevel) -> str:
        """获取投资建议"""
        recommendations = {
            RiskLevel.CONSERVATIVE: "建议配置 80% 以上资产于低风险产品（货币基金、国债、银行存款），20% 以内可尝试稳健理财。",
            RiskLevel.CAUTIOUS: "建议配置 60-70% 于固定收益类产品，30-40% 可配置平衡型基金或蓝筹股。",
            RiskLevel.BALANCED: "建议股债平衡配置，50% 权益类 +50% 固收类，可适度参与行业基金。",
            RiskLevel.GROWTH: "建议 70% 配置权益类资产（股票、股票基金），30% 固收类作为安全垫。",
            RiskLevel.AGGRESSIVE: "可高比例配置成长型资产，但建议保留 10-20% 流动性资产应对波动。"
        }
        return recommendations.get(level, "")


class PortfolioRiskAnalyzer:
    """
    投资组合风险分析器
    
    计算指标：
    - 波动率 (标准差)
    - VaR (风险价值)
    - 最大回撤
    - Sharpe 比率
    - Beta 系数
    """
    
    def __init__(self, returns: List[float], benchmark_returns: Optional[List[float]] = None):
        """
        Args:
            returns: 收益率序列 (日收益率或月收益率)
            benchmark_returns: 基准收益率序列 (用于计算 Beta)
        """
        self.returns = returns
        self.benchmark_returns = benchmark_returns
        self.n = len(returns)
    
    def calculate_volatility(self, annualization_factor: int = 252) -> float:
        """
        计算年化波动率
        
        Args:
            annualization_factor: 年化因子 (252=交易日，12=月)
        """
        if self.n < 2:
            return 0.0
            
        mean_return = sum(self.returns) / self.n
        variance = sum((r - mean_return) ** 2 for r in self.returns) / (self.n - 1)
        std_dev = math.sqrt(variance)
        
        return std_dev * math.sqrt(annualization_factor)
    
    def calculate_var(self, confidence_level: float = 0.95) -> float:
        """
        计算 VaR (Value at Risk)
        
        使用历史模拟法
        
        Args:
            confidence_level: 置信水平 (0.95 或 0.99)
            
        Returns:
            VaR 值 (负数表示损失)
        """
        if self.n < 10:
            return 0.0
            
        sorted_returns = sorted(self.returns)
        index = int((1 - confidence_level) * self.n)
        
        return sorted_returns[max(0, index)]
    
    def calculate_cvar(self, confidence_level: float = 0.95) -> float:
        """
        计算条件 VaR (CVaR / Expected Shortfall)
        
        超过 VaR 阈值的平均损失
        """
        if self.n < 10:
            return 0.0
            
        var = self.calculate_var(confidence_level)
        tail_returns = [r for r in self.returns if r <= var]
        
        if not tail_returns:
            return var
            
        return sum(tail_returns) / len(tail_returns)
    
    def calculate_max_drawdown(self) -> float:
        """
        计算最大回撤
        """
        if self.n < 2:
            return 0.0
            
        # 计算累计收益
        cumulative = [1.0]
        for r in self.returns:
            cumulative.append(cumulative[-1] * (1 + r))
        
        max_drawdown = 0
        peak = cumulative[0]
        
        for value in cumulative:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            max_drawdown = max(max_drawdown, drawdown)
        
        return max_drawdown
    
    def calculate_sharpe_ratio(self, risk_free_rate: float = 0.03, annualization_factor: int = 252) -> float:
        """
        计算 Sharpe 比率
        
        Args:
            risk_free_rate: 无风险利率 (年化)
            annualization_factor: 年化因子
        """
        if self.n < 2:
            return 0.0
            
        mean_return = sum(self.returns) / self.n
        annualized_return = mean_return * annualization_factor
        volatility = self.calculate_volatility(annualization_factor)
        
        if volatility == 0:
            return 0.0
            
        return (annualized_return - risk_free_rate) / volatility
    
    def calculate_beta(self) -> Optional[float]:
        """
        计算 Beta 系数 (相对于基准)
        """
        if not self.benchmark_returns or len(self.benchmark_returns) != self.n:
            return None
            
        if self.n < 10:
            return None
        
        # 计算协方差和方差
        mean_portfolio = sum(self.returns) / self.n
        mean_benchmark = sum(self.benchmark_returns) / self.n
        
        covariance = sum(
            (self.returns[i] - mean_portfolio) * (self.benchmark_returns[i] - mean_benchmark)
            for i in range(self.n)
        ) / (self.n - 1)
        
        variance_benchmark = sum(
            (r - mean_benchmark) ** 2 for r in self.benchmark_returns
        ) / (self.n - 1)
        
        if variance_benchmark == 0:
            return None
            
        return covariance / variance_benchmark
    
    def get_risk_metrics(self) -> Dict[str, float]:
        """获取完整风险指标"""
        return {
            'volatility': round(self.calculate_volatility(), 4),
            'var_95': round(self.calculate_var(0.95), 4),
            'var_99': round(self.calculate_var(0.99), 4),
            'cvar_95': round(self.calculate_cvar(0.95), 4),
            'max_drawdown': round(self.calculate_max_drawdown(), 4),
            'sharpe_ratio': round(self.calculate_sharpe_ratio(), 2),
            'beta': round(self.calculate_beta(), 4) if self.calculate_beta() else None
        }


class FinancialRiskWarning:
    """
    财务风险预警系统
    
    监控指标：
    1. 负债率预警
    2. 流动性预警
    3. 集中度预警
    4. 收益波动预警
    """
    
    # 预警阈值
    THRESHOLDS = {
        'debt_ratio_warning': 0.5,      # 负债率>50% 预警
        'debt_ratio_danger': 0.7,       # 负债率>70% 危险
        'liquidity_ratio_min': 0.1,     # 流动资产占比<10% 预警
        'emergency_fund_min_months': 3, # 应急资金<3 个月预警
        'single_asset_max': 0.5,        # 单一资产>50% 预警
        'volatility_warning': 0.3,      # 波动率>30% 预警
        'drawdown_warning': 0.2,        # 回撤>20% 预警
        'drawdown_danger': 0.4          # 回撤>40% 危险
    }
    
    def __init__(self):
        self.warnings = []
        self.alerts = []
    
    def check_debt_ratio(self, total_assets: float, total_liabilities: float) -> List[Dict]:
        """检查负债率风险"""
        if total_assets <= 0:
            return []
            
        debt_ratio = total_liabilities / total_assets
        warnings = []
        
        if debt_ratio >= self.THRESHOLDS['debt_ratio_danger']:
            warnings.append({
                'level': 'danger',
                'type': 'debt_ratio',
                'message': f'负债率{debt_ratio*100:.1f}%已超过危险线 (70%)，建议尽快降低负债',
                'value': debt_ratio,
                'threshold': self.THRESHOLDS['debt_ratio_danger']
            })
        elif debt_ratio >= self.THRESHOLDS['debt_ratio_warning']:
            warnings.append({
                'level': 'warning',
                'type': 'debt_ratio',
                'message': f'负债率{debt_ratio*100:.1f}%已超过预警线 (50%)，需注意控制',
                'value': debt_ratio,
                'threshold': self.THRESHOLDS['debt_ratio_warning']
            })
        
        return warnings
    
    def check_liquidity(
        self,
        liquid_assets: float,
        total_assets: float,
        monthly_expenses: float,
        emergency_fund: float
    ) -> List[Dict]:
        """检查流动性风险"""
        warnings = []
        
        # 流动资产占比
        if total_assets > 0:
            liquidity_ratio = liquid_assets / total_assets
            if liquidity_ratio < self.THRESHOLDS['liquidity_ratio_min']:
                warnings.append({
                    'level': 'warning',
                    'type': 'liquidity',
                    'message': f'流动资产占比{liquidity_ratio*100:.1f}%过低，建议提高流动性',
                    'value': liquidity_ratio,
                    'threshold': self.THRESHOLDS['liquidity_ratio_min']
                })
        
        # 应急资金
        if monthly_expenses > 0:
            emergency_months = emergency_fund / monthly_expenses
            if emergency_months < self.THRESHOLDS['emergency_fund_min_months']:
                warnings.append({
                    'level': 'warning',
                    'type': 'emergency_fund',
                    'message': f'应急资金仅够{emergency_months:.1f}个月支出，建议储备{self.THRESHOLDS["emergency_fund_min_months"]}个月以上',
                    'value': emergency_months,
                    'threshold': self.THRESHOLDS['emergency_fund_min_months']
                })
        
        return warnings
    
    def check_concentration(self, asset_allocation: Dict[str, float]) -> List[Dict]:
        """检查资产集中度风险"""
        warnings = []
        total = sum(asset_allocation.values())
        
        if total <= 0:
            return warnings
            
        for asset_name, value in asset_allocation.items():
            ratio = value / total
            if ratio > self.THRESHOLDS['single_asset_max']:
                warnings.append({
                    'level': 'warning',
                    'type': 'concentration',
                    'message': f'{asset_name}占比{ratio*100:.1f}%过高，建议分散配置',
                    'value': ratio,
                    'threshold': self.THRESHOLDS['single_asset_max']
                })
        
        return warnings
    
    def check_portfolio_risk(
        self,
        returns: List[float],
        current_drawdown: float = 0
    ) -> List[Dict]:
        """检查投资组合风险"""
        warnings = []
        
        if len(returns) >= 20:
            analyzer = PortfolioRiskAnalyzer(returns)
            volatility = analyzer.calculate_volatility()
            max_dd = analyzer.calculate_max_drawdown()
            
            if volatility > self.THRESHOLDS['volatility_warning']:
                warnings.append({
                    'level': 'warning',
                    'type': 'volatility',
                    'message': f'组合波动率{volatility*100:.1f}%较高，注意风险控制',
                    'value': volatility,
                    'threshold': self.THRESHOLDS['volatility_warning']
                })
            
            if max_dd > self.THRESHOLDS['drawdown_danger']:
                warnings.append({
                    'level': 'danger',
                    'type': 'drawdown',
                    'message': f'最大回撤{max_dd*100:.1f}%已达危险水平',
                    'value': max_dd,
                    'threshold': self.THRESHOLDS['drawdown_danger']
                })
            elif max_dd > self.THRESHOLDS['drawdown_warning']:
                warnings.append({
                    'level': 'warning',
                    'type': 'drawdown',
                    'message': f'最大回撤{max_dd*100:.1f}%已超过预警线',
                    'value': max_dd,
                    'threshold': self.THRESHOLDS['drawdown_warning']
                })
        
        # 当前回撤检查
        if current_drawdown > self.THRESHOLDS['drawdown_warning']:
            warnings.append({
                'level': 'warning' if current_drawdown < self.THRESHOLDS['drawdown_danger'] else 'danger',
                'type': 'current_drawdown',
                'message': f'当前回撤{current_drawdown*100:.1f}%',
                'value': current_drawdown
            })
        
        return warnings
    
    def full_check(
        self,
        total_assets: float,
        total_liabilities: float,
        liquid_assets: float,
        monthly_expenses: float,
        emergency_fund: float,
        asset_allocation: Dict[str, float],
        returns: Optional[List[float]] = None,
        current_drawdown: float = 0
    ) -> Dict[str, any]:
        """
        执行完整风险检查
        
        Returns:
            包含所有警告、风险等级、建议等信息
        """
        all_warnings = []
        
        # 执行所有检查
        all_warnings.extend(self.check_debt_ratio(total_assets, total_liabilities))
        all_warnings.extend(self.check_liquidity(liquid_assets, total_assets, monthly_expenses, emergency_fund))
        all_warnings.extend(self.check_concentration(asset_allocation))
        
        if returns:
            all_warnings.extend(self.check_portfolio_risk(returns, current_drawdown))
        
        # 计算风险等级
        danger_count = sum(1 for w in all_warnings if w['level'] == 'danger')
        warning_count = sum(1 for w in all_warnings if w['level'] == 'warning')
        
        if danger_count > 0:
            risk_level = 'high'
        elif warning_count >= 3:
            risk_level = 'medium'
        elif warning_count > 0:
            risk_level = 'low'
        else:
            risk_level = 'normal'
        
        # 生成建议
        recommendations = self._generate_recommendations(all_warnings)
        
        return {
            'risk_level': risk_level,
            'warning_count': warning_count,
            'danger_count': danger_count,
            'warnings': all_warnings,
            'recommendations': recommendations,
            'check_time': datetime.now().isoformat()
        }
    
    def _generate_recommendations(self, warnings: List[Dict]) -> List[str]:
        """根据警告生成建议"""
        recommendations = []
        warning_types = set(w['type'] for w in warnings)
        
        if 'debt_ratio' in warning_types:
            recommendations.append("优先偿还高息债务，考虑债务重组或延期")
        
        if 'liquidity' in warning_types or 'emergency_fund' in warning_types:
            recommendations.append("建立 3-6 个月支出的应急资金，提高资产流动性")
        
        if 'concentration' in warning_types:
            recommendations.append("分散投资，避免单一资产占比过高")
        
        if 'volatility' in warning_types:
            recommendations.append("考虑增加固定收益类资产，降低组合波动")
        
        if 'drawdown' in warning_types:
            recommendations.append("设置止损线，控制单笔投资损失")
        
        if not recommendations:
            recommendations.append("当前风险状况良好，继续保持多元化配置")
        
        return recommendations


# 便捷函数
def assess_risk_tolerance(**kwargs) -> Dict[str, any]:
    """
    便捷函数：评估风险承受能力
    
    示例:
        result = assess_risk_tolerance(
            age=35,
            employment_type='corporate',
            total_assets=1000000,
            years_investing=5
        )
    """
    return RiskToleranceScore.calculate_total_score(**kwargs)


def analyze_portfolio_risk(returns: List[float]) -> Dict[str, float]:
    """
    便捷函数：分析投资组合风险
    
    示例:
        metrics = analyze_portfolio_risk(daily_returns)
    """
    analyzer = PortfolioRiskAnalyzer(returns)
    return analyzer.get_risk_metrics()


if __name__ == '__main__':
    # 示例使用
    print("=" * 60)
    print("风险承受能力评估示例")
    print("=" * 60)
    
    result = assess_risk_tolerance(
        age=35,
        employment_type='corporate',
        income_variability=0.1,
        years_employed=8,
        total_assets=1500000,
        liquid_assets_ratio=0.3,
        debt_ratio=0.25,
        emergency_fund_months=6,
        years_investing=5,
        product_types=4,
        has_losses=True,
        education_level='bachelor',
        loss_tolerance=0.2,
        return_expectation=0.1,
        sleep_factor=0.2,
        investment_horizon=10,
        goal_importance=0.7,
        goal_flexibility=0.5
    )
    
    print(f"综合评分：{result['total_score']}")
    print(f"风险等级：{result['risk_level']}")
    print(f"投资建议：{result['recommendation']}")
    
    print("\n" + "=" * 60)
    print("财务风险预警示例")
    print("=" * 60)
    
    warner = FinancialRiskWarning()
    check_result = warner.full_check(
        total_assets=2000000,
        total_liabilities=800000,
        liquid_assets=300000,
        monthly_expenses=20000,
        emergency_fund=100000,
        asset_allocation={
            'stocks': 800000,
            'bonds': 500000,
            'cash': 300000,
            'real_estate': 400000
        },
        returns=[0.01, -0.02, 0.03, 0.015, -0.01, 0.02, -0.005, 0.025],
        current_drawdown=0.08
    )
    
    print(f"风险等级：{check_result['risk_level']}")
    print(f"警告数量：{check_result['warning_count']}")
    print(f"危险数量：{check_result['danger_count']}")
    print("\n建议:")
    for rec in check_result['recommendations']:
        print(f"  - {rec}")
