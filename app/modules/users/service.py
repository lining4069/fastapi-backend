from datetime import datetime

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import (
    DatabaseOperationException,
    NotFoundException,
    UnauthorizedException,
    UniqueViolationException,
    ValidationException,
)
from app.core.database import get_db
from app.core.security import verify_password
from app.modules.users.models import User, UserToken
from app.modules.users.repository import UserRepository
from app.modules.users.schema import (
    UserAuthResponse,
    UserInfoResponse,
    UserRequest,
    UserUpdateRequest,
)


async def get_current_user(
    authorization: str = Header(..., alias="Authorization"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """获取当前有效用户"""
    token = authorization.replace("Bearer ", "")
    valid_token = await UserRepository.verify_token(db, token)
    if not isinstance(valid_token, UserToken):
        raise ValidationException("非法Token,请检查后重试")

    if valid_token.expires_at < datetime.now():
        raise UnauthorizedException()

    user = await UserRepository.get_user_by_token(db, valid_token)
    if not isinstance(user, User):
        raise NotFoundException("用户", f"ID: {valid_token.user_id}")

    return user


class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserRequest):
        # 检查用户是否已经存在
        existing_user = await UserRepository.get_user_by_username(
            db, user_data.username
        )
        if existing_user:
            raise UniqueViolationException("用户", user_data.username)
        # 创建用户
        user = await UserRepository.create_user(db, user_data)
        # 创建Token
        token = await UserRepository.create_token(db, user.id)
        # 构建,返回UserAuthResponse
        return UserAuthResponse(
            token=token, userInfo=UserInfoResponse.model_validate(user)
        )

    @staticmethod
    async def auth_user(db: AsyncSession, user_data: UserRequest):
        # 检查用户是否已经存在
        existing_user = await UserRepository.get_user_by_username(
            db, user_data.username
        )
        if not existing_user:
            raise NotFoundException("用户", user_data.username)

        # 验证密码是否正确
        pwd_verify = verify_password(user_data.password, existing_user.password)
        if not pwd_verify:
            raise ValidationException(f"{user_data.username}的密码错误,请检查后重试")

        # 创建Token
        token = await UserRepository.create_token(db, existing_user.id)

        # 构建,返回UserAuthResponse
        return UserAuthResponse(
            token=token, userInfo=UserInfoResponse.model_validate(existing_user)
        )

    @staticmethod
    async def update_user(db: AsyncSession, user: User, update_data: UserUpdateRequest):
        valid_updated_rowcount = await UserRepository.update_user(
            db, user.username, update_data
        )
        # 校验是否有效更新数据库
        if valid_updated_rowcount == 0:
            raise DatabaseOperationException("用户", user.username, "更新")
        # 获取更新后的用户
        updated_user = await UserRepository.get_user_by_username(db, user.username)
        return updated_user
