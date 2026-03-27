import api from './axios';

// 财务自由规划 API
export const plannerApi = {
  getPlan: () => api.get('/planner/plan'),
  updatePlan: (data: any) => api.post('/planner/plan', data),
  calculateProgress: (data: any) => api.post('/planner/calculate', data),
};

// 投资日记 API
export const diaryApi = {
  getList: (params?: any) => api.get('/diary', { params }),
  getDetail: (id: string) => api.get(`/diary/${id}`),
  create: (data: any) => api.post('/diary', data),
  update: (id: string, data: any) => api.put(`/diary/${id}`, data),
  delete: (id: string) => api.delete(`/diary/${id}`),
};

// 心理诊断 API
export const psychologyApi = {
  assess: (data: any) => api.post('/psychology/assess', data),
  getHistory: () => api.get('/psychology/history'),
  getReport: (id: string) => api.get(`/psychology/report/${id}`),
};

// 资产视图 API
export const assetsApi = {
  getOverview: () => api.get('/assets/overview'),
  getDetails: (type: string) => api.get(`/assets/${type}`),
  updateAsset: (data: any) => api.post('/assets', data),
};

// 被动收入 API
export const passiveIncomeApi = {
  getOverview: () => api.get('/passive-income/overview'),
  getStreams: () => api.get('/passive-income/streams'),
  addStream: (data: any) => api.post('/passive-income/streams', data),
  updateStream: (id: string, data: any) => api.put(`/passive-income/streams/${id}`, data),
};

// AI 对话 API
export const chatApi = {
  sendMessage: (data: any) => api.post('/chat/message', data),
  getHistory: () => api.get('/chat/history'),
  clearHistory: () => api.delete('/chat/history'),
};
