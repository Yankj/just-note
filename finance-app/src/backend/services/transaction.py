"""
交易服务
"""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

from models.transaction import Transaction, TransactionType


class TransactionService:
    """交易服务"""
    
    @staticmethod
    def create_transaction(
        db: Session,
        symbol: str,
        transaction_type: TransactionType,
        quantity: float,
        price: float,
        portfolio_id: int,
        fee: float = 0.0,
        notes: str = None
    ) -> Transaction:
        """创建交易记录"""
        total_amount = quantity * price + fee
        
        transaction = Transaction(
            symbol=symbol,
            transaction_type=transaction_type,
            quantity=quantity,
            price=price,
            total_amount=total_amount,
            fee=fee,
            notes=notes,
            portfolio_id=portfolio_id
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    
    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: int) -> Optional[Transaction]:
        """根据 ID 获取交易"""
        return db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    @staticmethod
    def get_transactions_by_portfolio(
        db: Session,
        portfolio_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Transaction]:
        """获取投资组合的交易记录"""
        return db.query(Transaction)\
            .filter(Transaction.portfolio_id == portfolio_id)\
            .order_by(Transaction.transaction_date.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_transactions_by_symbol(
        db: Session,
        portfolio_id: int,
        symbol: str
    ) -> List[Transaction]:
        """获取某股票的交易记录"""
        return db.query(Transaction)\
            .filter(Transaction.portfolio_id == portfolio_id)\
            .filter(Transaction.symbol == symbol)\
            .order_by(Transaction.transaction_date.desc())\
            .all()
    
    @staticmethod
    def delete_transaction(db: Session, transaction_id: int) -> bool:
        """删除交易记录"""
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if transaction:
            db.delete(transaction)
            db.commit()
            return True
        return False
