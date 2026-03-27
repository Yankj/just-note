"""
FastAPI 应用主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import init_db
from api import auth_router, users_router, portfolios_router, transactions_router


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## Finance App API

投资管理系统的后端 API，提供以下功能：

### 认证模块
- 用户注册
- 用户登录（JWT）
- 获取当前用户信息

### 用户管理
- 用户 CRUD 操作

### 投资组合
- 创建/管理投资组合
- 组合资产跟踪

### 交易记录
- 买入/卖出记录
- 存款/取款记录
- 分红记录
    """,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    init_db()
    print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} 已启动")
    print(f"📚 Swagger 文档：http://localhost:8000/docs")
    print(f"📖 ReDoc 文档：http://localhost:8000/redoc")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理工作"""
    print(f"👋 {settings.APP_NAME} 已关闭")


@app.get("/")
async def root():
    """根路径"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# 注册 API 路由
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(portfolios_router, prefix="/api/v1")
app.include_router(transactions_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
