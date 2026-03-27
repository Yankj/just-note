"""
投资组合服务
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from models.portfolio import Portfolio


class PortfolioService:
    """投资组合服务"""
    
    @staticmethod
    def create_portfolio(
        db: Session,
        name: str,
        user_id: int,
        description: str = None,
        cash_balance: float = 0.0
    ) -> Portfolio:
        """创建投资组合"""
        portfolio = Portfolio(
            name=name,
            description=description,
            cash_balance=cash_balance,
            user_id=user_id
        )
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
        return portfolio
    
    @staticmethod
    def get_portfolio_by_id(db: Session, portfolio_id: int) -> Optional[Portfolio]:
        """根据 ID 获取投资组合"""
        return db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    
    @staticmethod
    def get_portfolios_by_user(db: Session, user_id: int) -> List[Portfolio]:
        """获取用户的所有投资组合"""
        return db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
    
    @staticmethod
    def update_portfolio(db: Session, portfolio_id: int, **kwargs) -> Optional[Portfolio]:
        """更新投资组合"""
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if portfolio:
            for key, value in kwargs.items():
                if hasattr(portfolio, key):
                    setattr(portfolio, key, value)
            db.commit()
            db.refresh(portfolio)
        return portfolio
    
    @staticmethod
    def delete_portfolio(db: Session, portfolio_id: int) -> bool:
        """删除投资组合"""
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if portfolio:
            db.delete(portfolio)
            db.commit()
            return True
        return False
