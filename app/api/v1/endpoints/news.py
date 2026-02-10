from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.pagination import Page, PageParams, get_page_params
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


@router.get(
    "/categories_paginated", response_model=APIResponse[Page[CategotyOutSchema]]
)
async def get_categories_paginated(
    params: PageParams = Depends(get_page_params), db: AsyncSession = Depends(get_db)
):
    """Page 分页器下的获取新闻类别"""
    data = await CategoryService.get_category_paginated(db, params)
    return success(data)


@router.get("/categories", response_model=APIResponse[list[CategotyOutSchema]])
async def get_categories(
    db: AsyncSession = Depends(get_db), params=Depends(get_page_params)
):
    """获取新闻类别"""
    logger.info("接口'/categories' 正常访问")
    data = await CategoryService.get_category(db, params)
    return success(data=data)


@router.get("/list")
async def get_news_list(
    db: AsyncSession = Depends(get_db),
    category_id: int = Query(alias="categoryId"),
    params: PageParams = Depends(get_page_params),
):
    """获取执行类别下新闻列表"""
    # 处理分页规则—> 查询新闻列表 -> 计算总量 -> 计算是否还有更多
    data = await CategoryService.get_news_list(db, category_id, params)
    return success(data)


@router.get("/detail")
async def get_detail_by_id(
    db: AsyncSession = Depends(get_db), id: int = Query(..., description="新闻ID")
):
    """根据新闻ID获取详情"""
    data = {}
    return success(data)
