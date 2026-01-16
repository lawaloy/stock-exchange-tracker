import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import type { StockMover } from '../../types';

interface GainersLosersChartProps {
  gainers: StockMover[];
  losers: StockMover[];
}

const GainersLosersChart: React.FC<GainersLosersChartProps> = ({ gainers, losers }) => {
  // Take top 5 gainers and top 5 losers
  const topGainers = gainers.slice(0, 5);
  const topLosers = losers.slice(0, 5);

  // Combine and format data
  const data = [
    ...topGainers.map(g => ({
      symbol: g.symbol,
      change: g.changePercent,
      type: 'gainer'
    })),
    ...topLosers.map(l => ({
      symbol: l.symbol,
      change: l.changePercent,
      type: 'loser'
    }))
  ];

  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold mb-4">Top Movers</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis dataKey="symbol" type="category" width={60} />
          <Tooltip
            formatter={(value: number) => `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`}
          />
          <Bar dataKey="change" radius={[0, 4, 4, 0]}>
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.change >= 0 ? '#10B981' : '#EF4444'}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default GainersLosersChart;
