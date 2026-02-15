from datetime import datetime

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import (
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)
from app.core.database import get_db
from app.modules.users.models import User, UserToken
from app.modules.users.repository import UserRepository


async def get_current_user(
    authorization: str = Header(..., alias="Authorization"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    认证Token
    获取当前有效用户
    """
    token = authorization.replace("Bearer ", "")
    valid_token = await UserRepository.verify_token(db, token)

    # Token -> UserToken表是否存在对应的一条记录
    if not isinstance(valid_token, UserToken):
        raise ValidationException("非法Token,请检查后重试")

    # 存在Token记录 -> 检查Token是否已经失效
    if valid_token.expires_at < datetime.now():
        raise UnauthorizedException()

    # 存在且未失效Token -> user:User
    user = await UserRepository.get_user_by_token(db, valid_token)

    # 防止Token在校验期间,用户被删除
    if not isinstance(user, User):
        raise NotFoundException("用户", f"ID: {valid_token.user_id}")

    # 返回存在且具备有效Token的用户,即完成了对路由处理函数登录前提的要求,又获得了当前用户实例
    return user
