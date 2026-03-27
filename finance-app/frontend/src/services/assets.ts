/**
 * 资产 API 服务
 */
import apiClient from './api';
import type { Asset, AssetCreate, AssetUpdate, AssetListResponse } from '../types/asset';

export const AssetService = {
  /**
   * 获取资产列表
   */
  async getAll(params?: {
    asset_type?: string;
    is_active?: boolean;
    page?: number;
    page_size?: number;
  }): Promise<AssetListResponse> {
    const response = await apiClient.get<AssetListResponse>('/assets', { params });
    return response.data;
  },

  /**
   * 获取资产详情
   */
  async getById(id: string): Promise<Asset> {
    const response = await apiClient.get<Asset>(`/assets/${id}`);
    return response.data;
  },

  /**
   * 创建资产
   */
  async create(data: AssetCreate): Promise<Asset> {
    const response = await apiClient.post<Asset>('/assets', data);
    return response.data;
  },

  /**
   * 更新资产
   */
  async update(id: string, data: AssetUpdate): Promise<Asset> {
    const response = await apiClient.put<Asset>(`/assets/${id}`, data);
    return response.data;
  },

  /**
   * 删除资产
   */
  async delete(id: string): Promise<void> {
    await apiClient.delete(`/assets/${id}`);
  },

  /**
   * 同步资产价格
   */
  async syncPrice(id: string): Promise<Asset> {
    const response = await apiClient.post<Asset>(`/assets/${id}/sync`);
    return response.data;
  },
};
