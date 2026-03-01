import React, { useEffect, useRef, useState } from 'react';
import { ArrowPathIcon } from '@heroicons/react/24/outline';
import axios from 'axios';
import ExportButton from '../components/common/ExportButton';
import api, { summaryApi } from '../services/api';
import { formatDate } from '../utils/formatters';

const Summary: React.FC = () => {
  const [summary, setSummary] = useState<string>('');
  const [date, setDate] = useState<string>('');
  const [source, setSource] = useState<'ai' | 'demo'>('demo');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const summaryRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchSummary();
  }, []);

  const fetchSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await summaryApi.getSummary();
      setSummary(res.data.summary);
      setDate(res.data.date);
      setSource(res.data.source);
    } catch (e) {
      let msg = 'Unable to load summary.';
      if (axios.isAxiosError(e)) {
        const status = e.response?.status;
        if (status === 404) {
          msg = 'show-fetch-button';
        } else if (status && status >= 500) {
          msg = 'Something went wrong. Please try again later.';
        } else if (e.code === 'ECONNREFUSED' || e.message?.includes('Network Error')) {
          msg = 'Unable to connect. Please try again.';
        }
      }
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleFetchNew = async () => {
    setIsRefreshing(true);
    try {
      await api.post('/api/refresh');
      const poll = async (): Promise<void> => {
        const statusRes = await api.get('/api/refresh/status');
        if (statusRes.data.is_running) {
          await new Promise((r) => setTimeout(r, 2000));
          return poll();
        }
        if (statusRes.data.last_status === 'success') {
          await fetchSummary();
        }
        setIsRefreshing(false);
      };
      await poll();
    } catch {
      setIsRefreshing(false);
      setError('Failed to start refresh. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="animate-pulse card p-8">
          <div className="h-4 bg-slate-200 dark:bg-slate-600 rounded w-1/4 mb-4" />
          <div className="space-y-2">
            <div className="h-3 bg-slate-200 dark:bg-slate-600 rounded" />
            <div className="h-3 bg-slate-200 dark:bg-slate-600 rounded" />
            <div className="h-3 bg-slate-200 dark:bg-slate-600 rounded w-3/4" />
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    const showFetchButton = error === 'show-fetch-button';
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-600 rounded-lg p-6">
          <p className="text-slate-700 dark:text-slate-300 mb-4">
            {showFetchButton
              ? 'No summary available yet.'
              : error}
          </p>
          {showFetchButton && (
            <button
              onClick={handleFetchNew}
              disabled={isRefreshing}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium bg-blue-500 text-white hover:bg-blue-600 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors"
            >
              <ArrowPathIcon className={`h-5 w-5 ${isRefreshing ? 'animate-spin' : ''}`} />
              {isRefreshing ? 'Fetching...' : 'Fetch New'}
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div ref={summaryRef} className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="card">
        <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-600 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <h1 className="text-xl font-semibold text-slate-900 dark:text-slate-100">Market Summary</h1>
          <div className="flex items-center gap-3 flex-wrap">
            <ExportButton captureRef={summaryRef} formats={['png', 'pdf']} label="Summary" />
            <span className="text-sm text-slate-500 dark:text-slate-400">
              {date ? formatDate(date) : '—'}
            </span>
            <span
              className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                source === 'ai'
                  ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400'
                  : 'bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-300'
              }`}
            >
              {source === 'ai' ? 'Expert Summary' : 'Summary'}
            </span>
          </div>
        </div>
        <div className="px-6 py-6">
          <p className="text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-wrap">
            {summary}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Summary;
