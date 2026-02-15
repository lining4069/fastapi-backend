# JWT / auth
from passlib.context import CryptContext

# 密码上下文
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    """密码加密"""
    return pwd_content.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """校验密码"""
    return pwd_content.verify(plain_password, hashed_password)
