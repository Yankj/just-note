"""
交易数据模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
import enum

from database import Base


class TransactionType(str, enum.Enum):
    """交易类型枚举"""
    BUY = "buy"
    SELL = "sell"
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    DIVIDEND = "dividend"


class Transaction(Base):
    """交易记录表"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)  # 股票代码
    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    fee = Column(Float, default=0.0)
    notes = Column(String(500))
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联关系
    portfolio = relationship("Portfolio", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, symbol={self.symbol}, type={self.transaction_type})>"
