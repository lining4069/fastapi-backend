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
            status_code=200,  # 有些团队固定 200
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
