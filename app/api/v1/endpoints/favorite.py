from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.auth import get_current_user
from app.common.responses import APIResponse
from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.favorite.schema import FavoriteAddRequest, FavoriteInfoResponse
from app.modules.favorite.service import FavoriteService
from app.modules.users.models import User

logger = get_logger(__name__)

router = APIRouter()


@router.get("/check", response_model=APIResponse[bool])
async def check_favorite(
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """检查新闻收藏状态"""
    logger.info("接口-检查新闻收藏状态 '/check' 被访问")
    is_favorite = await FavoriteService.check_news_favorite_state(db, user, news_id)
    return APIResponse.success(data=is_favorite, message="检查新闻收藏状态成功")


@router.post("/add", response_model=APIResponse[FavoriteInfoResponse])
async def favorite_news(
    data: FavoriteAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """收藏新闻"""
    logger.info("收藏新闻接口 '/add' 被访问")
    result = await FavoriteService.add_news_to_favorite(db, user, data)
    return APIResponse(data=result, message="新闻收藏成功")
