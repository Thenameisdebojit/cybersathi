import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import DashboardPage from './pages/DashboardPage';
import TrackerPage from './pages/TrackerPage';
import AwarenessPage from './pages/AwarenessPage';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/tracker" element={<TrackerPage />} />
          <Route path="/awareness" element={<AwarenessPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
