"""
交易 API 路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.transaction import Transaction, TransactionType
from services.transaction import TransactionService
from services.portfolio import PortfolioService
from services.auth import AuthService


router = APIRouter(prefix="/transactions", tags=["交易记录"])


@router.post("/", response_model=dict)
def create_transaction(
    symbol: str,
    transaction_type: TransactionType,
    quantity: float,
    price: float,
    portfolio_id: int,
    fee: float = 0.0,
    notes: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """创建交易记录"""
    # 验证投资组合归属
    portfolio = PortfolioService.get_portfolio_by_id(db, portfolio_id)
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    if portfolio.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add transactions to this portfolio"
        )
    
    transaction = TransactionService.create_transaction(
        db=db,
        symbol=symbol,
        transaction_type=transaction_type,
        quantity=quantity,
        price=price,
        portfolio_id=portfolio_id,
        fee=fee,
        notes=notes
    )
    
    return {
        "message": "Transaction created successfully",
        "transaction_id": transaction.id,
        "symbol": transaction.symbol,
        "type": transaction.transaction_type.value
    }


@router.get("/", response_model=List[dict])
def get_transactions(
    portfolio_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """获取交易记录列表"""
    # 验证投资组合归属
    portfolio = PortfolioService.get_portfolio_by_id(db, portfolio_id)
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    if portfolio.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this portfolio's transactions"
        )
    
    transactions = TransactionService.get_transactions_by_portfolio(
        db, portfolio_id, skip=skip, limit=limit
    )
    
    return [
        {
            "transaction_id": t.id,
            "symbol": t.symbol,
            "type": t.transaction_type.value,
            "quantity": t.quantity,
            "price": t.price,
            "total_amount": t.total_amount,
            "fee": t.fee,
            "notes": t.notes,
            "transaction_date": t.transaction_date
        }
        for t in transactions
    ]


@router.get("/{transaction_id}", response_model=dict)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """获取单条交易记录"""
    transaction = TransactionService.get_transaction_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # 验证投资组合归属
    portfolio = PortfolioService.get_portfolio_by_id(db, transaction.portfolio_id)
    if portfolio.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this transaction"
        )
    
    return {
        "transaction_id": transaction.id,
        "symbol": transaction.symbol,
        "type": transaction.transaction_type.value,
        "quantity": transaction.quantity,
        "price": transaction.price,
        "total_amount": transaction.total_amount,
        "fee": transaction.fee,
        "notes": transaction.notes,
        "transaction_date": transaction.transaction_date
    }


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """删除交易记录"""
    transaction = TransactionService.get_transaction_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # 验证投资组合归属
    portfolio = PortfolioService.get_portfolio_by_id(db, transaction.portfolio_id)
    if portfolio.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this transaction"
        )
    
    success = TransactionService.delete_transaction(db, transaction_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return {"message": "Transaction deleted successfully"}
