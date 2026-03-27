"""
认证模块 Schema 单元测试
"""
import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate, User, Token, LoginRequest


class TestUserCreateSchema:
    """UserCreate Schema 测试"""

    def test_valid_user_create(self):
        """测试有效的用户创建数据"""
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="SecurePass123!",
            password_confirmation="SecurePass123!",
        )
        assert user_data.username == "testuser"
        assert user_data.email == "test@example.com"

    def test_password_confirmation_mismatch(self):
        """测试密码确认不匹配"""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="testuser",
                email="test@example.com",
                password="SecurePass123!",
                password_confirmation="DifferentPass!",
            )
        assert "password_confirmation" in str(exc_info.value)

    def test_invalid_email_format(self):
        """测试无效邮箱格式"""
        with pytest.raises(ValidationError):
            UserCreate(
                username="testuser",
                email="invalid-email",
                password="SecurePass123!",
                password_confirmation="SecurePass123!",
            )

    def test_username_too_short(self):
        """测试用户名过短"""
        with pytest.raises(ValidationError):
            UserCreate(
                username="ab",  # 假设最小长度为 3
                email="test@example.com",
                password="SecurePass123!",
                password_confirmation="SecurePass123!",
            )

    def test_password_too_weak(self):
        """测试密码过弱（如果 schema 有验证）"""
        # 根据实际 schema 实现调整
        pass


class TestUserSchema:
    """User Schema 测试"""

    def test_valid_user(self):
        """测试有效的用户对象"""
        user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            is_active=True,
            is_superuser=False,
        )
        assert user.id == 1
        assert user.username == "testuser"
        assert user.email == "test@example.com"

    def test_user_optional_fields(self):
        """测试用户可选字段"""
        user = User(
            id=1,
            username="testuser",
            email="test@example.com",
        )
        assert user.is_active is True  # 默认值
        assert user.is_superuser is False  # 默认值


class TestTokenSchema:
    """Token Schema 测试"""

    def test_valid_token(self):
        """测试有效的 token 对象"""
        token = Token(
            access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            token_type="bearer",
        )
        assert token.access_token.startswith("eyJ")
        assert token.token_type == "bearer"

    def test_token_type_default(self):
        """测试 token 类型默认值"""
        token = Token(
            access_token="test_token",
        )
        assert token.token_type == "bearer"


class TestLoginRequestSchema:
    """LoginRequest Schema 测试"""

    def test_valid_login_request(self):
        """测试有效的登录请求"""
        login = LoginRequest(
            username="testuser",
            password="SecurePass123!",
        )
        assert login.username == "testuser"
        assert login.password == "SecurePass123!"

    def test_login_with_email(self):
        """测试使用邮箱登录（如果支持）"""
        # 根据实际实现调整
        pass
