from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.pagination import Page, PageParams, get_page_params
from app.common.responses import APIResponse
from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.news.schema import CategotyOutSchema, NewsDetailSchema, NewsSchema
from app.modules.news.service import CategoryService, NewsService

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
    return APIResponse.success(data)


@router.get("/categories", response_model=APIResponse[List[CategotyOutSchema]])
async def get_categories(
    db: AsyncSession = Depends(get_db), params=Depends(get_page_params)
):
    """获取新闻类别"""
    logger.info("获取新闻类别接口: '/categories' 被访问")
    data = await CategoryService.get_category(db, params)
    return APIResponse.success(data=data)


@router.get("/list", response_model=APIResponse[Page[NewsSchema]])
async def get_news_list(
    db: AsyncSession = Depends(get_db),
    category_id: int = Query(alias="categoryId"),
    params: PageParams = Depends(get_page_params),
):
    """获取执行类别下新闻列表"""
    # 处理分页规则—> 查询新闻列表 -> 计算总量 -> 计算是否还有更多
    logger.info(
        f"获取执行类别下新闻列表: '/list',被访问, id: {category_id},页码页数: {params.__dict__}"
    )
    data = await NewsService.get_news_list(db, category_id, params)
    return APIResponse.success(data)


@router.get("/detail", response_model=APIResponse[NewsDetailSchema])
async def get_detail_by_id(
    db: AsyncSession = Depends(get_db),
    news_id: int = Query(..., alias="id", description="新闻ID"),
):
    """根据新闻ID获取详情"""
    # 获取新闻详情 + 浏览量+1 + 相关新闻
    logger.info(f"获取新闻接口: '/detail',被访问, id: {news_id}")
    news_detail, related_news = await NewsService.view_news_detail(db, news_id)
    if news_detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="新闻不存在")

    result = NewsDetailSchema.model_validate(news_detail)
    result.related_news = [
        NewsSchema.model_validate(news) for news in (related_news or [])
    ]
    return APIResponse.success(result)
