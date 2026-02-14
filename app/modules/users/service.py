from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import UserExistsError
from app.modules.users.repository import UserRepository
from app.modules.users.schema import UserAuthResponse, UserInfoResponse, UserRequest


class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserRequest):
        # 检查用户是否已经存在
        existing_user = await UserRepository.get_user_by_username(
            db, user_data.username
        )
        if existing_user:
            raise UserExistsError(user_data.username)
        # 创建用户
        user = await UserRepository.create_user(db, user_data)
        # 创建Token
        token = await UserRepository.create_token(db, user.id)
        # 构建,返回UserAuthResponse
        return UserAuthResponse(
            token=token, userInfo=UserInfoResponse.model_validate(user)
        )
