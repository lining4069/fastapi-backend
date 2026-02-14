import uuid
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import get_hash_password
from app.modules.users.models import User, UserToken
from app.modules.users.schema import UserRequest


class UserRepository:
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
        """根据用户名查找用户"""
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserRequest) -> User:
        """注册用户"""
        hashed_pwd = get_hash_password(user_data.password)
        user = User(username=user_data.username, password=hashed_pwd)

        db.add(user)

        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def create_token(db: AsyncSession, user_id: int) -> str:
        """生成token"""
        token = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(days=settings.TOKEN_VALID_DURATION_DAYS)

        query = select(UserToken).where(UserToken.user_id == user_id)
        result = await db.execute(query)
        user_token = result.scalar_one_or_none()
        if user_token:
            user_token.token = token
            user_token.expires_at = expires_at
        else:
            user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
            db.add(user_token)
            await db.commit()
        return token
