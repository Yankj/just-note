"""
投资交易分析模块
包含投资日记数据模型、交易逻辑评分算法、盈亏归因分析
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional
from collections import defaultdict


# ==================== 数据模型 ====================

class TradeType(Enum):
    """交易类型"""
    BUY = "buy"
    SELL = "sell"
    SHORT = "short"
    COVER = "cover"


class AssetClass(Enum):
    """资产类别"""
    STOCK_A = "stock_a"  # A 股
    STOCK_HK = "stock_hk"  # 港股
    STOCK_US = "stock_us"  # 美股
    FUND = "fund"  # 基金
    CRYPTO = "crypto"  # 加密货币
    FUTURES = "futures"  # 期货
    OPTIONS = "options"  # 期权


class TradeStatus(Enum):
    """交易状态"""
    OPEN = "open"  # 持仓中
    CLOSED = "closed"  # 已平仓
    PENDING = "pending"  # 待成交


@dataclass
class TradeRecord:
    """交易记录数据模型"""
    id: str
    timestamp: datetime
    asset_code: str  # 股票代码
    asset_name: str  # 股票名称
    asset_class: AssetClass
    trade_type: TradeType
    price: float  # 成交价格
    quantity: int  # 成交数量
    amount: float  # 成交金额
    commission: float  # 手续费
    status: TradeStatus
    
    # 关联信息
    position_id: Optional[str] = None  # 关联仓位 ID
    order_id: Optional[str] = None  # 订单 ID
    
    # 交易逻辑
    entry_reason: str = ""  # 入场理由
    exit_reason: str = ""  # 出场理由
    strategy_tag: str = ""  # 策略标签
    
    # 计划信息
    planned_hold_days: int = 0  # 计划持仓天数
    target_price: Optional[float] = None  # 目标价
    stop_loss_price: Optional[float] = None  # 止损价
    
    # 实际信息
    actual_hold_days: int = 0  # 实际持仓天数
    actual_exit_price: Optional[float] = None  # 实际出场价
    actual_exit_time: Optional[datetime] = None  # 实际出场时间
    
    # 盈亏
    profit_loss: float = 0.0  # 盈亏金额
    profit_loss_pct: float = 0.0  # 盈亏比例
    
    # 情绪标记
    emotion_score: Optional[float] = None  # 情绪评分 (-1~1)
    confidence_level: int = 5  # 信心等级 (1-10)
    
    # 备注
    notes: str = ""
    tags: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "asset_code": self.asset_code,
            "asset_name": self.asset_name,
            "asset_class": self.asset_class.value,
            "trade_type": self.trade_type.value,
            "price": self.price,
            "quantity": self.quantity,
            "amount": self.amount,
            "commission": self.commission,
            "status": self.status.value,
            "position_id": self.position_id,
            "order_id": self.order_id,
            "entry_reason": self.entry_reason,
            "exit_reason": self.exit_reason,
            "strategy_tag": self.strategy_tag,
            "planned_hold_days": self.planned_hold_days,
            "target_price": self.target_price,
            "stop_loss_price": self.stop_loss_price,
            "actual_hold_days": self.actual_hold_days,
            "actual_exit_price": self.actual_exit_price,
            "actual_exit_time": self.actual_exit_time.isoformat() if self.actual_exit_time else None,
            "profit_loss": self.profit_loss,
            "profit_loss_pct": self.profit_loss_pct,
            "emotion_score": self.emotion_score,
            "confidence_level": self.confidence_level,
            "notes": self.notes,
            "tags": self.tags
        }


@dataclass
class Position:
    """仓位数据模型"""
    id: str
    asset_code: str
    asset_name: str
    asset_class: AssetClass
    
    # 持仓信息
    quantity: int  # 持仓数量
    avg_cost: float  # 平均成本
    current_price: float  # 当前价格
    market_value: float  # 市值
    
    # 盈亏
    unrealized_pnl: float  # 浮动盈亏
    unrealized_pnl_pct: float  # 浮动盈亏比例
    
    # 开仓信息
    open_time: datetime
    open_trades: list[str] = field(default_factory=list)  # 开仓交易 ID 列表
    
    # 平仓信息
    close_trades: list[str] = field(default_factory=list)  # 平仓交易 ID 列表
    realized_pnl: float = 0.0  # 已实现盈亏
    
    def update_price(self, price: float):
        """更新当前价格并重新计算盈亏"""
        self.current_price = price
        self.market_value = self.quantity * self.current_price
        self.unrealized_pnl = self.market_value - (self.quantity * self.avg_cost)
        self.unrealized_pnl_pct = self.unrealized_pnl / (self.quantity * self.avg_cost) if self.avg_cost > 0 else 0


@dataclass
class TradeLogicScore:
    """交易逻辑评分结果"""
    trade_id: str
    timestamp: datetime
    
    # 各维度评分 (0-100)
    entry_timing_score: float = 0  # 入场时机评分
    position_management_score: float = 0  # 仓位管理评分
    risk_control_score: float = 0  # 风险控制评分
    strategy_adherence_score: float = 0  # 策略执行评分
    exit_logic_score: float = 0  # 出场逻辑评分
    
    # 综合评分 (0-100)
    total_score: float = 0.0
    
    # 评分详情
    score_details: dict = field(default_factory=dict)
    
    # 改进建议
    suggestions: list[str] = field(default_factory=list)
    
    # 评级
    grade: str = ""  # A/B/C/D/E


@dataclass
class PnLAttribution:
    """盈亏归因分析结果"""
    trade_id: str
    timestamp: datetime
    
    # 盈亏分解
    total_pnl: float = 0.0  # 总盈亏
    
    # 归因因子
    market_beta_pnl: float = 0.0  # 市场 Beta 收益 (大盘涨跌带来的)
    sector_alpha_pnl: float = 0.0  # 行业 Alpha 收益
    stock_alpha_pnl: float = 0.0  # 个股 Alpha 收益 (选股能力)
    timing_pnl: float = 0.0  # 时机选择收益
    position_pnl: float = 0.0  # 仓位管理收益
    trading_cost: float = 0.0  # 交易成本损耗
    
    # 归因比例
    market_beta_ratio: float = 0.0
    sector_alpha_ratio: float = 0.0
    stock_alpha_ratio: float = 0.0
    timing_ratio: float = 0.0
    position_ratio: float = 0.0
    cost_ratio: float = 0.0
    
    # 能力评估
    stock_picking_ability: str = ""  # 选股能力评估
    timing_ability: str = ""  # 择时能力评估
    position_management_ability: str = ""  # 仓位管理能力评估
    
    # 备注
    notes: str = ""


# ==================== 交易逻辑评分器 ====================

class TradeLogicScorer:
    """交易逻辑评分器"""
    
    def __init__(self):
        self.weights = {
            "entry_timing": 0.25,
            "position_management": 0.20,
            "risk_control": 0.25,
            "strategy_adherence": 0.15,
            "exit_logic": 0.15
        }
    
    def score_trade(self, trade: TradeRecord, market_data: Optional[dict] = None) -> TradeLogicScore:
        """
        对单笔交易进行逻辑评分
        
        Args:
            trade: 交易记录
            market_data: 市场数据 (可选)
                - market_trend: 市场趋势 (-1~1)
                - sector_performance: 行业表现
                - stock_volatility: 股票波动率
        
        Returns:
            TradeLogicScore: 评分结果
        """
        timestamp = datetime.now()
        score_details = {}
        suggestions = []
        
        # === 1. 入场时机评分 (0-100) ===
        entry_timing_score = self._score_entry_timing(trade, market_data)
        score_details["entry_timing"] = {
            "score": entry_timing_score,
            "factors": self._get_entry_timing_factors(trade, market_data)
        }
        if entry_timing_score < 60:
            suggestions.append("入场时机选择不佳，建议加强技术分析或等待更好的买点")
        
        # === 2. 仓位管理评分 (0-100) ===
        position_score = self._score_position_management(trade)
        score_details["position_management"] = {
            "score": position_score,
            "factors": self._get_position_factors(trade)
        }
        if position_score < 60:
            suggestions.append("仓位管理不合理，建议根据风险承受能力调整仓位")
        
        # === 3. 风险控制评分 (0-100) ===
        risk_score = self._score_risk_control(trade)
        score_details["risk_control"] = {
            "score": risk_score,
            "factors": self._get_risk_factors(trade)
        }
        if risk_score < 60:
            suggestions.append("风险控制不足，必须设置止损并严格执行")
        
        # === 4. 策略执行评分 (0-100) ===
        strategy_score = self._score_strategy_adherence(trade)
        score_details["strategy_adherence"] = {
            "score": strategy_score,
            "factors": self._get_strategy_factors(trade)
        }
        if strategy_score < 60:
            suggestions.append("策略执行不严格，建议制定明确的交易计划并遵守")
        
        # === 5. 出场逻辑评分 (0-100) ===
        exit_score = self._score_exit_logic(trade)
        score_details["exit_logic"] = {
            "score": exit_score,
            "factors": self._get_exit_factors(trade)
        }
        if exit_score < 60 and trade.status == TradeStatus.CLOSED:
            suggestions.append("出场逻辑不清晰，建议设定明确的止盈止损点")
        
        # === 计算综合评分 ===
        total_score = (
            entry_timing_score * self.weights["entry_timing"] +
            position_score * self.weights["position_management"] +
            risk_score * self.weights["risk_control"] +
            strategy_score * self.weights["strategy_adherence"] +
            exit_score * self.weights["exit_logic"]
        )
        
        # === 确定评级 ===
        grade = self._calculate_grade(total_score)
        
        return TradeLogicScore(
            trade_id=trade.id,
            timestamp=timestamp,
            entry_timing_score=entry_timing_score,
            position_management_score=position_score,
            risk_control_score=risk_score,
            strategy_adherence_score=strategy_score,
            exit_logic_score=exit_score,
            total_score=total_score,
            score_details=score_details,
            suggestions=suggestions,
            grade=grade
        )
    
    def _score_entry_timing(self, trade: TradeRecord, market_data: Optional[dict]) -> float:
        """入场时机评分"""
        score = 50.0  # 基础分
        
        # 有计划持仓时间说明有准备
        if trade.planned_hold_days > 0:
            score += 10
        
        # 有目标价说明有研究
        if trade.target_price:
            score += 10
        
        # 有信心等级
        if trade.confidence_level >= 7:
            score += 10
        elif trade.confidence_level <= 3:
            score -= 10
        
        # 如果有市场数据
        if market_data:
            # 顺趋势交易加分
            market_trend = market_data.get("market_trend", 0)
            if market_trend > 0.3:  # 上涨趋势
                score += 15
            elif market_trend < -0.3:  # 下跌趋势
                score -= 10
        
        return max(0, min(100, score))
    
    def _score_position_management(self, trade: TradeRecord) -> float:
        """仓位管理评分"""
        score = 50.0
        
        # 仓位适中 (假设 amount 可以推算仓位比例)
        # 这里简化处理，有明确的交易金额说明有规划
        if trade.amount > 0:
            score += 20
        
        # 有止损价说明有风险意识
        if trade.stop_loss_price:
            score += 20
        
        # 有计划持仓时间
        if trade.planned_hold_days > 0:
            score += 10
        
        return max(0, min(100, score))
    
    def _score_risk_control(self, trade: TradeRecord) -> float:
        """风险控制评分"""
        score = 50.0
        
        # 设置止损价
        if trade.stop_loss_price:
            score += 30
        else:
            score -= 20
        
        # 设置目标价
        if trade.target_price:
            score += 10
        
        # 有入场理由
        if trade.entry_reason:
            score += 10
        
        return max(0, min(100, score))
    
    def _score_strategy_adherence(self, trade: TradeRecord) -> float:
        """策略执行评分"""
        score = 50.0
        
        # 有策略标签
        if trade.strategy_tag:
            score += 20
        
        # 有入场理由
        if trade.entry_reason:
            score += 15
        
        # 有标签说明有分类
        if trade.tags:
            score += 15
        
        return max(0, min(100, score))
    
    def _score_exit_logic(self, trade: TradeRecord) -> float:
        """出场逻辑评分"""
        if trade.status != TradeStatus.CLOSED:
            return 50.0  # 未平仓不评分
        
        score = 50.0
        
        # 有出场理由
        if trade.exit_reason:
            score += 30
        
        # 实际持仓天数与计划接近
        if trade.planned_hold_days > 0 and trade.actual_hold_days > 0:
            deviation = abs(trade.actual_hold_days - trade.planned_hold_days) / trade.planned_hold_days
            if deviation < 0.2:
                score += 20
            elif deviation < 0.5:
                score += 10
            else:
                score -= 10
        
        return max(0, min(100, score))
    
    def _get_entry_timing_factors(self, trade: TradeRecord, market_data: Optional[dict]) -> list[str]:
        """获取入场时机评分因素"""
        factors = []
        if trade.planned_hold_days > 0:
            factors.append("有计划持仓时间")
        if trade.target_price:
            factors.append("有目标价位")
        if trade.confidence_level >= 7:
            factors.append("信心充足")
        if market_data and market_data.get("market_trend", 0) > 0.3:
            factors.append("顺趋势交易")
        return factors
    
    def _get_position_factors(self, trade: TradeRecord) -> list[str]:
        """获取仓位管理评分因素"""
        factors = []
        if trade.amount > 0:
            factors.append("明确交易金额")
        if trade.stop_loss_price:
            factors.append("设置止损")
        if trade.planned_hold_days > 0:
            factors.append("计划持仓时间")
        return factors
    
    def _get_risk_factors(self, trade: TradeRecord) -> list[str]:
        """获取风险控制评分因素"""
        factors = []
        if trade.stop_loss_price:
            factors.append("设置止损价")
        else:
            factors.append("⚠️ 未设置止损")
        if trade.target_price:
            factors.append("设置目标价")
        if trade.entry_reason:
            factors.append("明确入场理由")
        return factors
    
    def _get_strategy_factors(self, trade: TradeRecord) -> list[str]:
        """获取策略执行评分因素"""
        factors = []
        if trade.strategy_tag:
            factors.append(f"策略：{trade.strategy_tag}")
        if trade.entry_reason:
            factors.append("有入场理由")
        if trade.tags:
            factors.append(f"标签：{', '.join(trade.tags)}")
        return factors
    
    def _get_exit_factors(self, trade: TradeRecord) -> list[str]:
        """获取出场逻辑评分因素"""
        factors = []
        if trade.status != TradeStatus.CLOSED:
            return ["未平仓"]
        if trade.exit_reason:
            factors.append(f"出场理由：{trade.exit_reason}")
        if trade.planned_hold_days > 0 and trade.actual_hold_days > 0:
            factors.append(f"计划{trade.planned_hold_days}天，实际{trade.actual_hold_days}天")
        return factors
    
    def _calculate_grade(self, total_score: float) -> str:
        """计算评级"""
        if total_score >= 90:
            return "A"
        elif total_score >= 80:
            return "B"
        elif total_score >= 70:
            return "C"
        elif total_score >= 60:
            return "D"
        else:
            return "E"


# ==================== 盈亏归因分析器 ====================

class PnLAttributionAnalyzer:
    """盈亏归因分析器"""
    
    def __init__(self):
        # 归因因子权重
        self.attribution_weights = {
            "market_beta": 0.3,
            "sector_alpha": 0.2,
            "stock_alpha": 0.25,
            "timing": 0.15,
            "position": 0.1
        }
    
    def attribute_pnl(self, trade: TradeRecord, benchmark_data: Optional[dict] = None) -> PnLAttribution:
        """
        对交易盈亏进行归因分析
        
        Args:
            trade: 交易记录
            benchmark_data: 基准数据 (可选)
                - market_return: 市场收益率
                - sector_return: 行业收益率
                - holding_period_return: 持仓期收益
        
        Returns:
            PnLAttribution: 归因分析结果
        """
        timestamp = datetime.now()
        
        total_pnl = trade.profit_loss
        
        # 初始化归因结果
        attribution = PnLAttribution(
            trade_id=trade.id,
            timestamp=timestamp,
            total_pnl=total_pnl
        )
        
        if not benchmark_data:
            # 无基准数据时，使用简化归因
            attribution = self._simple_attribution(trade, attribution)
        else:
            # 有基准数据时，使用详细归因
            attribution = self._detailed_attribution(trade, benchmark_data, attribution)
        
        # 计算归因比例
        if total_pnl != 0:
            attribution.market_beta_ratio = attribution.market_beta_pnl / abs(total_pnl) if total_pnl != 0 else 0
            attribution.sector_alpha_ratio = attribution.sector_alpha_pnl / abs(total_pnl) if total_pnl != 0 else 0
            attribution.stock_alpha_ratio = attribution.stock_alpha_pnl / abs(total_pnl) if total_pnl != 0 else 0
            attribution.timing_ratio = attribution.timing_pnl / abs(total_pnl) if total_pnl != 0 else 0
            attribution.position_ratio = attribution.position_pnl / abs(total_pnl) if total_pnl != 0 else 0
            attribution.cost_ratio = attribution.trading_cost / abs(total_pnl) if total_pnl != 0 else 0
        
        # 能力评估
        attribution.stock_picking_ability = self._evaluate_stock_picking(attribution)
        attribution.timing_ability = self._evaluate_timing(attribution)
        attribution.position_management_ability = self._evaluate_position(attribution)
        
        # 生成备注
        attribution.notes = self._generate_attribution_notes(attribution)
        
        return attribution
    
    def _simple_attribution(self, trade: TradeRecord, attribution: PnLAttribution) -> PnLAttribution:
        """简化归因 (无基准数据)"""
        total_pnl = trade.profit_loss
        
        # 估算交易成本
        trading_cost = trade.commission
        attribution.trading_cost = -abs(trading_cost)
        
        # 简化假设：盈亏主要来自选股和时机
        if total_pnl > 0:
            # 盈利时，归因于选股能力
            attribution.stock_alpha_pnl = total_pnl * 0.6
            attribution.timing_pnl = total_pnl * 0.3
            attribution.market_beta_pnl = total_pnl * 0.1
        else:
            # 亏损时，归因于时机选择
            attribution.timing_pnl = total_pnl * 0.5
            attribution.stock_alpha_pnl = total_pnl * 0.3
            attribution.market_beta_pnl = total_pnl * 0.2
        
        return attribution
    
    def _detailed_attribution(
        self, 
        trade: TradeRecord, 
        benchmark_data: dict, 
        attribution: PnLAttribution
    ) -> PnLAttribution:
        """详细归因 (有基准数据)"""
        total_pnl = trade.profit_loss
        pnl_pct = trade.profit_loss_pct
        
        # 交易成本
        trading_cost = trade.commission
        attribution.trading_cost = -abs(trading_cost)
        
        # 市场 Beta 收益 = 持仓金额 * 市场收益率
        market_return = benchmark_data.get("market_return", 0)
        attribution.market_beta_pnl = trade.amount * market_return
        
        # 行业 Alpha = 持仓金额 * (行业收益 - 市场收益)
        sector_return = benchmark_data.get("sector_return", 0)
        attribution.sector_alpha_pnl = trade.amount * (sector_return - market_return)
        
        # 个股 Alpha = 实际收益 - Beta - 行业 Alpha
        stock_excess_return = pnl_pct - market_return - (sector_return - market_return)
        attribution.stock_alpha_pnl = trade.amount * stock_excess_return * 0.7
        
        # 时机选择收益 = 基于入场时机与基准的比较
        timing_factor = benchmark_data.get("timing_factor", 0)
        attribution.timing_pnl = trade.amount * timing_factor
        
        # 仓位管理收益 = 基于仓位调整的贡献
        position_factor = benchmark_data.get("position_factor", 0)
        attribution.position_pnl = trade.amount * position_factor
        
        return attribution
    
    def _evaluate_stock_picking(self, attribution: PnLAttribution) -> str:
        """评估选股能力"""
        stock_alpha = attribution.stock_alpha_pnl
        if stock_alpha > 0:
            return "优秀" if stock_alpha > 1000 else "良好" if stock_alpha > 100 else "一般"
        else:
            return "待改进" if stock_alpha < -500 else "一般"
    
    def _evaluate_timing(self, attribution: PnLAttribution) -> str:
        """评估择时能力"""
        timing = attribution.timing_pnl
        if timing > 0:
            return "优秀" if timing > 500 else "良好" if timing > 100 else "一般"
        else:
            return "待改进" if timing < -300 else "一般"
    
    def _evaluate_position(self, attribution: PnLAttribution) -> str:
        """评估仓位管理能力"""
        position = attribution.position_pnl
        if position > 0:
            return "优秀" if position > 300 else "良好" if position > 50 else "一般"
        else:
            return "待改进" if position < -200 else "一般"
    
    def _generate_attribution_notes(self, attribution: PnLAttribution) -> str:
        """生成归因分析备注"""
        notes_parts = []
        
        # 主要贡献因子
        contributions = [
            ("市场 Beta", attribution.market_beta_pnl),
            ("行业 Alpha", attribution.sector_alpha_pnl),
            ("选股 Alpha", attribution.stock_alpha_pnl),
            ("时机选择", attribution.timing_pnl),
            ("仓位管理", attribution.position_pnl)
        ]
        
        # 找出最大正贡献和负贡献
        positive_contribs = [(name, val) for name, val in contributions if val > 0]
        negative_contribs = [(name, val) for name, val in contributions if val < 0]
        
        if positive_contribs:
            best = max(positive_contribs, key=lambda x: x[1])
            notes_parts.append(f"主要盈利来源：{best[0]} ({best[1]:.2f})")
        
        if negative_contribs:
            worst = min(negative_contribs, key=lambda x: x[1])
            notes_parts.append(f"主要亏损来源：{worst[0]} ({worst[1]:.2f})")
        
        # 能力评估总结
        if attribution.stock_picking_ability in ["优秀", "良好"]:
            notes_parts.append(f"选股能力：{attribution.stock_picking_ability}")
        if attribution.timing_ability in ["优秀", "良好"]:
            notes_parts.append(f"择时能力：{attribution.timing_ability}")
        
        # 交易成本提醒
        if abs(attribution.trading_cost) > 100:
            notes_parts.append(f"⚠️ 交易成本较高：{abs(attribution.trading_cost):.2f}")
        
        if not notes_parts:
            notes_parts.append("归因分析完成，无明显异常")
        
        return "; ".join(notes_parts)
    
    def batch_attribute(self, trades: list[TradeRecord], benchmark_data_list: Optional[list[dict]] = None) -> list[PnLAttribution]:
        """批量归因分析"""
        results = []
        for i, trade in enumerate(trades):
            benchmark = benchmark_data_list[i] if benchmark_data_list and i < len(benchmark_data_list) else None
            results.append(self.attribute_pnl(trade, benchmark))
        return results
    
    def aggregate_attribution(self, attributions: list[PnLAttribution]) -> dict:
        """汇总归因分析结果"""
        if not attributions:
            return {}
        
        total_pnl = sum(a.total_pnl for a in attributions)
        total_market_beta = sum(a.market_beta_pnl for a in attributions)
        total_sector_alpha = sum(a.sector_alpha_pnl for a in attributions)
        total_stock_alpha = sum(a.stock_alpha_pnl for a in attributions)
        total_timing = sum(a.timing_pnl for a in attributions)
        total_position = sum(a.position_pnl for a in attributions)
        total_cost = sum(a.trading_cost for a in attributions)
        
        # 计算各因子贡献比例
        total_abs = abs(total_pnl) if total_pnl != 0 else 1
        
        return {
            "total_trades": len(attributions),
            "total_pnl": total_pnl,
            "attribution_breakdown": {
                "market_beta": {"amount": total_market_beta, "ratio": total_market_beta / total_abs},
                "sector_alpha": {"amount": total_sector_alpha, "ratio": total_sector_alpha / total_abs},
                "stock_alpha": {"amount": total_stock_alpha, "ratio": total_stock_alpha / total_abs},
                "timing": {"amount": total_timing, "ratio": total_timing / total_abs},
                "position": {"amount": total_position, "ratio": total_position / total_abs},
                "trading_cost": {"amount": total_cost, "ratio": abs(total_cost) / total_abs}
            },
            "ability_summary": {
                "stock_picking": self._aggregate_ability([a.stock_picking_ability for a in attributions]),
                "timing": self._aggregate_ability([a.timing_ability for a in attributions]),
                "position_management": self._aggregate_ability([a.position_management_ability for a in attributions])
            }
        }
    
    def _aggregate_ability(self, abilities: list[str]) -> str:
        """汇总能力评估"""
        if not abilities:
            return "N/A"
        
        score_map = {"优秀": 4, "良好": 3, "一般": 2, "待改进": 1}
        avg_score = sum(score_map.get(a, 2) for a in abilities) / len(abilities)
        
        if avg_score >= 3.5:
            return "优秀"
        elif avg_score >= 2.5:
            return "良好"
        elif avg_score >= 1.5:
            return "一般"
        else:
            return "待改进"
