import { useState } from 'react';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
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
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50">
        <Header
          dataDate={dataDate}
          onRefreshComplete={handleRefreshComplete}
          onQuickRefresh={handleQuickRefresh}
        />
        <div className="border-b border-slate-200 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <nav className="flex gap-6">
              <NavLink
                to="/"
                end
                className={({ isActive }) =>
                  `py-4 px-1 border-b-2 text-sm font-medium transition-colors ${
                    isActive
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300'
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
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300'
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
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300'
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
  );
}

export default App;
