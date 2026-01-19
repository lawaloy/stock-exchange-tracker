import React, { useRef, useState } from 'react';
import { ArrowPathIcon } from '@heroicons/react/24/outline';
import api from '../../services/api';

interface HeaderProps {
  dataDate?: string;
  onRefreshComplete?: () => void;
  onQuickRefresh?: () => void;
}

const Header: React.FC<HeaderProps> = ({ dataDate, onRefreshComplete, onQuickRefresh }) => {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [refreshMessage, setRefreshMessage] = useState('');
  const pollIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const handleQuickRefresh = () => {
    setRefreshMessage('Reloading data...');
    onQuickRefresh?.();
    setTimeout(() => {
      setRefreshMessage('');
    }, 1000);
  };

  const handleFullRefresh = async () => {
    setIsRefreshing(true);
    setRefreshMessage('Reloading latest saved data...');
    onQuickRefresh?.();

    try {
      setRefreshMessage('Fetching fresh data in the background...');
      // Trigger refresh
      const response = await api.post('/api/refresh');
      setRefreshMessage(response.data.message);

      // Poll for status
      pollIntervalRef.current = setInterval(async () => {
        try {
          const statusRes = await api.get('/api/refresh/status');
          const status = statusRes.data;

          if (status.progress) {
            setRefreshMessage(status.progress);
          }

          if (!status.is_running) {
            if (pollIntervalRef.current) {
              clearInterval(pollIntervalRef.current);
              pollIntervalRef.current = null;
            }
            setIsRefreshing(false);

            if (status.last_status === 'success') {
              setRefreshMessage('✅ Data refresh complete!');
              setTimeout(() => {
                setRefreshMessage('');
                onRefreshComplete?.();
              }, 2000);
            } else {
              setRefreshMessage(`Refresh failed: ${status.progress}`);
              setTimeout(() => setRefreshMessage(''), 5000);
            }
          }
        } catch (err) {
          console.error('Status poll error:', err);
        }
      }, 2000); // Poll every 2 seconds

    } catch (error) {
      console.error('Refresh error:', error);
      setRefreshMessage('Failed to start refresh');
      setIsRefreshing(false);
      setTimeout(() => setRefreshMessage(''), 5000);
    }
  };

  const handleCancelRefresh = async () => {
    setRefreshMessage('Cancelling refresh...');
    try {
      await api.post('/api/refresh/cancel');
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
      setIsRefreshing(false);
      setRefreshMessage('Refresh cancelled.');
      setTimeout(() => setRefreshMessage(''), 3000);
    } catch (error) {
      console.error('Cancel refresh error:', error);
      setRefreshMessage('Failed to cancel refresh ');
      setTimeout(() => setRefreshMessage(''), 5000);
    }
  };

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold text-slate-900">
              📊 Stock Exchange Tracker
            </h1>
            {dataDate && (
              <div className="text-sm text-slate-600">
                <span className="font-medium">Data from:</span>{' '}
                <span className="font-semibold">{dataDate}</span>
              </div>
            )}
          </div>
          <div className="flex items-center space-x-4">
            {refreshMessage && (
              <div className="text-sm text-slate-600 max-w-xs truncate">
                {refreshMessage}
              </div>
            )}
            <button
              onClick={handleQuickRefresh}
              className="flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium bg-green-500 text-white hover:bg-green-600 transition-colors"
              title="Reload data from files (instant)"
            >
              <ArrowPathIcon className="h-5 w-5" />
              <span>Reload</span>
            </button>
            <button
              onClick={handleFullRefresh}
              disabled={isRefreshing}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                isRefreshing
                  ? 'bg-slate-300 text-slate-600 cursor-not-allowed'
                  : 'bg-blue-500 text-white hover:bg-blue-600'
              }`}
              title="Reload saved data instantly and fetch fresh data in background"
            >
              <ArrowPathIcon className={`h-5 w-5 ${isRefreshing ? 'animate-spin' : ''}`} />
              <span>{isRefreshing ? 'Fetching...' : 'Fetch New'}</span>
            </button>
            {isRefreshing && (
              <button
                onClick={handleCancelRefresh}
                className="flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium bg-red-500 text-white hover:bg-red-600 transition-colors"
                title="Cancel the current refresh job"
              >
                <span>Cancel</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
