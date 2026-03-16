import { AxiosInstance } from 'axios';

export interface MarketInsightData {
  market_data: Record<string, unknown>;
  weather_data: Record<string, unknown>;
  crop_data: Record<string, unknown>;
}

export const fetchMarketInsight = async (
  api: AxiosInstance,
  { market_data, weather_data, crop_data }: MarketInsightData
) => {
  const response = await api.post('/ai/market-insight/', {
    market_data,
    weather_data,
    crop_data,
  });
  return response.data;
};