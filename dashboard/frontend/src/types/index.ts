// API Response Types

export interface IndexData {
  stocks: number;
  avgChange: number;
  gainers: number;
  losers: number;
}

export interface MarketOverview {
  date: string;
  totalStocks: number;
  gainers: number;
  losers: number;
  unchanged: number;
  averageChange: number;
  maxChange: number;
  minChange: number;
  indices: Record<string, IndexData>;
}

export interface StockMover {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
}

export interface MoversResponse {
  type: string;
  data: StockMover[];
}

export interface ProjectionsSummary {
  date: string;
  targetDate: string;
  totalProjections: number;
  averageConfidence: number;
  expectedMarketMove: number;
  sentiment: string;
  recommendations: Record<string, number>;
  trends: Record<string, number>;
  riskProfile: Record<string, number>;
}

export interface Opportunity {
  symbol: string;
  name: string;
  currentPrice: number;
  targetPrice: number;
  expectedChange: number;
  confidence: number;
  risk: string;
  trend: string;
  reason: string;
  volume: number;
  momentum?: number;
  volatility?: number;
}

export interface OpportunitiesResponse {
  type: string;
  count: number;
  opportunities: Opportunity[];
}

export interface CurrentData {
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  marketCap?: number;
}

export interface ProjectionData {
  targetDate: string;
  targetPrice: number;
  expectedChange: number;
  confidence: number;
  recommendation: string;
  risk: string;
  trend: string;
}

export interface TechnicalData {
  momentum?: number;
  volatility?: number;
  rsi?: number;
}

export interface StockDetail {
  symbol: string;
  name: string;
  currentData: CurrentData;
  projection?: ProjectionData;
  technical?: TechnicalData;
}

export interface HistoricalPoint {
  date: string;
  close: number;
  change: number;
  volume: number;
  projection?: {
    targetPrice: number;
    confidence: number;
    recommendation: string;
  };
}

export interface HistoricalData {
  symbol: string;
  data: HistoricalPoint[];
}

export interface DailySummaryPoint {
  date: string;
  totalProjections: number;
  averageConfidence: number;
  expectedMarketMove: number;
  sentiment: string;
  strongBuy: number;
  buy: number;
  hold: number;
  sell: number;
  strongSell: number;
}

export interface HistoricalSummaryResponse {
  dates: string[];
  data: DailySummaryPoint[];
  firstDate: string;
  lastDate: string;
  symbols?: string[];
  names?: Record<string, string>;
}

export interface MarketSummaryResponse {
  date: string;
  summary: string;
  source: 'ai' | 'demo';
}
