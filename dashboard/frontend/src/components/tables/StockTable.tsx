import React, { useState } from 'react';
import { formatPrice, formatPercentage, getRecommendationColor, getRiskColor } from '../../utils/formatters';
import type { Opportunity } from '../../types';

interface StockTableProps {
  stocks: Opportunity[];
  onStockClick?: (symbol: string) => void;
}

const StockTable: React.FC<StockTableProps> = ({ stocks, onStockClick }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRec, setFilterRec] = useState('All');
  const itemsPerPage = 20;

  // Filter stocks
  const filteredStocks = stocks.filter(stock => {
    const matchesSearch = 
      stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
      stock.name.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilter = 
      filterRec === 'All' || 
      (filterRec === 'BUY' && (stock.trend === 'STRONG BUY' || stock.trend === 'BUY')) ||
      (filterRec === 'HOLD' && stock.trend === 'HOLD') ||
      (filterRec === 'SELL' && (stock.trend === 'STRONG SELL' || stock.trend === 'SELL'));
    
    return matchesSearch && matchesFilter;
  });

  // Paginate
  const totalPages = Math.ceil(filteredStocks.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedStocks = filteredStocks.slice(startIndex, startIndex + itemsPerPage);

  return (
    <div className="card p-6">
      <div className="mb-4 flex items-center justify-between gap-4">
        <h3 className="text-lg font-semibold">All Stocks</h3>
        <div className="flex items-center gap-3">
          <input
            type="text"
            placeholder="Search stocks..."
            className="px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <select
            className="px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={filterRec}
            onChange={(e) => setFilterRec(e.target.value)}
          >
            <option value="All">All</option>
            <option value="BUY">Buy</option>
            <option value="HOLD">Hold</option>
            <option value="SELL">Sell</option>
          </select>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 uppercase">#</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 uppercase">Symbol</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 uppercase">Name</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-slate-600 uppercase">Price</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-slate-600 uppercase">Target</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-slate-600 uppercase">Change</th>
              <th className="px-4 py-3 text-center text-xs font-medium text-slate-600 uppercase">Conf</th>
              <th className="px-4 py-3 text-center text-xs font-medium text-slate-600 uppercase">Risk</th>
              <th className="px-4 py-3 text-center text-xs font-medium text-slate-600 uppercase">Trend</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {paginatedStocks.map((stock, index) => (
              <tr
                key={stock.symbol}
                className="hover:bg-slate-50 cursor-pointer"
                onClick={() => onStockClick?.(stock.symbol)}
              >
                <td className="px-4 py-3 text-sm text-slate-600">
                  {startIndex + index + 1}
                </td>
                <td className="px-4 py-3 text-sm font-medium text-slate-900">
                  {stock.symbol}
                </td>
                <td className="px-4 py-3 text-sm text-slate-600 max-w-xs truncate">
                  {stock.name}
                </td>
                <td className="px-4 py-3 text-sm text-right">
                  {formatPrice(stock.currentPrice)}
                </td>
                <td className="px-4 py-3 text-sm text-right">
                  {formatPrice(stock.targetPrice)}
                </td>
                <td className={`px-4 py-3 text-sm text-right font-medium ${
                  stock.expectedChange >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {formatPercentage(stock.expectedChange)}
                </td>
                <td className="px-4 py-3 text-sm text-center">
                  {stock.confidence}%
                </td>
                <td className="px-4 py-3 text-center">
                  <span className={`badge ${getRiskColor(stock.risk)}`}>
                    {stock.risk}
                  </span>
                </td>
                <td className="px-4 py-3 text-center">
                  <span className={`badge ${getRecommendationColor(stock.trend)}`}>
                    {stock.trend}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="mt-4 flex items-center justify-center gap-2">
          <button
            className="px-3 py-1 border rounded disabled:opacity-50"
            disabled={currentPage === 1}
            onClick={() => setCurrentPage(p => p - 1)}
          >
            Previous
          </button>
          <span className="text-sm text-slate-600">
            Page {currentPage} of {totalPages}
          </span>
          <button
            className="px-3 py-1 border rounded disabled:opacity-50"
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage(p => p + 1)}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default StockTable;
