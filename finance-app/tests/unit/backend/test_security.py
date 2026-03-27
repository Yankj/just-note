"""
安全模块单元测试
"""
import pytest
from datetime import datetime, timedelta
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.config import settings


class TestPasswordHashing:
    """密码哈希测试"""

    def test_password_hashing(self):
        """测试密码哈希生成"""
        password = "SecurePassword123!"
        hashed = get_password_hash(password)
        assert hashed != password
        assert hashed.startswith("$2")  # bcrypt 哈希前缀

    def test_password_verification_success(self):
        """测试密码验证成功"""
        password = "SecurePassword123!"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_password_verification_failure(self):
        """测试密码验证失败"""
        password = "SecurePassword123!"
        wrong_password = "WrongPassword!"
        hashed = get_password_hash(password)
        assert verify_password(wrong_password, hashed) is False

    def test_different_hashes_for_same_password(self):
        """测试相同密码生成不同哈希（由于盐值）"""
        password = "SecurePassword123!"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2
        # 但都能验证通过
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestAccessToken:
    """访问 Token 测试"""

    def test_create_access_token(self):
        """测试创建访问 token"""
        data = {"sub": "testuser", "user_id": 1}
        token = create_access_token(data)
        assert token is not None
        assert len(token) > 0

    def test_access_token_expiration(self):
        """测试访问 token 过期时间"""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        decoded = decode_token(token)
        assert decoded["sub"] == "testuser"
        assert "exp" in decoded

    def test_access_token_custom_expiration(self):
        """测试自定义过期时间"""
        data = {"sub": "testuser"}
        expires_delta = timedelta(hours=2)
        token = create_access_token(data, expires_delta=expires_delta)
        decoded = decode_token(token)
        # 验证过期时间约为 2 小时后
        exp_timestamp = decoded["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        expected_exp = datetime.now() + expires_delta
        # 允许 1 分钟误差
        assert abs((exp_datetime - expected_exp).total_seconds()) < 60

    def test_decode_invalid_token(self):
        """测试解码无效 token"""
        with pytest.raises(Exception):
            decode_token("invalid_token_string")

    def test_decode_expired_token(self):
        """测试解码已过期 token"""
        data = {"sub": "testuser"}
        expires_delta = timedelta(seconds=-1)  # 已过期
        token = create_access_token(data, expires_delta=expires_delta)
        with pytest.raises(Exception):
            decode_token(token)


class TestRefreshToken:
    """刷新 Token 测试"""

    def test_create_refresh_token(self):
        """测试创建刷新 token"""
        data = {"sub": "testuser"}
        token = create_refresh_token(data)
        assert token is not None
        assert len(token) > 0

    def test_refresh_token_longer_expiration(self):
        """测试刷新 token 过期时间更长"""
        data = {"sub": "testuser"}
        access_token = create_access_token(data)
        refresh_token = create_refresh_token(data)
        
        access_decoded = decode_token(access_token)
        refresh_decoded = decode_token(refresh_token)
        
        # 刷新 token 应该比访问 token 过期时间更长
        assert refresh_decoded["exp"] > access_decoded["exp"]
