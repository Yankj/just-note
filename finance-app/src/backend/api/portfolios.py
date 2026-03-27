"""
投资组合 API 路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.portfolio import Portfolio
from services.portfolio import PortfolioService
from services.auth import AuthService


router = APIRouter(prefix="/portfolios", tags=["投资组合"])


@router.post("/", response_model=dict)
def create_portfolio(
    name: str,
    description: str = None,
    cash_balance: float = 0.0,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """创建投资组合"""
    portfolio = PortfolioService.create_portfolio(
        db=db,
        name=name,
        user_id=current_user.id,
        description=description,
        cash_balance=cash_balance
    )
    
    return {
        "message": "Portfolio created successfully",
        "portfolio_id": portfolio.id,
        "name": portfolio.name
    }


@router.get("/", response_model=List[dict])
def get_portfolios(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """获取当前用户的所有投资组合"""
    portfolios = PortfolioService.get_portfolios_by_user(db, current_user.id)
    return [
        {
            "portfolio_id": p.id,
            "name": p.name,
            "description": p.description,
            "total_value": p.total_value,
            "cash_balance": p.cash_balance,
            "created_at": p.created_at
        }
        for p in portfolios
    ]


@router.get("/{portfolio_id}", response_model=dict)
def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """获取指定投资组合详情"""
    portfolio = PortfolioService.get_portfolio_by_id(db, portfolio_id)
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    # 检查权限
    if portfolio.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this portfolio"
        )
    
    return {
        "portfolio_id": portfolio.id,
        "name": portfolio.name,
        "description": portfolio.description,
        "total_value": portfolio.total_value,
        "cash_balance": portfolio.cash_balance,
        "created_at": portfolio.created_at,
        "updated_at": portfolio.updated_at
    }


@router.put("/{portfolio_id}", response_model=dict)
def update_portfolio(
    portfolio_id: int,
    name: str = None,
    description: str = None,
    cash_balance: float = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """更新投资组合"""
    portfolio = PortfolioService.get_portfolio_by_id(db, portfolio_id)
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    if portfolio.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this portfolio"
        )
    
    update_data = {}
    if name:
        update_data["name"] = name
    if description:
        update_data["description"] = description
    if cash_balance is not None:
        update_data["cash_balance"] = cash_balance
    
    portfolio = PortfolioService.update_portfolio(db, portfolio_id, **update_data)
    
    return {
        "message": "Portfolio updated successfully",
        "portfolio_id": portfolio.id
    }


@router.delete("/{portfolio_id}")
def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """删除投资组合"""
    portfolio = PortfolioService.get_portfolio_by_id(db, portfolio_id)
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    if portfolio.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this portfolio"
        )
    
    success = PortfolioService.delete_portfolio(db, portfolio_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    return {"message": "Portfolio deleted successfully"}
