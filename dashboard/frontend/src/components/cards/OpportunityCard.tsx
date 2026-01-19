import React from 'react';
import { formatPrice, formatPercentage, getRiskColor, getTrendIcon } from '../../utils/formatters';
import CompanyLogo from '../common/CompanyLogo';
import type { Opportunity } from '../../types';

interface OpportunityCardProps {
  opportunity: Opportunity;
  onClick?: () => void;
}

const OpportunityCard: React.FC<OpportunityCardProps> = ({ opportunity, onClick }) => {
  return (
    <div
      className="card p-4 cursor-pointer hover:border-blue-300"
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div>
            <div className="flex items-center space-x-2">
              <CompanyLogo symbol={opportunity.symbol} name={opportunity.name} size={24} />
              <span className="font-semibold text-lg">{opportunity.symbol}</span>
              <span className="text-sm text-slate-600">{opportunity.name}</span>
            </div>
            <div className="flex items-center space-x-2 mt-1 text-sm">
              <span>{formatPrice(opportunity.currentPrice)}</span>
              <span className="text-slate-400">→</span>
              <span className="font-medium">{formatPrice(opportunity.targetPrice)}</span>
              <span className={opportunity.expectedChange >= 0 ? 'text-green-600' : 'text-red-600'}>
                ({formatPercentage(opportunity.expectedChange)})
              </span>
            </div>
          </div>
        </div>
        <div className="flex flex-col items-end space-y-1">
          <div className="flex items-center space-x-2">
            <span className="text-sm font-medium">{opportunity.confidence}% conf</span>
            <span className={`badge ${getRiskColor(opportunity.risk)}`}>
              {opportunity.risk} risk
            </span>
          </div>
          <div className="flex items-center space-x-1 text-sm text-slate-600">
            <span>{getTrendIcon(opportunity.trend)}</span>
            <span>{opportunity.trend}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OpportunityCard;
