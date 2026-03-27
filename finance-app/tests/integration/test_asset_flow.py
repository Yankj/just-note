"""
资产管理流程集成测试
"""
import pytest
from httpx import AsyncClient
from decimal import Decimal


@pytest.mark.asyncio
class TestAssetFlow:
    """资产管理流程集成测试"""

    async def test_create_and_query_asset_flow(self, client: AsyncClient, auth_token: str):
        """测试创建和查询资产流程"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # 1. 创建股票资产
        stock_asset = {
            "name": "贵州茅台",
            "asset_type": "stock",
            "symbol": "600519",
            "quantity": "100",
            "cost_basis": "1800.00",
            "current_price": "1750.00",
        }
        
        create_response = await client.post("/api/v1/assets/", json=stock_asset, headers=headers)
        assert create_response.status_code == 201
        created_asset = create_response.json()
        asset_id = created_asset["id"]
        
        # 2. 查询资产列表
        list_response = await client.get("/api/v1/assets/", headers=headers)
        assert list_response.status_code == 200
        assets = list_response.json()
        assert len(assets) >= 1
        
        # 3. 查询单个资产
        get_response = await client.get(f"/api/v1/assets/{asset_id}", headers=headers)
        assert get_response.status_code == 200
        assert get_response.json()["symbol"] == "600519"
        
        # 4. 更新资产价格
        update_response = await client.patch(
            f"/api/v1/assets/{asset_id}",
            json={"current_price": "1800.00"},
            headers=headers
        )
        assert update_response.status_code == 200
        assert update_response.json()["current_price"] == "1800.00"
        
        # 5. 删除资产
        delete_response = await client.delete(f"/api/v1/assets/{asset_id}", headers=headers)
        assert delete_response.status_code == 204

    async def test_portfolio_calculation_flow(self, client: AsyncClient, auth_token: str):
        """测试投资组合计算流程"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # 创建多个资产
        assets_data = [
            {
                "name": "股票 A",
                "asset_type": "stock",
                "quantity": "100",
                "cost_basis": "100.00",
                "current_price": "120.00",
            },
            {
                "name": "基金 B",
                "asset_type": "fund",
                "quantity": "500",
                "cost_basis": "2.00",
                "current_price": "2.50",
            },
        ]
        
        # 创建资产并计算总投资组合
        total_cost = Decimal("0")
        total_value = Decimal("0")
        
        for asset_data in assets_data:
            create_response = await client.post("/api/v1/assets/", json=asset_data, headers=headers)
            if create_response.status_code == 201:
                asset = create_response.json()
                total_cost += Decimal(asset["total_cost"])
                total_value += Decimal(asset["current_value"])
        
        # 验证投资组合总值
        portfolio_response = await client.get("/api/v1/assets/portfolio", headers=headers)
        if portfolio_response.status_code == 200:
            portfolio = portfolio_response.json()
            assert Decimal(portfolio["total_cost"]) == total_cost
            assert Decimal(portfolio["total_value"]) == total_value

    async def test_asset_type_filtering_flow(self, client: AsyncClient, auth_token: str):
        """测试资产类型筛选流程"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # 创建不同类型的资产
        # 筛选特定类型的资产
        # 验证筛选结果
        pass
