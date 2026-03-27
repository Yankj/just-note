"""
交易记录模型
"""
import uuid
from datetime import datetime, date, time
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Numeric, Date, Time, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Transaction(Base):
    """交易记录表"""
    
    __tablename__ = "transactions"
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # 交易信息
    tx_type: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    tx_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    tx_time: Mapped[time] = mapped_column(Time, default=time(0, 0, 0))
    
    # 交易详情
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    fee: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    currency: Mapped[str] = mapped_column(String(3), default="CNY")
    
    # 交易场所
    broker: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    order_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # 关系 (暂时移除)
    # user = relationship("User", backref="transactions")
    # asset = relationship("Asset", backref="transactions")
    
    # 约束
    __table_args__ = (
        CheckConstraint('quantity > 0', name='chk_tx_quantity_positive'),
        CheckConstraint('price >= 0', name='chk_tx_price_positive'),
        CheckConstraint('amount >= 0', name='chk_tx_amount_positive'),
    )
    
    def __repr__(self) -> str:
        return f"<Transaction {self.tx_type} {self.symbol}>"
