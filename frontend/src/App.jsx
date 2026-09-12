import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import CommandCenter from './pages/CommandCenter';
import AuditLogs from './pages/AuditLogs';
import Agents from './pages/Agents';
import Students from './pages/Students';
import Courses from './pages/Courses';
import Knowledge from './pages/Knowledge';

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/command-center" element={<ProtectedRoute><CommandCenter /></ProtectedRoute>} />
        <Route path="/audit" element={<ProtectedRoute><AuditLogs /></ProtectedRoute>} />
        <Route path="/agents" element={<ProtectedRoute><Agents /></ProtectedRoute>} />
        <Route path="/students" element={<ProtectedRoute><Students /></ProtectedRoute>} />
        <Route path="/courses" element={<ProtectedRoute><Courses /></ProtectedRoute>} />
        <Route path="/knowledge" element={<ProtectedRoute><Knowledge /></ProtectedRoute>} />
      </Routes>
    </Router>
  );
}

export default App;
