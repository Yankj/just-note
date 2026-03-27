"""
财务自由之路 - FastAPI 后端应用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, assets, transactions, diaries, analytics
from app.db.session import init_db


def create_application() -> FastAPI:
    """创建 FastAPI 应用实例"""
    
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        docs_url=f"{settings.API_V1_PREFIX}/docs",
        redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    )
    
    # CORS 配置
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由
    application.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["认证"])
    application.include_router(assets.router, prefix=f"{settings.API_V1_PREFIX}/assets", tags=["资产"])
    application.include_router(transactions.router, prefix=f"{settings.API_V1_PREFIX}/transactions", tags=["交易"])
    application.include_router(diaries.router, prefix=f"{settings.API_V1_PREFIX}/diaries", tags=["日记"])
    application.include_router(analytics.router, prefix=f"{settings.API_V1_PREFIX}/analytics", tags=["分析"])
    
    # 健康检查
    @application.get("/health")
    async def health_check():
        return {"status": "healthy", "version": settings.VERSION}
    
    # 启动事件
    @application.on_event("startup")
    async def startup_event():
        await init_db()
    
    return application


app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
