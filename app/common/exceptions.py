from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": exc.status_code, "message": exc.detail, "data": None},
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal Error",
            "data": None,
        },
    )


# app/common/exceptions.py
class BusinessException(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code


async def business_exception_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, BusinessException):
        return JSONResponse(
            status_code=200,  # 默认固定 200
            content={
                "code": exc.code,
                "message": exc.message,
                "data": None,
            },
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal Error",
            "data": None,
        },
    )


class UserExistsError(BusinessException):
    """用户已存在"""

    def __init__(self, username: str):
        super().__init__(message=f"用户名 '{username}' 已存在", code=400)


class UserNotFoundError(BusinessException):
    """用户不存在"""

    def __init__(self, user_id: int):
        super().__init__(message=f"用户 ID {user_id} 不存在", code=404)


class InvalidCredentialsError(BusinessException):
    """凭据无效"""

    def __init__(self):
        super().__init__(message="用户名或密码错误", code=401)
