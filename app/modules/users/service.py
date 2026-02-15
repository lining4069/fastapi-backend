from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import (
    DatabaseOperationException,
    NotFoundException,
    UniqueViolationException,
    ValidationException,
)
from app.core.security import get_hash_password, verify_password
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schema import (
    PwdUpdatedRequest,
    UserAuthResponse,
    UserInfoResponse,
    UserRequest,
    UserUpdateRequest,
)


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

    @staticmethod
    async def change_password(
        db: AsyncSession, user: User, pwd_data: PwdUpdatedRequest
    ):
        """修改密码"""
        is_valid = verify_password(pwd_data.old_pwd, user.password)
        if not is_valid:
            raise ValidationException("输入旧密码错误,请修改后重试")

        hashed_pwd = get_hash_password(pwd_data.new_pwd)
        valid_updated_rowcount = await UserRepository.change_password(
            db, user.username, hashed_pwd
        )
        if valid_updated_rowcount == 0:
            raise DatabaseOperationException("用户密码", user.username, "修改")
