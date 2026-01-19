import React, { useState } from 'react';
import Header from './components/layout/Header';
import Dashboard from './pages/Dashboard';

function App() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [dataDate, setDataDate] = useState<string>('');

  const handleRefreshComplete = () => {
    // Trigger dashboard re-fetch by changing key
    setRefreshKey((prev) => prev + 1);
  };

  const handleQuickRefresh = () => {
    // Instant reload - just refetch current data
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Header 
        dataDate={dataDate} 
        onRefreshComplete={handleRefreshComplete}
        onQuickRefresh={handleQuickRefresh}
      />
      <Dashboard key={refreshKey} onDataLoaded={setDataDate} />
    </div>
  );
}

export default App;
