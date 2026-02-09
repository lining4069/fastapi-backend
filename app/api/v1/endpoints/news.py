from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.pagination import Page, PageParams
from app.common.responses import APIResponse, success
from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.news.schema import CategotyOutSchema
from app.modules.news.service import CategoryService

logger = get_logger(__name__)

router = APIRouter()


@router.get("/")
async def news_hello():
    return {"message": "Hello World"}


@router.get("/categories_paginated", response_model=Page[CategotyOutSchema])
async def get_categories_paginated(
    params: PageParams = Depends(), db: AsyncSession = Depends(get_db)
):
    return await CategoryService.get_category_paginated(db, params)


@router.get("/categories", response_model=APIResponse[list[CategotyOutSchema]])
async def get_categories(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100
):
    logger.info("接口'/categories' 正常访问")
    result = await CategoryService.get_category(db, skip, limit)
    return success(data=result)
