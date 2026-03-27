"""
投资日记 API 路由
"""
from typing import Annotated, Optional
from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.diary import Diary, DiaryCreate, DiaryUpdate, DiaryListResponse

router = APIRouter()


@router.get("/", response_model=DiaryListResponse)
async def get_diaries(
    db: Annotated[AsyncSession, Depends(get_db)],
    diary_type: Optional[str] = Query(None),
    tags: Optional[list[str]] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """获取投资日记列表"""
    # TODO: 实现日记列表查询
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented yet",
    )


@router.post("/", response_model=Diary, status_code=status.HTTP_201_CREATED)
async def create_diary(
    diary_data: DiaryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """创建投资日记"""
    # TODO: 实现日记创建逻辑
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented yet",
    )


@router.get("/{diary_id}", response_model=Diary)
async def get_diary(
    diary_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """获取日记详情"""
    # TODO: 实现日记详情查询
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented yet",
    )


@router.put("/{diary_id}", response_model=Diary)
async def update_diary(
    diary_id: UUID,
    diary_data: DiaryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """更新日记"""
    # TODO: 实现日记更新逻辑
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented yet",
    )


@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
    diary_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """删除日记"""
    # TODO: 实现日记删除逻辑
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented yet",
    )
