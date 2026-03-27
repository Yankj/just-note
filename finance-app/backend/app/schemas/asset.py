"""
资产 Schema
"""
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class AssetBase(BaseModel):
    """资产基础 Schema"""
    asset_type: str = Field(..., description="资产类型")
    symbol: str = Field(..., min_length=1, max_length=50, description="代码")
    name: str = Field(..., min_length=1, max_length=200, description="名称")
    market: Optional[str] = Field(None, max_length=20, description="市场")


class AssetCreate(AssetBase):
    """资产创建 Schema"""
    quantity: Decimal = Field(default=0, ge=0, description="数量")
    avg_cost: Decimal = Field(default=0, ge=0, description="平均成本")


class AssetUpdate(BaseModel):
    """资产更新 Schema"""
    name: Optional[str] = Field(None, max_length=200)
    quantity: Optional[Decimal] = Field(None, ge=0)
    avg_cost: Optional[Decimal] = Field(None, ge=0)
    is_hidden: Optional[bool] = None


class AssetInDB(AssetBase):
    """数据库资产 Schema"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    user_id: uuid.UUID
    quantity: Decimal
    avg_cost: Decimal
    current_price: Optional[Decimal] = None
    market_value: Optional[Decimal] = None
    unrealized_pnl: Optional[Decimal] = None
    unrealized_pnl_pct: Optional[Decimal] = None
    realized_pnl: Decimal = Decimal("0")
    is_active: bool = True
    is_hidden: bool = False
    last_synced_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class Asset(AssetInDB):
    """资产响应 Schema"""
    pass


class AssetListResponse(BaseModel):
    """资产列表响应"""
    items: List[Asset]
    total: int
    page: int
    page_size: int
    total_pages: int
