import axios from 'axios';
import type {
  MarketOverview,
  MoversResponse,
  ProjectionsSummary,
  OpportunitiesResponse,
  StockDetail,
  HistoricalData,
  HistoricalSummaryResponse,
  MarketSummaryResponse,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL ?? '';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Log API failures in development only
if (import.meta.env.DEV) {
  api.interceptors.response.use(
    (res) => res,
    (err) => {
      console.error('[API] Request failed:', err.config?.url, err.response?.status, err.message);
      return Promise.reject(err);
    }
  );
}

// Market endpoints
export const marketApi = {
  getOverview: () => api.get<MarketOverview>('/api/market/overview'),
  getMovers: (type: 'gainers' | 'losers', limit: number = 10) =>
    api.get<MoversResponse>('/api/market/movers', { params: { type, limit } }),
};

// Projections endpoints
export const projectionsApi = {
  getSummary: () => api.get<ProjectionsSummary>('/api/projections/summary'),
  getOpportunities: (type: string, limit: number = 10) =>
    api.get<OpportunitiesResponse>('/api/projections/opportunities', {
      params: { type, limit },
    }),
};

// Summary endpoint (market AI/demo summary)
export const summaryApi = {
  getSummary: () => api.get<MarketSummaryResponse>('/api/summary'),
};

// History endpoints
export const historyApi = {
  getDates: () => api.get<{ dates: string[] }>('/api/history/dates'),
  getSummary: (days: number = 30) =>
    api.get<HistoricalSummaryResponse>('/api/history/summary', { params: { days } }),
  getSymbols: () =>
    api.get<{ symbols: string[]; names: Record<string, string>; date: string }>('/api/history/symbols'),
};

// Stocks endpoints
export const stocksApi = {
  getDetail: (symbol: string) => api.get<StockDetail>(`/api/stocks/${symbol}`),
  getHistorical: (symbol: string, days: number = 30) =>
    api.get<HistoricalData>(`/api/stocks/${symbol}/historical`, {
      params: { days },
    }),
};

export default api;
