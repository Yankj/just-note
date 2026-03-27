"""
投资情感分析模块
负责识别交易中的贪婪/恐惧情绪，进行认知偏差分析
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class EmotionType(Enum):
    """情绪类型"""
    GREED = "greed"  # 贪婪
    FEAR = "fear"  # 恐惧
    NEUTRAL = "neutral"  # 中性
    OVERCONFIDENCE = "overconfidence"  # 过度自信
    REGRET = "regret"  # 后悔


class CognitiveBias(Enum):
    """认知偏差类型"""
    LOSS_AVERSION = "loss_aversion"  # 损失厌恶
    CONFIRMATION_BIAS = "confirmation_bias"  # 确认偏误
    ANCHORING = "anchoring"  # 锚定效应
    HERDING = "herding"  # 从众心理
    RECENCY_BIAS = "recency_bias"  # 近因效应
    SELF_ATTRIBUTION = "self_attribution"  # 自我归因
    GAMBLER_FALLACY = "gambler_fallacy"  # 赌徒谬误


@dataclass
class SentimentScore:
    """情感评分结果"""
    timestamp: datetime
    emotion_type: EmotionType
    intensity: float  # 0.0 - 1.0，情绪强度
    
    # 贪婪指标
    greed_indicators: dict = field(default_factory=dict)
    # 恐惧指标
    fear_indicators: dict = field(default_factory=dict)
    
    # 综合评分 (-1.0 极度恐惧 ~ +1.0 极度贪婪)
    composite_score: float = 0.0
    
    # 检测到的认知偏差
    detected_biases: list[CognitiveBias] = field(default_factory=list)
    
    # 分析备注
    notes: str = ""


class SentimentAnalyzer:
    """
    交易情感分析器
    基于交易行为识别贪婪/恐惧情绪
    """
    
    def __init__(self):
        # 贪婪阈值
        self.greed_threshold = 0.6
        # 恐惧阈值
        self.fear_threshold = -0.6
        
    def analyze_trade_sentiment(self, trade_data: dict) -> SentimentScore:
        """
        分析单笔交易的情感状态
        
        Args:
            trade_data: 包含交易信息的字典
                - position_size: 仓位大小 (相对于总资金的比例)
                - entry_timing: 入场时机 (0=底部, 0.5=中部, 1=顶部)
                - leverage: 杠杆倍数
                - stop_loss_set: 是否设置止损
                - take_profit_ratio: 止盈/止损比例
                - holding_period: 持仓时间 (天)
                - trade_frequency: 近期交易频率 (次/周)
                - market_sentiment: 市场情绪 (0=极度悲观, 1=极度乐观)
                - profit_loss: 盈亏金额
                - is_chasing: 是否追涨杀跌
                - deviation_from_plan: 偏离原计划程度 (0-1)
        
        Returns:
            SentimentScore: 情感评分结果
        """
        timestamp = datetime.now()
        greed_score = 0.0
        fear_score = 0.0
        
        greed_indicators = {}
        fear_indicators = {}
        
        # === 贪婪指标检测 ===
        
        # 1. 仓位过大 (>30% 总资金)
        position_size = trade_data.get("position_size", 0)
        if position_size > 0.3:
            greed_score += (position_size - 0.3) * 1.5
            greed_indicators["oversized_position"] = position_size
        
        # 2. 高杠杆 (>3 倍)
        leverage = trade_data.get("leverage", 1)
        if leverage > 3:
            greed_score += (leverage - 3) * 0.2
            greed_indicators["high_leverage"] = leverage
        
        # 3. 顶部追涨 (entry_timing > 0.7)
        entry_timing = trade_data.get("entry_timing", 0.5)
        if entry_timing > 0.7:
            greed_score += (entry_timing - 0.7) * 2
            greed_indicators["chasing_top"] = entry_timing
        
        # 4. 频繁交易 (>5 次/周)
        trade_frequency = trade_data.get("trade_frequency", 0)
        if trade_frequency > 5:
            greed_score += (trade_frequency - 5) * 0.1
            greed_indicators["overtrading"] = trade_frequency
        
        # 5. 无止损
        if not trade_data.get("stop_loss_set", True):
            greed_score += 0.3
            greed_indicators["no_stop_loss"] = True
        
        # 6. 追涨杀跌行为
        if trade_data.get("is_chasing", False):
            greed_score += 0.4
            greed_indicators["chasing_behavior"] = True
        
        # 7. 偏离交易计划
        deviation = trade_data.get("deviation_from_plan", 0)
        if deviation > 0.3:
            greed_score += deviation * 0.5
            greed_indicators["plan_deviation"] = deviation
        
        # === 恐惧指标检测 ===
        
        # 1. 仓位过小 (<5% 总资金，有机会不敢上)
        if position_size < 0.05 and trade_data.get("market_sentiment", 0.5) > 0.6:
            fear_score += (0.05 - position_size) * 3
            fear_indicators["undersized_position"] = position_size
        
        # 2. 底部不敢买 (entry_timing < 0.3 但 market_sentiment 低)
        if entry_timing < 0.3 and trade_data.get("market_sentiment", 0.5) < 0.3:
            fear_score += 0.4
            fear_indicators["fear_of_bottom"] = True
        
        # 3. 过早止盈 (take_profit_ratio < 1，盈亏比不合理)
        tp_ratio = trade_data.get("take_profit_ratio", 2)
        if tp_ratio < 1:
            fear_score += (1 - tp_ratio) * 0.3
            fear_indicators["early_profit_taking"] = tp_ratio
        
        # 4. 过紧止损 (holding_period 很短就止损)
        holding_period = trade_data.get("holding_period", 30)
        if holding_period < 3 and trade_data.get("profit_loss", 0) < 0:
            fear_score += 0.3
            fear_indicators["panic_stop"] = holding_period
        
        # 5. 亏损后停止交易 (trade_frequency 突然降低)
        if trade_frequency < 1 and trade_data.get("profit_loss", 0) < -0.1:
            fear_score += 0.3
            fear_indicators["post_loss_withdrawal"] = True
        
        # === 计算综合评分 ===
        composite_score = greed_score - fear_score
        composite_score = max(-1.0, min(1.0, composite_score))  # 限制在 [-1, 1]
        
        # === 确定主导情绪 ===
        if composite_score > self.greed_threshold:
            emotion_type = EmotionType.GREED
        elif composite_score < self.fear_threshold:
            emotion_type = EmotionType.FEAR
        elif greed_score > 0.3:
            emotion_type = EmotionType.OVERCONFIDENCE
        elif fear_score > 0.3:
            emotion_type = EmotionType.REGRET
        else:
            emotion_type = EmotionType.NEUTRAL
        
        # === 检测认知偏差 ===
        detected_biases = self._detect_cognitive_biases(trade_data, greed_indicators, fear_indicators)
        
        # === 生成分析备注 ===
        notes = self._generate_notes(emotion_type, greed_indicators, fear_indicators)
        
        # 情绪强度 (0-1)
        intensity = abs(composite_score)
        
        return SentimentScore(
            timestamp=timestamp,
            emotion_type=emotion_type,
            intensity=intensity,
            greed_indicators=greed_indicators,
            fear_indicators=fear_indicators,
            composite_score=composite_score,
            detected_biases=detected_biases,
            notes=notes
        )
    
    def _detect_cognitive_biases(
        self, 
        trade_data: dict, 
        greed_indicators: dict, 
        fear_indicators: dict
    ) -> list[CognitiveBias]:
        """检测认知偏差"""
        biases = []
        
        # 损失厌恶：亏损时持仓时间显著长于盈利时
        if trade_data.get("profit_loss", 0) < 0:
            holding_period = trade_data.get("holding_period", 30)
            if holding_period > 30:
                biases.append(CognitiveBias.LOSS_AVERSION)
        
        # 确认偏误：只关注支持自己观点的信息
        if trade_data.get("deviation_from_plan", 0) > 0.5:
            biases.append(CognitiveBias.CONFIRMATION_BIAS)
        
        # 锚定效应：基于买入价做决策
        if "early_profit_taking" in fear_indicators:
            biases.append(CognitiveBias.ANCHORING)
        
        # 从众心理：市场情绪高时追涨
        if trade_data.get("market_sentiment", 0.5) > 0.8 and trade_data.get("is_chasing", False):
            biases.append(CognitiveBias.HERDING)
        
        # 近因效应：基于最近表现做决策
        if trade_data.get("trade_frequency", 0) > 10:
            biases.append(CognitiveBias.RECENCY_BIAS)
        
        # 自我归因：盈利归因于能力，亏损归因于运气
        if "chasing_top" in greed_indicators and trade_data.get("profit_loss", 0) > 0:
            biases.append(CognitiveBias.SELF_ATTRIBUTION)
        
        # 赌徒谬误：认为连续亏损后会盈利
        if trade_data.get("trade_frequency", 0) > 5 and trade_data.get("profit_loss", 0) < 0:
            biases.append(CognitiveBias.GAMBLER_FALLACY)
        
        return biases
    
    def _generate_notes(
        self, 
        emotion_type: EmotionType, 
        greed_indicators: dict, 
        fear_indicators: dict
    ) -> str:
        """生成分析备注"""
        notes_parts = []
        
        if emotion_type == EmotionType.GREED:
            notes_parts.append("⚠️ 检测到贪婪情绪主导")
            if "oversized_position" in greed_indicators:
                notes_parts.append(f"仓位过大 ({greed_indicators['oversized_position']*100:.1f}%)")
            if "high_leverage" in greed_indicators:
                notes_parts.append(f"杠杆过高 ({greed_indicators['high_leverage']}倍)")
            if "chasing_top" in greed_indicators:
                notes_parts.append("追高行为明显")
            if "overtrading" in greed_indicators:
                notes_parts.append(f"交易过于频繁 ({greed_indicators['overtrading']}次/周)")
                
        elif emotion_type == EmotionType.FEAR:
            notes_parts.append("⚠️ 检测到恐惧情绪主导")
            if "undersized_position" in fear_indicators:
                notes_parts.append("仓位过小，错失机会")
            if "fear_of_bottom" in fear_indicators:
                notes_parts.append("底部不敢买入")
            if "panic_stop" in fear_indicators:
                notes_parts.append("恐慌性止损")
            if "post_loss_withdrawal" in fear_indicators:
                notes_parts.append("亏损后回避交易")
                
        elif emotion_type == EmotionType.OVERCONFIDENCE:
            notes_parts.append("⚠️ 检测到过度自信倾向")
            notes_parts.append("可能高估自己的判断能力")
            
        elif emotion_type == EmotionType.REGRET:
            notes_parts.append("⚠️ 检测到后悔情绪")
            notes_parts.append("可能影响后续决策质量")
        
        if not notes_parts:
            notes_parts.append("✓ 情绪状态平稳，决策理性")
        
        return "; ".join(notes_parts)
    
    def analyze_trade_journal_batch(self, trades: list[dict]) -> list[SentimentScore]:
        """批量分析交易日记"""
        return [self.analyze_trade_sentiment(trade) for trade in trades]
    
    def get_emotion_statistics(self, scores: list[SentimentScore]) -> dict:
        """获取情绪统计"""
        if not scores:
            return {}
        
        emotion_counts = {}
        total_greed = 0
        total_fear = 0
        bias_counts = {}
        
        for score in scores:
            # 情绪类型统计
            emotion_type = score.emotion_type.value
            emotion_counts[emotion_type] = emotion_counts.get(emotion_type, 0) + 1
            
            # 贪婪/恐惧分数累计
            if score.composite_score > 0:
                total_greed += score.composite_score
            else:
                total_fear += abs(score.composite_score)
            
            # 认知偏差统计
            for bias in score.detected_biases:
                bias_name = bias.value
                bias_counts[bias_name] = bias_counts.get(bias_name, 0) + 1
        
        total_trades = len(scores)
        
        return {
            "total_trades": total_trades,
            "emotion_distribution": emotion_counts,
            "average_greed_score": total_greed / total_trades if total_trades > 0 else 0,
            "average_fear_score": total_fear / total_trades if total_trades > 0 else 0,
            "bias_frequency": bias_counts,
            "rational_trades_percentage": emotion_counts.get("neutral", 0) / total_trades * 100 if total_trades > 0 else 0
        }
