import { useState } from 'react';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import Header from './components/layout/Header';
import Dashboard from './pages/Dashboard';
import HistoricalTrends from './pages/HistoricalTrends';
import Summary from './pages/Summary';

function App() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [dataDate, setDataDate] = useState<string>('');

  const handleRefreshComplete = () => {
    setRefreshKey((prev) => prev + 1);
  };

  const handleQuickRefresh = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <ThemeProvider>
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
        <Header
          dataDate={dataDate}
          onRefreshComplete={handleRefreshComplete}
          onQuickRefresh={handleQuickRefresh}
        />
        <div className="border-b border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <nav className="flex gap-6">
              <NavLink
                to="/"
                end
                className={({ isActive }) =>
                  `py-4 px-1 border-b-2 text-sm font-medium transition-colors ${
                    isActive
                      ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                      : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:border-slate-600'
                  }`
                }
              >
                Dashboard
              </NavLink>
              <NavLink
                to="/historical"
                className={({ isActive }) =>
                  `py-4 px-1 border-b-2 text-sm font-medium transition-colors ${
                    isActive
                      ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                      : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:border-slate-600'
                  }`
                }
              >
                Historical Trends
              </NavLink>
              <NavLink
                to="/summary"
                className={({ isActive }) =>
                  `py-4 px-1 border-b-2 text-sm font-medium transition-colors ${
                    isActive
                      ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                      : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:border-slate-600'
                  }`
                }
              >
                Summary
              </NavLink>
            </nav>
          </div>
        </div>
        <Routes>
          <Route path="/" element={<Dashboard key={refreshKey} onDataLoaded={setDataDate} />} />
          <Route path="/historical" element={<HistoricalTrends key={refreshKey} />} />
          <Route path="/summary" element={<Summary key={refreshKey} />} />
        </Routes>
      </div>
    </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
