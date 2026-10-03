import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CommandCenter from './pages/CommandCenter';
import AuditLogs from './pages/AuditLogs';
import Agents from './pages/Agents';
import Tools from './pages/Tools';
import Approvals from './pages/Approvals';
import Notifications from './pages/Notifications';
import Workflows from './pages/Workflows';
import Students from './pages/Students';
import Courses from './pages/Courses';
import Knowledge from './pages/Knowledge';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';
import RoleRoute from './components/RoleRoute';

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" replace />;
}

// English: Convenience wrapper combining auth + role check.
// Roman Urdu: Auth + role check ko ek saath karne wala wrapper.
function Guarded({ roles, children }) {
  return (
    <ProtectedRoute>
      <RoleRoute allowedRoles={roles}>{children}</RoleRoute>
    </ProtectedRoute>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* English: Pages visible to everyone (any logged-in role). */}
        {/* Roman Urdu: Sab logged-in roles ke liye khuli pages. */}
        <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/command-center" element={<ProtectedRoute><CommandCenter /></ProtectedRoute>} />
        <Route path="/students" element={<ProtectedRoute><Students /></ProtectedRoute>} />
        <Route path="/courses" element={<ProtectedRoute><Courses /></ProtectedRoute>} />
        <Route path="/knowledge" element={<ProtectedRoute><Knowledge /></ProtectedRoute>} />
        <Route path="/notifications" element={<ProtectedRoute><Notifications /></ProtectedRoute>} />

        {/* English: Analytics — admin + faculty only. */}
        <Route path="/analytics" element={
          <Guarded roles={['admin', 'super_admin', 'faculty']}><Analytics /></Guarded>
        } />

        {/* English: Tools, Workflows, Audit — admin + faculty + super_admin. */}
        <Route path="/tools" element={
          <Guarded roles={['admin', 'super_admin', 'faculty']}><Tools /></Guarded>
        } />
        <Route path="/workflows" element={
          <Guarded roles={['admin', 'super_admin', 'faculty']}><Workflows /></Guarded>
        } />
        <Route path="/audit" element={
          <Guarded roles={['admin', 'super_admin', 'faculty']}><AuditLogs /></Guarded>
        } />

        {/* English: Agents, Approvals, Settings — admin + super_admin only. */}
        <Route path="/agents" element={
          <Guarded roles={['admin', 'super_admin']}><Agents /></Guarded>
        } />
        <Route path="/approvals" element={
          <Guarded roles={['admin', 'super_admin']}><Approvals /></Guarded>
        } />
        <Route path="/settings" element={
          <Guarded roles={['admin', 'super_admin']}><Settings /></Guarded>
        } />
      </Routes>
    </Router>
  );
}

export default App;
