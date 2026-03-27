"""
交易记录 Schema
"""
import uuid
from datetime import datetime, date, time
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class TransactionBase(BaseModel):
    """交易基础 Schema"""
    tx_type: str = Field(..., description="交易类型")
    tx_date: date
    tx_time: Optional[time] = time(0, 0, 0)
    quantity: Decimal = Field(..., gt=0, description="数量")
    price: Decimal = Field(..., ge=0, description="单价")
    amount: Decimal = Field(..., ge=0, description="金额")
    fee: Decimal = Field(default=0, ge=0, description="手续费")
    currency: str = Field(default="CNY", min_length=3, max_length=3)
    broker: Optional[str] = Field(None, max_length=100)
    order_id: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class TransactionCreate(TransactionBase):
    """交易创建 Schema"""
    asset_id: uuid.UUID


class TransactionUpdate(BaseModel):
    """交易更新 Schema"""
    quantity: Optional[Decimal] = Field(None, gt=0)
    price: Optional[Decimal] = Field(None, ge=0)
    amount: Optional[Decimal] = Field(None, ge=0)
    fee: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = None


class TransactionInDB(TransactionBase):
    """数据库交易 Schema"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    user_id: uuid.UUID
    asset_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class Transaction(TransactionInDB):
    """交易响应 Schema"""
    pass


class TransactionListResponse(BaseModel):
    """交易列表响应"""
    items: List[Transaction]
    total: int
    page: int
    page_size: int
    total_pages: int
