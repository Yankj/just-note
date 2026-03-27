"""
投资日记模型
"""
import uuid
from datetime import datetime, date
from typing import Optional, List

from sqlalchemy import String, Text, Date, Boolean, ForeignKey, CheckConstraint, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class InvestmentDiary(Base):
    """投资日记表"""
    
    __tablename__ = "investment_diaries"
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # 日记内容
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    diary_type: Mapped[str] = mapped_column(String(20), default="REFLECTION", index=True)
    
    # 关联
    related_assets: Mapped[Optional[List[uuid.UUID]]] = mapped_column(
        ARRAY(UUID(as_uuid=True)), nullable=True
    )
    related_tx_ids: Mapped[Optional[List[uuid.UUID]]] = mapped_column(
        ARRAY(UUID(as_uuid=True)), nullable=True
    )
    
    # 标签与分类
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String(50)), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # 情绪与评分
    sentiment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    confidence_score: Mapped[Optional[int]] = mapped_column(nullable=True)
    
    # 状态
    is_private: Mapped[bool] = mapped_column(Boolean, default=True)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 审计
    diary_date: Mapped[date] = mapped_column(Date, default=date.today, index=True)
    
    # 关系 (暂时移除)
    # user = relationship("User", backref="diaries")
    
    # 约束
    __table_args__ = (
        CheckConstraint('confidence_score >= 1 AND confidence_score <= 10', name='chk_diary_confidence_score'),
    )
    
    def __repr__(self) -> str:
        return f"<InvestmentDiary {self.title}>"
