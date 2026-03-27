"""
投资日记 Schema
"""
import uuid
from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class DiaryBase(BaseModel):
    """日记基础 Schema"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str
    diary_type: str = Field(default="REFLECTION", description="日记类型")
    category: Optional[str] = Field(None, max_length=50)
    sentiment: Optional[str] = Field(None, description="情绪")
    confidence_score: Optional[int] = Field(None, ge=1, le=10, description="信心评分")
    is_private: bool = True
    is_pinned: bool = False


class DiaryCreate(DiaryBase):
    """日记创建 Schema"""
    related_assets: Optional[List[uuid.UUID]] = None
    related_tx_ids: Optional[List[uuid.UUID]] = None
    tags: Optional[List[str]] = None


class DiaryUpdate(BaseModel):
    """日记更新 Schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    diary_type: Optional[str] = None
    tags: Optional[List[str]] = None
    sentiment: Optional[str] = None
    confidence_score: Optional[int] = Field(None, ge=1, le=10)
    is_pinned: Optional[bool] = None


class DiaryInDB(DiaryBase):
    """数据库日记 Schema"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    user_id: uuid.UUID
    related_assets: Optional[List[uuid.UUID]] = None
    related_tx_ids: Optional[List[uuid.UUID]] = None
    tags: Optional[List[str]] = None
    diary_date: date
    created_at: datetime
    updated_at: datetime


class Diary(DiaryInDB):
    """日记响应 Schema"""
    pass


class DiaryListResponse(BaseModel):
    """日记列表响应"""
    items: List[Diary]
    total: int
    page: int
    page_size: int
    total_pages: int
