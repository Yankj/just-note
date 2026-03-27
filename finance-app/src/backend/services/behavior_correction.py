"""
行为矫正方案生成器
Behavior Correction Plan Generator

负责：
1. 根据心理评估结果生成个性化行为矫正方案
2. 提供具体的训练计划和执行建议
3. 跟踪矫正进度和效果评估
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json
from datetime import datetime, timedelta

from .psychology_model import (
    CognitiveBiasType, 
    CognitiveBias, 
    COGNITIVE_BIASES,
    PsychologyAssessmentResult,
    BiasScore
)


# ==================== 矫正方案数据结构 ====================

class CorrectionPhase(Enum):
    """矫正阶段"""
    AWARENESS = "awareness"  # 意识觉醒期 (第 1-2 周)
    TRAINING = "training"  # 刻意训练期 (第 3-6 周)
    HABIT = "habit"  # 习惯养成期 (第 7-12 周)
    MAINTENANCE = "maintenance"  # 长期维护期 (12 周后)


class DifficultyLevel(Enum):
    """难度等级"""
    EASY = "easy"  # 简单
    MEDIUM = "medium"  # 中等
    HARD = "hard"  # 困难


@dataclass
class CorrectionTask:
    """矫正任务"""
    task_id: str
    title: str
    description: str
    bias_type: CognitiveBiasType
    phase: CorrectionPhase
    difficulty: DifficultyLevel
    estimated_days: int  # 预计完成天数
    action_steps: List[str]  # 具体行动步骤
    success_criteria: str  # 成功标准
    tracking_method: str  # 追踪方法
    
    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "bias_type": self.bias_type.value,
            "bias_name": COGNITIVE_BIASES[self.bias_type].name,
            "phase": self.phase.value,
            "difficulty": self.difficulty.value,
            "estimated_days": self.estimated_days,
            "action_steps": self.action_steps,
            "success_criteria": self.success_criteria,
            "tracking_method": self.tracking_method
        }


@dataclass
class DailyCheckIn:
    """每日打卡"""
    date: str
    tasks_completed: List[str]  # 完成的任务 ID
    mood_score: int  # 情绪评分 1-10
    trading_decisions_made: int  # 做出的交易决策数
    impulsive_actions: int  # 冲动行为次数
    notes: str  # 备注
    
    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "tasks_completed": self.tasks_completed,
            "mood_score": self.mood_score,
            "trading_decisions_made": self.trading_decisions_made,
            "impulsive_actions": self.impulsive_actions,
            "notes": self.notes
        }


@dataclass
class CorrectionPlan:
    """矫正方案"""
    plan_id: str
    user_id: str
    assessment_result: PsychologyAssessmentResult
    created_date: str
    target_biases: List[CognitiveBiasType]
    tasks: List[CorrectionTask]
    estimated_weeks: int
    milestones: List[dict]  # 里程碑
    status: str  # active/completed/paused
    
    def to_dict(self) -> dict:
        return {
            "plan_id": self.plan_id,
            "user_id": self.user_id,
            "assessment_date": self.assessment_result.assessment_date,
            "overall_score": self.assessment_result.overall_score,
            "level": self.assessment_result.level.value,
            "created_date": self.created_date,
            "target_biases": [tb.value for tb in self.target_biases],
            "tasks": [t.to_dict() for t in self.tasks],
            "estimated_weeks": self.estimated_weeks,
            "milestones": self.milestones,
            "status": self.status
        }


# ==================== 矫正任务库 ====================

CORRECTION_TASK_LIBRARY: Dict[CognitiveBiasType, List[CorrectionTask]] = {
    CognitiveBiasType.LOSS_AVERSION: [
        CorrectionTask(
            task_id="LA_T1",
            title="建立机械化止损规则",
            description="通过预设止损点和条件单，克服不愿止损的心理障碍。",
            bias_type=CognitiveBiasType.LOSS_AVERSION,
            phase=CorrectionPhase.AWARENESS,
            difficulty=DifficultyLevel.MEDIUM,
            estimated_days=7,
            action_steps=[
                "学习并理解止损的重要性（阅读相关材料）",
                "为每笔交易预设明确的止损点（如 -8%）",
                "使用条件单/止损单自动执行，避免手动操作",
                "记录每次止损后的市场走势，验证止损决策"
            ],
            success_criteria="连续 2 周严格执行预设止损，无一次例外",
            tracking_method="交易日志记录止损执行情况"
        ),
        CorrectionTask(
            task_id="LA_T2",
            title="盈利保护训练",
            description="学习让利润奔跑，避免过早止盈。",
            bias_type=CognitiveBiasType.LOSS_AVERSION,
            phase=CorrectionPhase.TRAINING,
            difficulty=DifficultyLevel.MEDIUM,
            estimated_days=14,
            action_steps=[
                "设定目标价而非固定止盈点",
                "使用移动止盈（追踪止损）保护利润",
                "分批止盈而非一次性全部卖出",
                "记录过早止盈后错过的涨幅"
            ],
            success_criteria="盈利交易中持有超过目标涨幅的比例达到 60%",
            tracking_method="统计止盈时机与最佳时机的差距"
        ),
        CorrectionTask(
            task_id="LA_T3",
            title="损失情绪脱敏",
            description="通过认知重构减少对损失的情绪反应。",
            bias_type=CognitiveBiasType.LOSS_AVERSION,
            phase=CorrectionPhase.HABIT,
            difficulty=DifficultyLevel.HARD,
            estimated_days=21,
            action_steps=[
                "每次亏损后写情绪日记，记录感受",
                "将亏损重新定义为'学费'和'数据点'",
                "练习正念冥想，观察情绪而不被控制",
                "计算长期期望值，接受单笔亏损是正常概率"
            ],
            success_criteria="亏损后情绪恢复时间缩短至 24 小时内",
            tracking_method="情绪日记 + 恢复时间记录"
        )
    ],
    
    CognitiveBiasType.OVERCONFIDENCE: [
        CorrectionTask(
            task_id="OC_T1",
            title="交易日志训练",
            description="记录每笔交易的决策依据，用数据验证判断准确率。",
            bias_type=CognitiveBiasType.OVERCONFIDENCE,
            phase=CorrectionPhase.AWARENESS,
            difficulty=DifficultyLevel.EASY,
            estimated_days=14,
            action_steps=[
                "每笔交易前写下买入理由和预期",
                "记录决策时的信心程度（1-10 分）",
                "交易结束后对比预期与实际结果",
                "每周统计预测准确率"
            ],
            success_criteria="完成至少 20 笔交易的完整记录",
            tracking_method="交易日志完成率 + 准确率统计"
        ),
        CorrectionTask(
            task_id="OC_T2",
            title="谦逊练习",
            description="主动寻找自己错误的证据，保持开放心态。",
            bias_type=CognitiveBiasType.OVERCONFIDENCE,
            phase=CorrectionPhase.TRAINING,
            difficulty=DifficultyLevel.MEDIUM,
            estimated_days=14,
            action_steps=[
                "每笔交易前列出 3 个可能出错的理由",
                "定期复盘错误交易，分析原因",
                "阅读与自己观点相反的分析",
                "承认并记录自己的错误判断"
            ],
            success_criteria="能够坦然承认错误，不找借口",
            tracking_method="错误承认次数 + 复盘深度"
        ),
        CorrectionTask(
            task_id="OC_T3",
            title="仓位控制训练",
            description="严格执行仓位管理，避免因自信而过度暴露风险。",
            bias_type=CognitiveBiasType.OVERCONFIDENCE,
            phase=CorrectionPhase.HABIT,
            difficulty=DifficultyLevel.MEDIUM,
            estimated_days=21,
            action_steps=[
                "设定单只股票最大仓位（如 20%）",
                "设定总仓位上限（如 80%）",
                "无论多自信都不突破仓位限制",
                "记录突破冲动的时刻和原因"
            ],
            success_criteria="连续 4 周无一次突破仓位限制",
            tracking_method="仓位记录 + 冲动日志"
        )
    ],
    
    CognitiveBiasType.CONFIRMATION_BIAS: [
        CorrectionTask(
            task_id="CB_T1",
            title="反面证据搜集",
            description="强制自己寻找与已有观点相反的信息。",
            bias_type=CognitiveBiasType.CONFIRMATION_BIAS,
            phase=CorrectionPhase.AWARENESS,
            difficulty=DifficultyLevel.MEDIUM,
            estimated_days=10,
            action_steps=[
                "做决策前搜索'XXX 股票 风险'或'XXX 利空'",
                "关注至少 2 个与自己观点相反的分析师",
                "列出支持反面观点的 3 个最强论据",
                "问自己'什么证据会改变我的想法'"
            ],
            success_criteria="每笔交易前都完成反面证据搜集",
            tracking_method="反面证据记录完整性"
        ),
        CorrectionTask(
            task_id="CB_T2",
            title="信息源多样化",
            description="打破信息茧房，接触多元观点。",
            bias_type=CognitiveBiasType.CONFIRMATION_BIAS,
            phase=CorrectionPhase.TRAINING,
            difficulty=DifficultyLevel.EASY,
            estimated_days=14,
            action_steps=[
                "关注不同立场的媒体和分析师",
                "加入有不同观点的投资社群",
                "定期阅读看空报告即使你看多",
                "记录观点改变的时刻和原因"
            ],
            success_criteria="信息源覆盖至少 3 种不同立场",
            tracking_method="信息源清单 + 观点变化记录"
        )
    ],
    
    CognitiveBiasType.HERD_MENTALITY: [
        CorrectionTask(
            task_id="HM_T1",
            title="独立分析框架",
            description="建立自己的分析框架，减少受他人影响。",
            bias_type=CognitiveBiasType.HERD_MENTALITY,
            phase=CorrectionPhase.AWARENESS,
            difficulty=DifficultyLevel.MEDIUM,
            estimated_days=14,
            action_steps=[
                "写下自己的投资标准和原则",
                "每笔交易必须有自己的分析依据",
                "减少看盘和刷消息的频率",
                "记录受他人影响做出的决策及结果"
            ],
            success_criteria="80% 的交易决策基于独立分析",
            tracking_method="决策依据记录"
        ),
        CorrectionTask(
            task_id="HM_T2",
            title="FOMO 抵抗训练",
            description="学会错过，避免害怕错过机会而盲目入场。",
            bias_type=CognitiveBiasType.HERD_MENTALITY,
            phase=CorrectionPhase.TRAINING,
            difficulty=DifficultyLevel.HARD,
            estimated_days=21,
            action_steps=[
                "理解'机会永远都有'的理念",
                "错过牛股后记录情绪和想法",
                "练习主动错过不符合标准的'机会'",
                "统计追涨杀跌的亏损 vs 等待的收获"
            ],
            success_criteria="能够坦然错过不符合标准的上涨",
            tracking_method="FOMO 冲动记录 + 抵抗成功次数"
        ),
        CorrectionTask(
            task_id="HM_T3",
            title="逆向思维练习",
            description="在市场极端情绪时练习逆向思考。",
            bias_type=CognitiveBiasType.HERD_MENTALITY,
            phase=CorrectionPhase.HABIT,
            difficulty=DifficultyLevel.HARD,
            estimated_days=28,
            action_steps=[
                "学习市场情绪指标（如恐慌指数）",
                "在市场狂热时列出风险因素",
                "在市场恐慌时寻找机会",
                "记录逆向思考的决策和结果"
            ],
            success_criteria="至少完成 3 次成功的逆向操作",
            tracking_method="逆向决策记录 + 结果分析"
        )
    ],
    
    CognitiveBiasType.ANCHORING: [
        CorrectionTask(
            task_id="AN_T1",
            title="忘记成本价练习",
            description="学会以当前价值而非成本价评估持仓。",
            bias_type=CognitiveBiasType.ANCHORING,
            phase=CorrectionPhase.AWARENESS,
            difficulty=DifficultyLevel.MEDIUM,
            estimated_days=10,
            action_steps=[
                "每次评估持仓时遮住成本价",
                "问自己'如果现在空仓，我会买吗？'",
                "以当前基本面重新估值",
                "记录基于成本价决策的错误案例"
            ],
            success_criteria="能够不看成本价做出持仓决策",
            tracking_method="决策时是否参考成本价的记录"
        ),
        CorrectionTask(
            task_id="AN_T2",
            title="历史价格脱锚",
            description="摆脱历史高点/低点的锚定影响。",
            bias_type=CognitiveBiasType.ANCHORING,
            phase=CorrectionPhase.TRAINING,
            difficulty=DifficultyLevel.MEDIUM,
            estimated_days=14,
            action_steps=[
                "分析股票时不看历史 K 线",
                "基于未来现金流而非过去年份估值",
                "理解'便宜'不等于'从高点跌了很多'",
                "记录被历史价格锚定的错误判断"
            ],
            success_criteria="估值时不再参考历史价格",
            tracking_method="估值依据记录"
        )
    ],
    
    CognitiveBiasType.GAMBLER_FALLACY: [
        CorrectionTask(
            task_id="GF_T1",
            title="独立事件理解",
            description="深刻理解每次交易都是独立事件。",
            bias_type=CognitiveBiasType.GAMBLER_FALLACY,
            phase=CorrectionPhase.AWARENESS,
            difficulty=DifficultyLevel.EASY,
            estimated_days=7,
            action_steps=[
                "学习概率论基础知识",
                "理解'赌徒谬误'的数学原理",
                "记录连续亏损/盈利后的心理变化",
                "用抛硬币实验感受独立性"
            ],
            success_criteria="能够清晰解释为什么过去不影响未来",
            tracking_method="理解测试 + 心理记录"
        ),
        CorrectionTask(
            task_id="GF_T2",
            title="概率思维训练",
            description="用概率而非确定性思考市场。",
            bias_type=CognitiveBiasType.GAMBLER_FALLACY,
            phase=CorrectionPhase.TRAINING,
            difficulty=DifficultyLevel.MEDIUM,
            estimated_days=14,
            action_steps=[
                "每笔交易用概率表达预期（如 60% 可能上涨）",
                "理解期望值概念并应用",
                "接受亏损是概率游戏的一部分",
                "记录'该赢了'心态导致的错误"
            ],
            success_criteria="不再使用'肯定''一定'等绝对词汇",
            tracking_method="决策语言记录 + 期望值计算"
        )
    ],
    
    CognitiveBiasType.RECENCY_BIAS: [
        CorrectionTask(
            task_id="RB_T1",
            title="长期视角训练",
            description="拉长时间周期看数据，避免被短期波动左右。",
            bias_type=CognitiveBiasType.RECENCY_BIAS,
            phase=CorrectionPhase.AWARENESS,
            difficulty=DifficultyLevel.EASY,
            estimated_days=10,
            action_steps=[
                "分析时至少看 3-5 年历史数据",
                "关注长期平均值而非近期表现",
                "减少看盘频率（如每周一次）",
                "记录被短期波动误导的决策"
            ],
            success_criteria="决策时参考长期数据而非近期走势",
            tracking_method="决策依据时间跨度记录"
        ),
        CorrectionTask(
            task_id="RB_T2",
            title="均值回归理解",
            description="理解市场长期均值回归的规律。",
            bias_type=CognitiveBiasType.RECENCY_BIAS,
            phase=CorrectionPhase.TRAINING,
            difficulty=DifficultyLevel.MEDIUM,
            estimated_days=14,
            action_steps=[
                "学习历史估值区间和均值",
                "在极端估值时保持警惕",
                "理解'这次不一样'的危险性",
                "记录线性外推错误的案例"
            ],
            success_criteria="在极端行情时能够逆向思考",
            tracking_method="极端行情决策记录"
        )
    ],
    
    CognitiveBiasType.ENDOWMENT_EFFECT: [
        CorrectionTask(
            task_id="EE_T1",
            title="零基思考练习",
            description="定期以零基视角重新评估持仓。",
            bias_type=CognitiveBiasType.ENDOWMENT_EFFECT,
            phase=CorrectionPhase.AWARENESS,
            difficulty=DifficultyLevel.MEDIUM,
            estimated_days=10,
            action_steps=[
                "每周问自己'如果现在不持有，我会买吗？'",
                "假设继承一笔持仓，决定是否保留",
                "换仓时比较新旧持仓的优劣",
                "记录因情感依恋而持有的错误案例"
            ],
            success_criteria="能够客观评估持仓，不因持有时长而偏爱",
            tracking_method="零基思考记录"
        )
    ]
}


# ==================== 行为矫正方案生成器 ====================

class BehaviorCorrectionGenerator:
    """行为矫正方案生成器"""
    
    # 各阶段建议时长（周）
    PHASE_DURATION = {
        CorrectionPhase.AWARENESS: 2,
        CorrectionPhase.TRAINING: 4,
        CorrectionPhase.HABIT: 6,
        CorrectionPhase.MAINTENANCE: 12
    }
    
    def __init__(self):
        self.plans: Dict[str, CorrectionPlan] = {}
        self.checkins: Dict[str, List[DailyCheckIn]] = {}
    
    def generate_plan(self, user_id: str, assessment: PsychologyAssessmentResult) -> CorrectionPlan:
        """
        根据评估结果生成个性化矫正方案
        
        Args:
            user_id: 用户 ID
            assessment: 心理评估结果
            
        Returns:
            CorrectionPlan: 矫正方案
        """
        import uuid
        
        plan_id = str(uuid.uuid4())[:8]
        target_biases = assessment.top_risks
        
        # 根据风险等级选择任务
        tasks = []
        for bias_type in target_biases:
            if bias_type in CORRECTION_TASK_LIBRARY:
                bias_tasks = CORRECTION_TASK_LIBRARY[bias_type]
                # 根据严重程度选择任务数量
                bias_score = next(
                    (bs for bs in assessment.bias_scores if bs.bias_type == bias_type),
                    None
                )
                if bias_score:
                    if bias_score.severity in ["critical", "high"]:
                        # 高风险：所有任务
                        tasks.extend(bias_tasks)
                    elif bias_score.severity == "medium":
                        # 中等风险：前两个阶段任务
                        tasks.extend([t for t in bias_tasks if t.phase in [
                            CorrectionPhase.AWARENESS, 
                            CorrectionPhase.TRAINING
                        ]])
                    else:
                        # 低风险：只需意识觉醒
                        tasks.extend([t for t in bias_tasks if t.phase == CorrectionPhase.AWARENESS])
        
        # 按阶段排序任务
        phase_order = {
            CorrectionPhase.AWARENESS: 0,
            CorrectionPhase.TRAINING: 1,
            CorrectionPhase.HABIT: 2,
            CorrectionPhase.MAINTENANCE: 3
        }
        tasks.sort(key=lambda t: (phase_order[t.phase], t.estimated_days))
        
        # 计算总时长
        total_days = sum(t.estimated_days for t in tasks)
        estimated_weeks = max(12, total_days // 7)  # 至少 12 周
        
        # 生成里程碑
        milestones = self._generate_milestones(tasks, estimated_weeks)
        
        plan = CorrectionPlan(
            plan_id=plan_id,
            user_id=user_id,
            assessment_result=assessment,
            created_date=datetime.now().strftime("%Y-%m-%d"),
            target_biases=target_biases,
            tasks=tasks,
            estimated_weeks=estimated_weeks,
            milestones=milestones,
            status="active"
        )
        
        self.plans[plan_id] = plan
        self.checkins[plan_id] = []
        
        return plan
    
    def _generate_milestones(self, tasks: List[CorrectionTask], total_weeks: int) -> List[dict]:
        """生成里程碑"""
        milestones = []
        
        # 阶段里程碑
        phases = [
            (CorrectionPhase.AWARENESS, "意识觉醒", "完成意识觉醒期训练，能够识别自己的认知偏差"),
            (CorrectionPhase.TRAINING, "刻意训练", "完成核心训练任务，建立新的行为模式"),
            (CorrectionPhase.HABIT, "习惯养成", "新行为成为习惯，不再需要刻意坚持"),
            (CorrectionPhase.MAINTENANCE, "长期维护", "形成长期稳定的交易心理状态")
        ]
        
        phase_weeks = {p: sum(t.estimated_days for t in tasks if t.phase == p) // 7 
                       for p, _, _ in phases}
        
        current_week = 0
        for phase, name, description in phases:
            weeks = max(2, phase_weeks.get(phase, 2))
            current_week += weeks
            milestones.append({
                "phase": phase.value,
                "name": name,
                "description": description,
                "target_week": min(current_week, total_weeks),
                "status": "pending"
            })
        
        return milestones
    
    def submit_checkin(self, plan_id: str, checkin: DailyCheckIn) -> bool:
        """提交每日打卡"""
        if plan_id not in self.checkins:
            return False
        
        self.checkins[plan_id].append(checkin)
        return True
    
    def get_progress(self, plan_id: str) -> dict:
        """获取矫正进度"""
        if plan_id not in self.plans:
            return {"error": "Plan not found"}
        
        plan = self.plans[plan_id]
        checkins = self.checkins.get(plan_id, [])
        
        # 计算任务完成度
        completed_task_ids = set()
        for checkin in checkins:
            completed_task_ids.update(checkin.tasks_completed)
        
        total_tasks = len(plan.tasks)
        completed_tasks = len([t for t in plan.tasks if t.task_id in completed_task_ids])
        
        # 计算当前阶段
        current_phase = CorrectionPhase.AWARENESS
        for task in plan.tasks:
            if task.task_id in completed_task_ids:
                current_phase = task.phase
            else:
                break
        
        # 统计打卡数据
        total_checkins = len(checkins)
        avg_mood = sum(c.mood_score for c in checkins) / total_checkins if checkins else 0
        total_impulsive = sum(c.impulsive_actions for c in checkins)
        
        return {
            "plan_id": plan_id,
            "status": plan.status,
            "current_phase": current_phase.value,
            "progress_percentage": round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0,
            "completed_tasks": completed_tasks,
            "total_tasks": total_tasks,
            "total_checkins": total_checkins,
            "avg_mood_score": round(avg_mood, 1),
            "total_impulsive_actions": total_impulsive,
            "estimated_weeks": plan.estimated_weeks,
            "milestones": plan.milestones
        }
    
    def get_daily_tasks(self, plan_id: str, current_phase: Optional[CorrectionPhase] = None) -> List[CorrectionTask]:
        """获取当前阶段的任务"""
        if plan_id not in self.plans:
            return []
        
        plan = self.plans[plan_id]
        
        if current_phase is None:
            # 根据打卡记录推断当前阶段
            checkins = self.checkins.get(plan_id, [])
            completed_task_ids = set()
            for checkin in checkins:
                completed_task_ids.update(checkin.tasks_completed)
            
            # 找到第一个未完成的任务的阶段
            for task in plan.tasks:
                if task.task_id not in completed_task_ids:
                    current_phase = task.phase
                    break
            else:
                return []  # 所有任务已完成
        
        # 返回当前阶段的任务
        return [t for t in plan.tasks if t.phase == current_phase]
    
    def evaluate_improvement(self, plan_id: str) -> dict:
        """评估改善效果"""
        if plan_id not in self.checkins:
            return {"error": "No checkins found"}
        
        checkins = self.checkins[plan_id]
        if len(checkins) < 14:  # 至少 2 周数据
            return {"error": "Insufficient data (need at least 14 days)"}
        
        # 比较第一周和最后一周
        first_week = checkins[:7]
        last_week = checkins[-7:]
        
        first_avg_impulsive = sum(c.impulsive_actions for c in first_week) / 7
        last_avg_impulsive = sum(c.impulsive_actions for c in last_week) / 7
        
        first_avg_mood = sum(c.mood_score for c in first_week) / 7
        last_avg_mood = sum(c.mood_score for c in last_week) / 7
        
        improvement_rate = ((first_avg_impulsive - last_avg_impulsive) / first_avg_impulsive * 100) if first_avg_impulsive > 0 else 0
        
        return {
            "evaluation_date": datetime.now().strftime("%Y-%m-%d"),
            "days_tracked": len(checkins),
            "first_week": {
                "avg_impulsive_actions": round(first_avg_impulsive, 2),
                "avg_mood_score": round(first_avg_mood, 1)
            },
            "last_week": {
                "avg_impulsive_actions": round(last_avg_impulsive, 2),
                "avg_mood_score": round(last_avg_mood, 1)
            },
            "improvement": {
                "impulsive_action_reduction": f"{improvement_rate:.1f}%",
                "mood_improvement": round(last_avg_mood - first_avg_mood, 1),
                "overall_trend": "improving" if improvement_rate > 0 else "needs_attention"
            }
        }


# ==================== 便捷函数 ====================

def create_correction_plan(user_id: str, assessment: PsychologyAssessmentResult) -> CorrectionPlan:
    """创建矫正方案的便捷函数"""
    generator = BehaviorCorrectionGenerator()
    return generator.generate_plan(user_id, assessment)


def get_bias_correction_tasks(bias_type: CognitiveBiasType) -> List[CorrectionTask]:
    """获取特定偏差的矫正任务"""
    return CORRECTION_TASK_LIBRARY.get(bias_type, [])


def run_sample_correction():
    """运行示例矫正方案生成（用于测试）"""
    from .psychology_model import PsychologyScoringModel, run_sample_assessment
    
    # 生成示例评估
    assessment_dict = run_sample_assessment()
    
    # 创建简化的评估对象用于测试
    class MockAssessment:
        def __init__(self, d):
            self.overall_score = d['overall_score']
            self.level = type('obj', (object,), {'value': d['level']})()
            self.top_risks = [CognitiveBiasType(r) for r in d['top_risks'][:3]]
            self.bias_scores = []
            self.assessment_date = d['assessment_date']
            self.recommendations = d['recommendations']
    
    assessment = MockAssessment(assessment_dict)
    
    # 生成矫正方案
    generator = BehaviorCorrectionGenerator()
    plan = generator.generate_plan("test_user", assessment)
    
    return plan.to_dict()


if __name__ == "__main__":
    # 测试代码
    print("=== 行为矫正方案生成器测试 ===\n")
    
    # 显示任务库
    print("矫正任务库:")
    for bias_type, tasks in CORRECTION_TASK_LIBRARY.items():
        bias = COGNITIVE_BIASES[bias_type]
        print(f"\n  {bias.name} ({bias.name_en}):")
        for task in tasks:
            print(f"    - [{task.phase.value}] {task.title} ({task.estimated_days}天)")
    
    print("\n\n=== 示例矫正方案 ===\n")
    
    # 运行示例
    plan = run_sample_correction()
    print(f"方案 ID: {plan['plan_id']}")
    print(f"目标偏差：{plan['target_biases']}")
    print(f"任务数量：{len(plan['tasks'])}")
    print(f"预计周期：{plan['estimated_weeks']}周")
    print(f"\n里程碑:")
    for ms in plan['milestones']:
        print(f"  - 第{ms['target_week']}周：{ms['name']} - {ms['description']}")
