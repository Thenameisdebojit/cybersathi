import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import FloatingChatbot from './components/FloatingChatbot';
import LandingPage from './pages/LandingPage';
import NewLoginPage from './pages/NewLoginPage';
import SignupPage from './pages/SignupPage';
import GoogleCallbackPage from './pages/GoogleCallbackPage';
import DashboardPage from './pages/DashboardPage';
import TrackerPage from './pages/TrackerPage';
import AwarenessPage from './pages/AwarenessPage';
import ProfilePage from './pages/ProfilePage';
import SettingsPage from './pages/SettingsPage';
import ComplaintsPage from './pages/ComplaintsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import CampaignsPage from './pages/CampaignsPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<NewLoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/auth/google/callback" element={<GoogleCallbackPage />} />
        
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <div className="min-h-screen bg-gradient-to-br from-gray-50 via-primary-50/10 to-white">
                <Navbar />
                <Routes>
                  <Route path="/dashboard" element={<DashboardPage />} />
                  <Route path="/complaints" element={<ComplaintsPage />} />
                  <Route path="/analytics" element={<AnalyticsPage />} />
                  <Route path="/campaigns" element={<CampaignsPage />} />
                  <Route path="/tracker" element={<TrackerPage />} />
                  <Route path="/awareness" element={<AwarenessPage />} />
                  <Route path="/profile" element={<ProfilePage />} />
                  <Route path="/settings" element={<SettingsPage />} />
                </Routes>
                <FloatingChatbot />
              </div>
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
