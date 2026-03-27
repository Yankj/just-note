"""
配置模块单元测试
"""
import os
import pytest
from app.core.config import Settings


class TestSettings:
    """配置设置测试"""

    def test_default_project_name(self):
        """测试默认项目名称"""
        settings = Settings()
        assert settings.PROJECT_NAME == "财务自由之路"

    def test_default_version(self):
        """测试默认版本号"""
        settings = Settings()
        assert settings.VERSION == "1.0.0"

    def test_api_prefix(self):
        """测试 API 前缀"""
        settings = Settings()
        assert settings.API_V1_PREFIX == "/api/v1"

    def test_database_url_generation(self):
        """测试数据库 URL 生成"""
        settings = Settings(
            POSTGRES_USER="test_user",
            POSTGRES_PASSWORD="test_pass",
            POSTGRES_HOST="test_host",
            POSTGRES_PORT="5433",
            POSTGRES_DB="test_db",
        )
        expected = "postgresql+asyncpg://test_user:test_pass@test_host:5433/test_db"
        assert settings.DATABASE_URL == expected

    def test_cors_origins_from_string(self):
        """测试 CORS  origins 从字符串解析"""
        settings = Settings(
            BACKEND_CORS_ORIGINS="http://localhost:3000,http://localhost:5173"
        )
        assert len(settings.BACKEND_CORS_ORIGINS) == 2
        assert "http://localhost:3000" in settings.BACKEND_CORS_ORIGINS
        assert "http://localhost:5173" in settings.BACKEND_CORS_ORIGINS

    def test_cors_origins_from_list(self):
        """测试 CORS origins 从列表设置"""
        settings = Settings(
            BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
        )
        assert len(settings.BACKEND_CORS_ORIGINS) == 2

    def test_default_secret_key(self):
        """测试默认密钥（警告：生产环境应修改）"""
        settings = Settings()
        assert settings.SECRET_KEY == "your-secret-key-change-in-production"

    def test_token_expiration_settings(self):
        """测试 token 过期时间设置"""
        settings = Settings()
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
        assert settings.REFRESH_TOKEN_EXPIRE_DAYS == 7

    def test_redis_config(self):
        """测试 Redis 配置"""
        settings = Settings()
        assert settings.REDIS_HOST == "localhost"
        assert settings.REDIS_PORT == 6379

    def test_log_level(self):
        """测试日志级别"""
        settings = Settings()
        assert settings.LOG_LEVEL == "INFO"
