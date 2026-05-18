/**
 * TakhleeqX App — Main application with routing and layout.
 */
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Onboarding from './pages/Onboarding';
import AgentMonitor from './pages/AgentMonitor';
import Campaign from './pages/Campaign';
import SocialFeed from './pages/SocialFeed';
import Analytics from './pages/Analytics';
import AboutUs from './pages/AboutUs';

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <div className="flex items-center justify-center min-h-screen"><div className="animate-spin-slow w-8 h-8 border-2 border-primary border-t-transparent rounded-full" /></div>;
  return isAuthenticated ? children : <Navigate to="/login" />;
}

function AppRoutes() {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      <Route path="/login" element={isAuthenticated ? <Navigate to="/" /> : <Login />} />
      <Route path="/register" element={isAuthenticated ? <Navigate to="/" /> : <Register />} />
      <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route index element={<Onboarding />} />
        <Route path="agents" element={<AgentMonitor />} />
        <Route path="campaign" element={<Campaign />} />
        <Route path="feed" element={<SocialFeed />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="about" element={<AboutUs />} />
      </Route>
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </Router>
  );
}

export default App;
