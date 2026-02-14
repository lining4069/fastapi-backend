from venv import logger

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.responses import APIResponse
from app.core.database import get_db
from app.modules.users.schema import UserRequest
from app.modules.users.service import UserService

router = APIRouter()


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    """
    用户注册
    逻辑：验证用户是否存在 -> 创建用户 -> 生成Token -> 响应结果
    """
    logger.info("接口 用户注册 :'/register' 被访问")
    user_auth_info = await UserService.create_user(db, user_data)
    return APIResponse.success(user_auth_info)
