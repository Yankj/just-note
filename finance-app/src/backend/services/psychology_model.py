"""
交易心理诊断模型
Finance Psychology Model - Trading Psychology Assessment

负责：
1. 定义常见认知偏差（6 种以上）
2. 实现心理评分模型
3. 创建心理测试题库
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json


# ==================== 认知偏差定义 ====================

class CognitiveBiasType(Enum):
    """认知偏差类型"""
    LOSS_AVERSION = "loss_aversion"  # 损失厌恶
    CONFIRMATION_BIAS = "confirmation_bias"  # 确认偏误
    OVERCONFIDENCE = "overconfidence"  # 过度自信
    ANCHORING = "anchoring"  # 锚定效应
    HERD_MENTALITY = "herd_mentality"  # 从众心理
    RECENCY_BIAS = "recency_bias"  # 近因效应
    GAMBLER_FALLACY = "gambler_fallacy"  # 赌徒谬误
    ENDOWMENT_EFFECT = "endowment_effect"  # 禀赋效应
    STATUS_QUO_BIAS = "status_quo_bias"  # 现状偏见
    SELF_ATTRIBUTION = "self_attribution"  # 自我归因偏差


@dataclass
class CognitiveBias:
    """认知偏差数据结构"""
    bias_type: CognitiveBiasType
    name: str
    name_en: str
    description: str
    trading_manifestation: str  # 在交易中的表现
    risk_level: int  # 风险等级 1-5
    detection_questions: List[str]  # 检测问题
    
    def to_dict(self) -> dict:
        return {
            "bias_type": self.bias_type.value,
            "name": self.name,
            "name_en": self.name_en,
            "description": self.description,
            "trading_manifestation": self.trading_manifestation,
            "risk_level": self.risk_level,
            "detection_questions": self.detection_questions
        }


# 认知偏差库
COGNITIVE_BIASES: Dict[CognitiveBiasType, CognitiveBias] = {
    CognitiveBiasType.LOSS_AVERSION: CognitiveBias(
        bias_type=CognitiveBiasType.LOSS_AVERSION,
        name="损失厌恶",
        name_en="Loss Aversion",
        description="人们对损失的痛苦感受远大于同等收益带来的快乐，导致过早止盈、过晚止损。",
        trading_manifestation="盈利时过早卖出锁定利润，亏损时死扛不愿止损，期待回本。",
        risk_level=5,
        detection_questions=[
            "你是否经常在盈利一点点时就急于卖出，害怕利润回吐？",
            "当持仓亏损时，你是否倾向于继续持有，期待价格反弹？",
            "你是否设定了止损点但经常不执行？",
            "亏损带来的情绪困扰是否远大于盈利带来的喜悦？"
        ]
    ),
    CognitiveBiasType.CONFIRMATION_BIAS: CognitiveBias(
        bias_type=CognitiveBiasType.CONFIRMATION_BIAS,
        name="确认偏误",
        name_en="Confirmation Bias",
        description="倾向于寻找和相信支持自己已有观点的信息，忽视或贬低相反证据。",
        trading_manifestation="只看利好消息，忽视利空信号；加入看涨社群强化已有观点；对反面信息选择性失明。",
        risk_level=4,
        detection_questions=[
            "做投资决策前，你是否主动寻找反面观点？",
            "看到不利消息时，你是否倾向于质疑其可靠性？",
            "你是否只关注支持自己持仓方向的分析师？",
            "当市场走势与预期相反时，你是否寻找理由解释而非反思？"
        ]
    ),
    CognitiveBiasType.OVERCONFIDENCE: CognitiveBias(
        bias_type=CognitiveBiasType.OVERCONFIDENCE,
        name="过度自信",
        name_en="Overconfidence",
        description="高估自己的知识、能力和预测准确性，导致过度交易和风险暴露。",
        trading_manifestation="频繁交易、仓位过重、忽视止损、认为自己能战胜市场。",
        risk_level=5,
        detection_questions=[
            "你是否认为自己比大多数投资者更懂市场？",
            "连续盈利后，你是否会增加仓位或交易频率？",
            "你是否经常不做充分研究就做出投资决策？",
            "你是否相信自己的直觉胜过系统化的分析方法？"
        ]
    ),
    CognitiveBiasType.ANCHORING: CognitiveBias(
        bias_type=CognitiveBiasType.ANCHORING,
        name="锚定效应",
        name_en="Anchoring Effect",
        description="过度依赖首次获得的信息（锚点），后续判断围绕该锚点调整。",
        trading_manifestation="以买入价作为参考点判断盈亏；被历史高点/低点锚定；过度关注某个目标价。",
        risk_level=4,
        detection_questions=[
            "你是否经常以买入成本价作为判断投资成败的标准？",
            "某股票的历史高点是否影响你对它当前价值的判断？",
            "你是否因为某价格曾出现过而认为它会再次回到该位置？",
            "分析师的目标价是否过度影响你的买卖决策？"
        ]
    ),
    CognitiveBiasType.HERD_MENTALITY: CognitiveBias(
        bias_type=CognitiveBiasType.HERD_MENTALITY,
        name="从众心理",
        name_en="Herd Mentality",
        description="跟随大多数人的行为或观点，害怕被孤立或错过机会。",
        trading_manifestation="追涨杀跌、FOMO 入场、热门股盲目跟风、恐慌性抛售。",
        risk_level=4,
        detection_questions=[
            "看到别人都在买某只股票时，你是否会感到压力也要买入？",
            "市场大跌时，你是否会因恐慌而跟随抛售？",
            "你是否经常因为害怕错过而买入热门资产？",
            "你的投资决策是否经常受到社交媒体或群聊的影响？"
        ]
    ),
    CognitiveBiasType.RECENCY_BIAS: CognitiveBias(
        bias_type=CognitiveBiasType.RECENCY_BIAS,
        name="近因效应",
        name_en="Recency Bias",
        description="过度重视最近发生的事件，忽视长期历史数据和规律。",
        trading_manifestation="根据近期走势线性外推；牛市末期过度乐观，熊市末期过度悲观。",
        risk_level=3,
        detection_questions=[
            "你是否认为最近的走势会持续下去？",
            "连续上涨后你是否更看好后市，连续下跌后更看空？",
            "你是否容易忘记长期的平均回报率，而过度关注近期表现？",
            "市场新闻是否过度影响你对短期走势的判断？"
        ]
    ),
    CognitiveBiasType.GAMBLER_FALLACY: CognitiveBias(
        bias_type=CognitiveBiasType.GAMBLER_FALLACY,
        name="赌徒谬误",
        name_en="Gambler's Fallacy",
        description="错误地认为独立事件之间存在关联，认为某事'该发生了'。",
        trading_manifestation="连续亏损后认为'该赢了'而加大仓位；认为涨多了'该跌了'。",
        risk_level=4,
        detection_questions=[
            "连续亏损后，你是否觉得下一笔交易更可能盈利？",
            "某资产连续上涨后，你是否认为'该回调了'而做空？",
            "你是否相信市场有某种'平衡机制'会自动纠偏？",
            "过去的走势是否影响你对未来独立事件的判断？"
        ]
    ),
    CognitiveBiasType.ENDOWMENT_EFFECT: CognitiveBias(
        bias_type=CognitiveBiasType.ENDOWMENT_EFFECT,
        name="禀赋效应",
        name_en="Endowment Effect",
        description="对自己拥有的资产赋予更高价值，不愿以公平价格出售。",
        trading_manifestation="高估自己持仓的价值；不愿卖出已持有的股票即使基本面变差。",
        risk_level=3,
        detection_questions=[
            "你是否认为自己持有的股票比同类未持有的更有价值？",
            "如果有人想从你手中买走你的持仓，你开价会高于市场价吗？",
            "你是否因为'已经持有很久'而不愿卖出某资产？",
            "换仓时，你是否对卖出旧持仓感到特别不舍？"
        ]
    )
}


# ==================== 心理评分模型 ====================

class PsychologyScoreLevel(Enum):
    """心理评分等级"""
    EXCELLENT = "excellent"  # 优秀 (80-100)
    GOOD = "good"  # 良好 (60-79)
    FAIR = "fair"  # 一般 (40-59)
    POOR = "poor"  # 较差 (20-39)
    CRITICAL = "critical"  # 危险 (0-19)


@dataclass
class BiasScore:
    """单个偏差的评分"""
    bias_type: CognitiveBiasType
    raw_score: float  # 原始得分 0-100
    severity: str  # 严重程度: low/medium/high/critical
    weight: float  # 权重
    
    def to_dict(self) -> dict:
        return {
            "bias_type": self.bias_type.value,
            "bias_name": COGNITIVE_BIASES[self.bias_type].name,
            "raw_score": round(self.raw_score, 2),
            "severity": self.severity,
            "weight": self.weight
        }


@dataclass
class PsychologyAssessmentResult:
    """心理评估结果"""
    overall_score: float  # 总体得分 0-100
    level: PsychologyScoreLevel  # 等级
    bias_scores: List[BiasScore]  # 各偏差得分
    top_risks: List[CognitiveBiasType]  # 前三大风险
    assessment_date: str  # 评估日期
    recommendations: List[str]  # 建议
    
    def to_dict(self) -> dict:
        return {
            "overall_score": round(self.overall_score, 2),
            "level": self.level.value,
            "bias_scores": [bs.to_dict() for bs in self.bias_scores],
            "top_risks": [tr.value for tr in self.top_risks],
            "assessment_date": self.assessment_date,
            "recommendations": self.recommendations
        }


class PsychologyScoringModel:
    """心理评分模型"""
    
    # 各偏差的权重（可根据研究调整）
    BIAS_WEIGHTS: Dict[CognitiveBiasType, float] = {
        CognitiveBiasType.LOSS_AVERSION: 0.20,  # 损失厌恶权重最高
        CognitiveBiasType.OVERCONFIDENCE: 0.18,  # 过度自信
        CognitiveBiasType.CONFIRMATION_BIAS: 0.15,  # 确认偏误
        CognitiveBiasType.HERD_MENTALITY: 0.13,  # 从众心理
        CognitiveBiasType.ANCHORING: 0.12,  # 锚定效应
        CognitiveBiasType.GAMBLER_FALLACY: 0.10,  # 赌徒谬误
        CognitiveBiasType.RECENCY_BIAS: 0.07,  # 近因效应
        CognitiveBiasType.ENDOWMENT_EFFECT: 0.05,  # 禀赋效应
    }
    
    # 严重程度阈值
    SEVERITY_THRESHOLDS = {
        "low": 25,
        "medium": 50,
        "high": 75,
        "critical": 90
    }
    
    def __init__(self):
        self.responses: Dict[CognitiveBiasType, List[int]] = {}
    
    def submit_response(self, bias_type: CognitiveBiasType, question_index: int, score: int):
        """
        提交回答
        
        Args:
            bias_type: 偏差类型
            question_index: 问题索引 (0-based)
            score: 得分 1-5 (1=完全不符合, 5=完全符合)
        """
        if bias_type not in self.responses:
            max_questions = len(COGNITIVE_BIASES[bias_type].detection_questions)
            self.responses[bias_type] = [0] * max_questions
        
        if 0 <= question_index < len(self.responses[bias_type]):
            self.responses[bias_type][question_index] = score
    
    def _calculate_bias_score(self, bias_type: CognitiveBiasType) -> float:
        """计算单个偏差的得分 (0-100)"""
        if bias_type not in self.responses or not any(self.responses[bias_type]):
            return 0.0
        
        responses = self.responses[bias_type]
        valid_responses = [r for r in responses if r > 0]
        
        if not valid_responses:
            return 0.0
        
        # 计算平均分并转换为 0-100 分
        avg_score = sum(valid_responses) / len(valid_responses)
        normalized_score = ((avg_score - 1) / 4) * 100  # 1-5 映射到 0-100
        
        return normalized_score
    
    def _get_severity(self, score: float) -> str:
        """根据得分判断严重程度"""
        if score >= self.SEVERITY_THRESHOLDS["critical"]:
            return "critical"
        elif score >= self.SEVERITY_THRESHOLDS["high"]:
            return "high"
        elif score >= self.SEVERITY_THRESHOLDS["medium"]:
            return "medium"
        else:
            return "low"
    
    def _get_level(self, overall_score: float) -> PsychologyScoreLevel:
        """根据总分判断等级"""
        if overall_score >= 80:
            return PsychologyScoreLevel.EXCELLENT
        elif overall_score >= 60:
            return PsychologyScoreLevel.GOOD
        elif overall_score >= 40:
            return PsychologyScoreLevel.FAIR
        elif overall_score >= 20:
            return PsychologyScoreLevel.POOR
        else:
            return PsychologyScoreLevel.CRITICAL
    
    def _generate_recommendations(self, top_risks: List[CognitiveBiasType]) -> List[str]:
        """生成建议"""
        recommendations = []
        
        for bias_type in top_risks[:3]:
            bias = COGNITIVE_BIASES[bias_type]
            if bias_type == CognitiveBiasType.LOSS_AVERSION:
                recommendations.append(
                    f"【{bias.name}】建议建立机械化止损规则，预设止损点后严格执行，"
                    f"可考虑使用条件单自动止损，避免情绪干扰。"
                )
            elif bias_type == CognitiveBiasType.OVERCONFIDENCE:
                recommendations.append(
                    f"【{bias.name}】建议记录每笔交易的决策依据和结果，定期复盘，"
                    f"用数据验证自己的判断准确率，保持谦逊。"
                )
            elif bias_type == CognitiveBiasType.CONFIRMATION_BIAS:
                recommendations.append(
                    f"【{bias.name}】做决策前强制自己列出 3 个反面理由，"
                    f"主动寻找不同观点，避免信息茧房。"
                )
            elif bias_type == CognitiveBiasType.HERD_MENTALITY:
                recommendations.append(
                    f"【{bias.name}】建立独立分析框架，减少看盘和刷消息频率，"
                    f"在市场狂热时保持警惕，逆向思考。"
                )
            elif bias_type == CognitiveBiasType.ANCHORING:
                recommendations.append(
                    f"【{bias.name}】忘记成本价，以当前基本面和技术面重新评估，"
                    f"问自己'如果现在空仓，我会买吗？'"
                )
            elif bias_type == CognitiveBiasType.GAMBLER_FALLACY:
                recommendations.append(
                    f"【{bias.name}】理解每次交易都是独立事件，过去走势不影响未来，"
                    f"避免'该赢了'的心态，坚持概率思维。"
                )
            elif bias_type == CognitiveBiasType.RECENCY_BIAS:
                recommendations.append(
                    f"【{bias.name}】拉长时间周期看数据，参考历史平均值和长期规律，"
                    f"避免被短期波动左右情绪。"
                )
            elif bias_type == CognitiveBiasType.ENDOWMENT_EFFECT:
                recommendations.append(
                    f"【{bias.name}】定期问自己'如果现在不持有，我会买入吗？'，"
                    f"以客观标准评估持仓价值，而非情感依恋。"
                )
        
        # 通用建议
        if len(top_risks) > 0:
            recommendations.append(
                "通用建议：建立交易日志，记录每笔交易的决策过程、情绪状态和结果，"
                "定期复盘识别行为模式，逐步改善。"
            )
        
        return recommendations
    
    def assess(self) -> PsychologyAssessmentResult:
        """
        执行评估
        
        Returns:
            PsychologyAssessmentResult: 评估结果
        """
        from datetime import datetime
        
        bias_scores = []
        weighted_scores = []
        
        # 计算各偏差得分
        for bias_type, weight in self.BIAS_WEIGHTS.items():
            raw_score = self._calculate_bias_score(bias_type)
            severity = self._get_severity(raw_score)
            
            bias_score = BiasScore(
                bias_type=bias_type,
                raw_score=raw_score,
                severity=severity,
                weight=weight
            )
            bias_scores.append(bias_score)
            weighted_scores.append(raw_score * weight)
        
        # 计算总体得分（偏差得分越高，心理状态越差，所以用 100 减）
        total_weighted_score = sum(weighted_scores)
        overall_score = 100 - total_weighted_score
        overall_score = max(0, min(100, overall_score))  # 限制在 0-100
        
        # 排序找出风险最高的偏差
        sorted_scores = sorted(bias_scores, key=lambda x: x.raw_score, reverse=True)
        top_risks = [bs.bias_type for bs in sorted_scores[:3] if bs.raw_score > 0]
        
        # 生成建议
        recommendations = self._generate_recommendations(top_risks)
        
        return PsychologyAssessmentResult(
            overall_score=overall_score,
            level=self._get_level(overall_score),
            bias_scores=bias_scores,
            top_risks=top_risks,
            assessment_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            recommendations=recommendations
        )
    
    def reset(self):
        """重置所有回答"""
        self.responses.clear()


# ==================== 心理测试题库 ====================

@dataclass
class Question:
    """测试题目"""
    question_id: str
    bias_type: CognitiveBiasType
    question_text: str
    options: List[str]  # 选项
    scores: List[int]  # 各选项对应的分数 (1-5)
    explanation: str  # 解析
    
    def to_dict(self) -> dict:
        return {
            "question_id": self.question_id,
            "bias_type": self.bias_type.value,
            "bias_name": COGNITIVE_BIASES[self.bias_type].name,
            "question_text": self.question_text,
            "options": self.options,
            "scores": self.scores,
            "explanation": self.explanation
        }


# 完整题库
PSYCHOLOGY_QUESTION_BANK: List[Question] = [
    # 损失厌恶相关题目
    Question(
        question_id="LA001",
        bias_type=CognitiveBiasType.LOSS_AVERSION,
        question_text="当你的持仓盈利 10% 时，你通常会怎么做？",
        options=[
            "继续持有，让利润奔跑",
            "卖出一部分，锁定部分利润",
            "全部卖出，落袋为安",
            "非常焦虑，担心利润回吐，立即全部卖出"
        ],
        scores=[1, 2, 4, 5],
        explanation="损失厌恶者倾向于过早止盈，害怕已获得的利润消失。理性做法是根据趋势和目標价决策，而非情绪。"
    ),
    Question(
        question_id="LA002",
        bias_type=CognitiveBiasType.LOSS_AVERSION,
        question_text="持仓亏损 20% 且跌破止损位时，你会？",
        options=[
            "立即止损卖出",
            "犹豫但最终止损",
            "再等等看，可能会反弹",
            "坚决不卖，坚信会涨回来"
        ],
        scores=[1, 2, 4, 5],
        explanation="损失厌恶导致人们不愿实现亏损，宁愿继续承担风险。设定并执行止损是克服这一偏差的关键。"
    ),
    Question(
        question_id="LA003",
        bias_type=CognitiveBiasType.LOSS_AVERSION,
        question_text="亏损带来的情绪困扰程度与同等幅度盈利带来的喜悦相比？",
        options=[
            "差不多",
            "亏损稍微更难受一些",
            "亏损的痛苦明显大于盈利的快乐",
            "亏损让我几天都睡不好，盈利只是高兴一会儿"
        ],
        scores=[1, 2, 4, 5],
        explanation="心理学研究表明，损失的痛苦约是同等收益快乐的 2-2.5 倍。意识到这一点有助于理性决策。"
    ),
    
    # 确认偏误相关题目
    Question(
        question_id="CB001",
        bias_type=CognitiveBiasType.CONFIRMATION_BIAS,
        question_text="买入某股票前，你如何收集信息？",
        options=[
            "主动寻找正反两方面的观点",
            "主要看利好，但也瞥一眼利空",
            "主要关注支持自己判断的信息",
            "只看利好的分析，认为利空都是错的"
        ],
        scores=[1, 2, 4, 5],
        explanation="确认偏误使人只接受符合已有观点的信息。强制自己寻找反面证据能提高决策质量。"
    ),
    Question(
        question_id="CB002",
        bias_type=CognitiveBiasType.CONFIRMATION_BIAS,
        question_text="看到不利于自己持仓的消息时，你的第一反应是？",
        options=[
            "认真分析，考虑是否需要调整策略",
            "有些抵触，但还是会看完",
            "质疑消息的可靠性和动机",
            "直接忽略，认为是唱空"
        ],
        scores=[1, 2, 4, 5],
        explanation="对反面信息的抵触是确认偏误的典型表现。保持开放心态，让证据而非立场引导判断。"
    ),
    
    # 过度自信相关题目
    Question(
        question_id="OC001",
        bias_type=CognitiveBiasType.OVERCONFIDENCE,
        question_text="你如何评价自己的投资能力？",
        options=[
            "还在不断学习，市场很难预测",
            "比新手强，但还有很多要学",
            "比大多数散户厉害",
            "我能战胜市场，有独特的洞察力"
        ],
        scores=[1, 2, 4, 5],
        explanation="过度自信是亏损的主要原因之一。保持谦逊，用数据而非感觉评估自己的能力。"
    ),
    Question(
        question_id="OC002",
        bias_type=CognitiveBiasType.OVERCONFIDENCE,
        question_text="连续盈利 3 笔后，你会？",
        options=[
            "保持原有策略和仓位",
            "稍微增加仓位",
            "明显增加仓位，感觉来了",
            "大举加仓，相信自己判断正确"
        ],
        scores=[1, 2, 4, 5],
        explanation="连续盈利后过度自信会导致风险暴露增加。每笔交易都应独立评估，不受之前结果影响。"
    ),
    
    # 锚定效应相关题目
    Question(
        question_id="AN001",
        bias_type=CognitiveBiasType.ANCHORING,
        question_text="判断一笔投资是否成功，你主要看？",
        options=[
            "当前基本面和前景",
            "主要看基本面，偶尔会想起成本价",
            "经常和成本价比较",
            "完全以成本价为参考，高于成本就是成功"
        ],
        scores=[1, 2, 4, 5],
        explanation="成本价是沉没成本，不应影响决策。问自己'如果现在空仓，我会买吗？'"
    ),
    Question(
        question_id="AN002",
        bias_type=CognitiveBiasType.ANCHORING,
        question_text="某股票从 100 元跌到 60 元，你的看法是？",
        options=[
            "以当前价值评估，与历史高点无关",
            "有点便宜了，但还要看基本面",
            "从 100 跌下来，应该很便宜了",
            "相比 100 元的高点，现在肯定是低估"
        ],
        scores=[1, 2, 4, 5],
        explanation="历史高点是锚点，但不代表当前价值。独立评估基本面，而非与过去年份比较。"
    ),
    
    # 从众心理相关题目
    Question(
        question_id="HM001",
        bias_type=CognitiveBiasType.HERD_MENTALITY,
        question_text="某股票突然大涨，群聊里都在讨论，你会？",
        options=[
            "独立分析，不因他人行为而行动",
            "有些心动，但还是先研究",
            "担心错过机会，开始认真考虑买入",
            "立即买入，害怕踏空"
        ],
        scores=[1, 2, 4, 5],
        explanation="FOMO(害怕错过)是从众心理的核心。建立自己的投资框架，减少受他人影响。"
    ),
    Question(
        question_id="HM002",
        bias_type=CognitiveBiasType.HERD_MENTALITY,
        question_text="市场恐慌性大跌时，你通常会？",
        options=[
            "冷静分析，可能寻找机会",
            "有些紧张，但不会盲目操作",
            "感到害怕，考虑减仓",
            "跟随抛售，先出来再说"
        ],
        scores=[1, 2, 4, 5],
        explanation="市场恐慌时从众抛售往往卖在低点。逆向思维需要勇气，但长期来看更有利。"
    ),
    
    # 赌徒谬误相关题目
    Question(
        question_id="GF001",
        bias_type=CognitiveBiasType.GAMBLER_FALLACY,
        question_text="连续亏损 5 笔后，你对下一笔交易的看法是？",
        options=[
            "每笔交易独立，胜率不变",
            "可能运气不好，但理性看待",
            "感觉该赢了，信心增加",
            "肯定该反弹了，加大仓位"
        ],
        scores=[1, 2, 4, 5],
        explanation="每次交易都是独立事件，过去结果不影响未来。避免'该赢了'的赌徒思维。"
    ),
    
    # 近因效应相关题目
    Question(
        question_id="RB001",
        bias_type=CognitiveBiasType.RECENCY_BIAS,
        question_text="市场连续上涨一周后，你对后市的判断是？",
        options=[
            "基于长期数据和估值判断",
            "短期偏乐观，但保持警惕",
            "认为上涨趋势会延续",
            "肯定还会涨，趋势已经形成"
        ],
        scores=[1, 2, 4, 5],
        explanation="近因效应使人线性外推近期走势。拉长时间周期，参考历史平均值更可靠。"
    ),
]


def get_questions_by_bias(bias_type: CognitiveBiasType) -> List[Question]:
    """获取特定偏差类型的题目"""
    return [q for q in PSYCHOLOGY_QUESTION_BANK if q.bias_type == bias_type]


def get_full_assessment_questions() -> List[Question]:
    """获取完整评估所需的所有题目"""
    return PSYCHOLOGY_QUESTION_BANK


def run_sample_assessment():
    """运行示例评估（用于测试）"""
    import random
    
    model = PsychologyScoringModel()
    
    # 模拟用户回答
    for question in PSYCHOLOGY_QUESTION_BANK:
        # 随机选择答案 (1-5)
        score = random.randint(1, 5)
        model.submit_response(question.bias_type, 0, score)
    
    result = model.assess()
    return result.to_dict()


if __name__ == "__main__":
    # 测试代码
    print("=== 交易心理评估模型测试 ===\n")
    
    # 显示认知偏差库
    print(f"认知偏差库包含 {len(COGNITIVE_BIASES)} 种偏差:\n")
    for bias in COGNITIVE_BIASES.values():
        print(f"  - {bias.name} ({bias.name_en}): 风险等级 {bias.risk_level}/5")
    
    print(f"\n题库包含 {len(PSYCHOLOGY_QUESTION_BANK)} 道题目\n")
    
    # 运行示例评估
    result = run_sample_assessment()
    print(f"示例评估结果:")
    print(f"  总体得分：{result['overall_score']}/100")
    print(f"  等级：{result['level']}")
    print(f"  主要风险：{result['top_risks']}")
    print(f"\n建议:")
    for rec in result['recommendations']:
        print(f"  • {rec}")
