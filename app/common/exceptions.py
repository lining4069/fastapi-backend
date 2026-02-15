from typing import Any


class BusinessException(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code


class ValidationException(BusinessException):
    """通用业务校验失败 (比如密码错误,...)"""

    def __init__(self, message: str):
        super().__init__(message=message, code=400)


class UnauthorizedException(BusinessException):
    """未经认证 (401)"""

    def __init__(self, message: str = "登录状态已失效，请重新登录"):
        super().__init__(message=message, code=401)


class ForbiddenException(BusinessException):
    """权限不足 (403)"""

    def __init__(self, message: str = "您没有权限执行此操作"):
        super().__init__(message=message, code=403)


class NotFoundException(BusinessException):
    """资源不存在 (404)"""

    def __init__(self, resource: str, identifier: Any):
        super().__init__(message=f"{resource} '{identifier}' 不存在", code=404)


class UniqueViolationException(BusinessException):
    """唯一性约束冲突 (400 或 409)"""

    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            message=f"{resource} '{identifier}' 已存在，请更换后重试", code=400
        )


class DatabaseOperationException(BusinessException):
    """数据库操作未生效 (如 rowcount=0)"""

    def __init__(self, resource: str, identifier: Any, action: str = "更新"):
        super().__init__(
            message=f"{action}{resource} '{identifier}' 失败，数据可能已被删除或无变动",
            code=400,
        )


class RateLimitException(BusinessException):
    """频率限制"""

    def __init__(self, message: str = "操作过于频繁，请稍后再试"):
        super().__init__(message=message, code=429)
