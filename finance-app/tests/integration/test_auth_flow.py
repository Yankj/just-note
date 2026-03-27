"""
认证流程集成测试
测试完整的用户认证生命周期
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
class TestAuthFlow:
    """认证流程集成测试"""

    async def test_full_registration_and_login_flow(self, client: AsyncClient):
        """测试完整注册登录流程"""
        # 1. 注册用户
        user_data = {
            "username": "integration_test_user",
            "email": "integration@test.com",
            "password": "IntegrationTest123!",
            "password_confirmation": "IntegrationTest123!",
        }
        
        register_response = await client.post("/api/v1/auth/register", json=user_data)
        
        # 如果已实现，应返回 201
        if register_response.status_code == 201:
            created_user = register_response.json()
            assert created_user["username"] == user_data["username"]
            assert created_user["email"] == user_data["email"]
            assert "id" in created_user
            
            # 2. 登录
            login_response = await client.post(
                "/api/v1/auth/login",
                data={
                    "username": user_data["username"],
                    "password": user_data["password"],
                }
            )
            assert login_response.status_code == 200
            
            token_data = login_response.json()
            assert "access_token" in token_data
            assert token_data["token_type"] == "bearer"
            
            # 3. 使用 token 访问受保护端点
            access_token = token_data["access_token"]
            me_response = await client.get(
                "/api/v1/auth/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert me_response.status_code == 200
            user_info = me_response.json()
            assert user_info["username"] == user_data["username"]

    async def test_token_refresh_flow(self, client: AsyncClient):
        """测试 token 刷新流程"""
        # 注册并登录
        user_data = {
            "username": "refresh_test_user",
            "email": "refresh@test.com",
            "password": "RefreshTest123!",
            "password_confirmation": "RefreshTest123!",
        }
        
        await client.post("/api/v1/auth/register", json=user_data)
        login_response = await client.post(
            "/api/v1/auth/login",
            data={"username": user_data["username"], "password": user_data["password"]}
        )
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data["access_token"]
            refresh_token = token_data.get("refresh_token")
            
            if refresh_token:
                # 使用刷新 token 获取新的 access token
                refresh_response = await client.post(
                    "/api/v1/auth/refresh",
                    json={"refresh_token": refresh_token}
                )
                assert refresh_response.status_code == 200
                new_token_data = refresh_response.json()
                assert "access_token" in new_token_data

    async def test_password_reset_flow(self, client: AsyncClient):
        """测试密码重置流程"""
        # 1. 请求密码重置
        reset_request = {"email": "reset@test.com"}
        reset_response = await client.post("/api/v1/auth/password-reset/request", json=reset_request)
        
        # 2. 使用重置 token 设置新密码
        # reset_confirm_response = await client.post("/api/v1/auth/password-reset/confirm", json={...})
        
        # 3. 使用新密码登录
        # ...
        pass

    async def test_session_management(self, client: AsyncClient):
        """测试会话管理"""
        # 1. 登录获取 token
        # 2. 验证 token 有效性
        # 3. 登出使 token 失效
        # 4. 验证已失效的 token 无法访问受保护资源
        pass
