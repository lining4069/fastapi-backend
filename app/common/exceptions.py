class BusinessException(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code


class UserExistsException(BusinessException):
    """用户已存在"""

    def __init__(self, username: str):
        super().__init__(message=f"用户名 '{username}' 已存在", code=400)


class UserNotFoundException(BusinessException):
    """用户不存在"""

    def __init__(self, user_id: int):
        super().__init__(message=f"用户 ID {user_id} 不存在", code=404)


class InvalidCredentialsException(BusinessException):
    """凭据无效"""

    def __init__(self):
        super().__init__(message="用户名或密码错误", code=401)


class TokenExpiredException(BusinessException):
    """Token失效"""

    def __init__(self):
        super().__init__(message="token失效,请重新登录", code=401)
