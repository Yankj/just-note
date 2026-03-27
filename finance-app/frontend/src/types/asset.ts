/**
 * 资产类型定义
 */

export type AssetType = 'STOCK' | 'FUND' | 'CASH' | 'CRYPTO' | 'OTHER';

export interface Asset {
  id: string;
  user_id: string;
  asset_type: AssetType;
  symbol: string;
  name: string;
  market: string | null;
  quantity: number;
  avg_cost: number;
  current_price: number | null;
  market_value: number | null;
  unrealized_pnl: number | null;
  unrealized_pnl_pct: number | null;
  realized_pnl: number;
  is_active: boolean;
  is_hidden: boolean;
  last_synced_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface AssetCreate {
  asset_type: AssetType;
  symbol: string;
  name: string;
  market?: string;
  quantity?: number;
  avg_cost?: number;
}

export interface AssetUpdate {
  name?: string;
  quantity?: number;
  avg_cost?: number;
  is_hidden?: boolean;
}

export interface AssetListResponse {
  items: Asset[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
