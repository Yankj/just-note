"""
资产模块 Schema 单元测试
"""
import pytest
from datetime import date
from decimal import Decimal
from pydantic import ValidationError
from app.schemas.asset import Asset, AssetCreate, AssetUpdate, AssetType


class TestAssetType:
    """资产类型枚举测试"""

    def test_asset_type_values(self):
        """测试资产类型枚举值"""
        assert AssetType.STOCK == "stock"
        assert AssetType.FUND == "fund"
        assert AssetType.BOND == "bond"
        assert AssetType.REAL_ESTATE == "real_estate"
        assert AssetType.CASH == "cash"
        assert AssetType.CRYPTO == "crypto"
        assert AssetType.OTHER == "other"


class TestAssetCreateSchema:
    """AssetCreate Schema 测试"""

    def test_valid_asset_create_stock(self):
        """测试创建股票资产"""
        asset_data = AssetCreate(
            name="贵州茅台",
            asset_type=AssetType.STOCK,
            symbol="600519",
            quantity=Decimal("100"),
            cost_basis=Decimal("1800.00"),
            current_price=Decimal("1750.00"),
            purchase_date=date(2024, 1, 15),
        )
        assert asset_data.name == "贵州茅台"
        assert asset_data.asset_type == AssetType.STOCK
        assert asset_data.symbol == "600519"
        assert asset_data.quantity == Decimal("100")

    def test_valid_asset_create_fund(self):
        """测试创建基金资产"""
        asset_data = AssetCreate(
            name="沪深 300ETF",
            asset_type=AssetType.FUND,
            symbol="510300",
            quantity=Decimal("1000"),
            cost_basis=Decimal("4.50"),
            current_price=Decimal("4.20"),
        )
        assert asset_data.asset_type == AssetType.FUND

    def test_valid_asset_create_crypto(self):
        """测试创建加密货币资产"""
        asset_data = AssetCreate(
            name="Bitcoin",
            asset_type=AssetType.CRYPTO,
            symbol="BTC",
            quantity=Decimal("0.5"),
            cost_basis=Decimal("45000.00"),
            current_price=Decimal("50000.00"),
            currency="USD",
        )
        assert asset_data.asset_type == AssetType.CRYPTO
        assert asset_data.currency == "USD"

    def test_asset_create_missing_required_fields(self):
        """测试缺少必填字段"""
        with pytest.raises(ValidationError):
            AssetCreate()  # 缺少 name, asset_type 等必填字段

    def test_asset_create_negative_quantity(self):
        """测试负数数量（应失败）"""
        with pytest.raises(ValidationError):
            AssetCreate(
                name="Test Asset",
                asset_type=AssetType.STOCK,
                quantity=Decimal("-100"),
                cost_basis=Decimal("100.00"),
            )

    def test_asset_create_negative_cost_basis(self):
        """测试负数成本（应失败）"""
        with pytest.raises(ValidationError):
            AssetCreate(
                name="Test Asset",
                asset_type=AssetType.STOCK,
                quantity=Decimal("100"),
                cost_basis=Decimal("-100.00"),
            )

    def test_asset_create_empty_name(self):
        """测试空名称（应失败）"""
        with pytest.raises(ValidationError):
            AssetCreate(
                name="",
                asset_type=AssetType.STOCK,
                quantity=Decimal("100"),
                cost_basis=Decimal("100.00"),
            )


class TestAssetUpdateSchema:
    """AssetUpdate Schema 测试"""

    def test_partial_update(self):
        """测试部分字段更新"""
        update_data = AssetUpdate(
            current_price=Decimal("1800.00"),
        )
        assert update_data.current_price == Decimal("1800.00")
        # 其他字段应为 None（可选）

    def test_full_update(self):
        """测试全部字段更新"""
        update_data = AssetUpdate(
            name="Updated Name",
            quantity=Decimal("200"),
            current_price=Decimal("1900.00"),
            notes="Updated notes",
        )
        assert update_data.name == "Updated Name"
        assert update_data.quantity == Decimal("200")

    def test_update_negative_quantity(self):
        """测试更新为负数数量（应失败）"""
        with pytest.raises(ValidationError):
            AssetUpdate(quantity=Decimal("-50"))


class TestAssetSchema:
    """Asset Schema 测试（包含 ID 的完整资产对象）"""

    def test_valid_asset(self):
        """测试有效的资产对象"""
        asset = Asset(
            id=1,
            user_id=1,
            name="贵州茅台",
            asset_type=AssetType.STOCK,
            symbol="600519",
            quantity=Decimal("100"),
            cost_basis=Decimal("1800.00"),
            current_price=Decimal("1750.00"),
            purchase_date=date(2024, 1, 15),
            is_active=True,
        )
        assert asset.id == 1
        assert asset.name == "贵州茅台"
        assert asset.total_cost == Decimal("180000.00")  # 100 * 1800
        assert asset.current_value == Decimal("175000.00")  # 100 * 1750
        assert asset.profit_loss == Decimal("-5000.00")  # 175000 - 180000
        assert asset.profit_loss_rate == Decimal("-0.0278")  # -5000 / 180000

    def test_asset_profit_loss_calculation(self):
        """测试盈亏计算"""
        asset = Asset(
            id=1,
            user_id=1,
            name="Test Stock",
            asset_type=AssetType.STOCK,
            quantity=Decimal("100"),
            cost_basis=Decimal("100.00"),
            current_price=Decimal("120.00"),
        )
        assert asset.total_cost == Decimal("10000.00")
        assert asset.current_value == Decimal("12000.00")
        assert asset.profit_loss == Decimal("2000.00")
        assert asset.profit_loss_rate == Decimal("0.20")  # 20%

    def test_asset_with_zero_quantity(self):
        """测试零数量资产"""
        asset = Asset(
            id=1,
            user_id=1,
            name="Sold Stock",
            asset_type=AssetType.STOCK,
            quantity=Decimal("0"),
            cost_basis=Decimal("100.00"),
            current_price=Decimal("150.00"),
        )
        assert asset.total_cost == Decimal("0")
        assert asset.current_value == Decimal("0")
