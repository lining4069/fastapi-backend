# engine/sessionmaker/get_db依赖项
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

ASYNC_DATABASE_URL = f"mysql+aiomysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

async_agine = create_async_engine(
    url=ASYNC_DATABASE_URL,
    echo=False,  # 输出sql日志
    pool_size=5,  # 连接池中保持的持久连接数
    max_overflow=5,  # 峰值额外连接
    pool_timeout=30,  # 等待连接的超时时间
    pool_recycle=1800,  # 30分钟回收一次连接 防止服务器断开
    pool_pre_ping=True,  # 每次去连接前ping一下
)

AsyncSessionLocal = async_sessionmaker(  # 一个可配置的 异步会话(AsyncSession) 工厂函数
    bind=async_agine,  # 绑定数据库引擎
    class_=AsyncSession,  # 制定会话类
    expire_on_commit=False,  # 提交会话不过期，不会重新查库
)


# 数据库Session依赖项
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session  # 返回数据库会话给路由处理函数
            await session.commit()  # 提交事务
        except Exception:
            await session.rollback()  # 出现异常 回滚
            raise
        finally:
            await session.close()  # 关闭会话
