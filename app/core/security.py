# JWT / auth
from passlib.context import CryptContext

# 密码上下文
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    """密码加密"""
    return pwd_content.hash(password)


if __name__ == "__main__":
    print(get_hash_password("12345679"))
