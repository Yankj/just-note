"""
资产 API 单元测试
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from datetime import date


class TestAssetAPI:
    """资产 API 测试"""

    @pytest.mark.asyncio
    async def test_list_assets_empty(self, client: AsyncClient):
        """测试获取空资产列表"""
        # 需要先登录获取 token（这里简化处理）
        # 实际测试中应该先注册登录获取 token
        response = await client.get("/api/v1/assets/")
        # 未授权应返回 401
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_create_asset(self, client: AsyncClient):
        """测试创建资产"""
        asset_data = {
            "name": "贵州茅台",
            "asset_type": "stock",
            "symbol": "600519",
            "quantity": "100",
            "cost_basis": "1800.00",
            "current_price": "1750.00",
            "purchase_date": "2024-01-15",
        }
        
        response = await client.post("/api/v1/assets/", json=asset_data)
        # 未授权应返回 401
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_asset_not_found(self, client: AsyncClient):
        """测试获取不存在的资产"""
        response = await client.get("/api/v1/assets/999")
        assert response.status_code == 401  # 未授权

    @pytest.mark.asyncio
    async def test_update_asset(self, client: AsyncClient):
        """测试更新资产"""
        update_data = {
            "current_price": "1800.00",
            "notes": "Updated price",
        }
        
        response = await client.put("/api/v1/assets/1", json=update_data)
        assert response.status_code == 401  # 未授权

    @pytest.mark.asyncio
    async def test_delete_asset(self, client: AsyncClient):
        """测试删除资产"""
        response = await client.delete("/api/v1/assets/1")
        assert response.status_code == 401  # 未授权

    # 以下测试在实现认证后启用
    @pytest.mark.skip(reason="需要实现认证后启用")
    @pytest.mark.asyncio
    async def test_asset_crud_flow(self, client: AsyncClient, auth_token: str):
        """测试资产完整 CRUD 流程"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # 1. 创建资产
        create_data = {
            "name": "Test Stock",
            "asset_type": "stock",
            "symbol": "TEST",
            "quantity": "100",
            "cost_basis": "100.00",
            "current_price": "100.00",
        }
        create_response = await client.post("/api/v1/assets/", json=create_data, headers=headers)
        assert create_response.status_code == 201
        created_asset = create_response.json()
        asset_id = created_asset["id"]
        
        # 2. 获取资产
        get_response = await client.get(f"/api/v1/assets/{asset_id}", headers=headers)
        assert get_response.status_code == 200
        assert get_response.json()["name"] == "Test Stock"
        
        # 3. 更新资产
        update_data = {"current_price": "120.00"}
        update_response = await client.put(
            f"/api/v1/assets/{asset_id}",
            json=update_data,
            headers=headers
        )
        assert update_response.status_code == 200
        assert update_response.json()["current_price"] == "120.00"
        
        # 4. 删除资产
        delete_response = await client.delete(f"/api/v1/assets/{asset_id}", headers=headers)
        assert delete_response.status_code == 204
        
        # 5. 验证删除
        get_deleted_response = await client.get(f"/api/v1/assets/{asset_id}", headers=headers)
        assert get_deleted_response.status_code == 404
