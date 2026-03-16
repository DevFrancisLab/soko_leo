import { useState } from 'react';
import { useAuth } from '@/context/useAuth';
import { fetchMarketInsight } from '@/api/marketInsights';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';

const MarketInsights = () => {
  const { api } = useAuth();
  const [marketData, setMarketData] = useState('');
  const [weatherData, setWeatherData] = useState('');
  const [cropData, setCropData] = useState('');
  const [insights, setInsights] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setInsights(null);

    try {
      // Parse inputs as JSON (assuming JSON input)
      const parsedMarketData = JSON.parse(marketData);
      const parsedWeatherData = JSON.parse(weatherData);
      const parsedCropData = JSON.parse(cropData);

      const result = await fetchMarketInsight(api, {
        market_data: parsedMarketData,
        weather_data: parsedWeatherData,
        crop_data: parsedCropData,
      });

      setInsights(result);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to fetch insights');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <Card>
        <CardHeader>
          <CardTitle>Market Insights Generator</CardTitle>
          <CardDescription>
            Enter market, weather, and crop data to generate actionable insights using AI.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <Label htmlFor="marketData">Market Data (JSON)</Label>
              <Textarea
                id="marketData"
                value={marketData}
                onChange={(e) => setMarketData(e.target.value)}
                placeholder='{"prices": [...], "trends": [...]}'
                rows={4}
                required
              />
            </div>
            <div>
              <Label htmlFor="weatherData">Weather Data (JSON)</Label>
              <Textarea
                id="weatherData"
                value={weatherData}
                onChange={(e) => setWeatherData(e.target.value)}
                placeholder='{"temperature": 25, "rainfall": 10}'
                rows={4}
                required
              />
            </div>
            <div>
              <Label htmlFor="cropData">Crop Data (JSON)</Label>
              <Textarea
                id="cropData"
                value={cropData}
                onChange={(e) => setCropData(e.target.value)}
                placeholder='{"crop_type": "maize", "yield": 100}'
                rows={4}
                required
              />
            </div>
            <Button type="submit" disabled={loading} className="w-full">
              {loading ? 'Generating Insights...' : 'Generate Insights'}
            </Button>
          </form>

          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          {insights && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold mb-4">Actionable Insights</h3>
              <Card>
                <CardContent className="pt-6">
                  <pre className="whitespace-pre-wrap text-sm">{JSON.stringify(insights, null, 2)}</pre>
                </CardContent>
              </Card>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default MarketInsights;