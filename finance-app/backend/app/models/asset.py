"""
资产模型
"""
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import Boolean, String, Numeric, ForeignKey, UniqueConstraint, Index, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Asset(Base):
    """资产表"""
    
    __tablename__ = "assets"
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # 资产标识
    asset_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    symbol: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    market: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # 持仓信息
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6), default=0)
    avg_cost: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=0)
    current_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)
    market_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    
    # 盈亏
    unrealized_pnl: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    unrealized_pnl_pct: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 4), nullable=True)
    realized_pnl: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    
    # 状态
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 审计
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # 关系 (暂时移除，避免循环依赖)
    # user = relationship("User", backref="assets")
    # transactions = relationship("Transaction", back_populates="asset", cascade="all, delete-orphan")
    
    # 约束
    __table_args__ = (
        UniqueConstraint('user_id', 'asset_type', 'symbol', 'market', name='uk_assets_user_type_symbol_market'),
        Index('idx_assets_user_active', 'user_id', 'is_active'),
    )
    
    def __repr__(self) -> str:
        return f"<Asset {self.symbol} ({self.name})>"
