from venv import logger

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.responses import APIResponse
from app.core.database import get_db
from app.modules.users.models import User
from app.modules.users.schema import (
    UserAuthResponse,
    UserInfoResponse,
    UserRequest,
    UserUpdateRequest,
)
from app.modules.users.service import UserService, get_current_user

router = APIRouter()


@router.post("/register", response_model=APIResponse[UserAuthResponse])
async def register(user: UserRequest, db: AsyncSession = Depends(get_db)):
    """
    用户注册
    逻辑：验证用户是否存在 -> 创建用户 -> 生成Token -> 响应结果
    """
    logger.info("接口 用户注册 :'/register' 被访问")
    user_auth_info = await UserService.create_user(db, user)
    return APIResponse.success(data=user_auth_info, message="注册成功")


@router.post("/login", response_model=APIResponse[UserAuthResponse])
async def login(user: UserRequest, db: AsyncSession = Depends(get_db)):
    """
    用户登录
    逻辑: 验证用户是否存在 -> 验证密码 -> 生成Token -> 响应结果
    """
    logger.info(f"接口 用户登录 :'/login' 被访问,用户{user.username}正在尝试登录")
    user_auth_info = await UserService.auth_user(db, user)
    return APIResponse.success(data=user_auth_info, message="登录成功")


@router.get("/info", response_model=APIResponse[UserInfoResponse])
async def get_info(user: User = Depends(get_current_user)):
    """获取用户信息"""
    logger.info("接口 用户登录 :'/info' 被访问")
    return APIResponse.success(data=user, message="获取用户信息成功")


@router.put("/update", response_model=APIResponse[UserInfoResponse])
async def update_user(
    update_data: UserUpdateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """更新用户信息"""
    logger.info("接口 用户更新 :'/update' 被访问")
    result = await UserService.update_user(db, user, update_data)
    return APIResponse.success(data=result, message="更新用户信息成功")
