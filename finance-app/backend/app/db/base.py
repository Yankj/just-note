"""
数据库 Base 类
"""
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped


class Base(DeclarativeBase):
    """SQLAlchemy 基础类"""
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """自动生成表名（复数形式）"""
        class_name = cls.__name__
        if class_name.endswith('s'):
            return class_name.lower()
        return f"{class_name.lower()}s"
