"""
用户 Schema
"""
import uuid
from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, ConfigDict


# ============ 基础 Schema ============

class UserBase(BaseModel):
    """用户基础 Schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """用户创建 Schema"""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """用户更新 Schema"""
    full_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)
    base_currency: Optional[str] = Field(None, min_length=3, max_length=3)
    net_worth_target: Optional[float] = None
    financial_freedom_date: Optional[date] = None


class UserInDB(UserBase):
    """数据库用户 Schema"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    avatar_url: Optional[str] = None
    base_currency: str = "CNY"
    net_worth_target: Optional[float] = None
    financial_freedom_date: Optional[date] = None
    is_active: bool = True
    is_verified: bool = False
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class User(UserInDB):
    """用户响应 Schema"""
    pass


# ============ 认证相关 ============

class Token(BaseModel):
    """Token 响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseModel):
    """Token 刷新请求"""
    refresh_token: str


class LoginRequest(BaseModel):
    """登录请求"""
    email: EmailStr
    password: str
