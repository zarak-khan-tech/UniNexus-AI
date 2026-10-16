import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CommandCenter from './pages/CommandCenter';
import AuditLogs from './pages/AuditLogs';
import Integrations from './pages/Integrations';
import ExecutionDetail from './pages/ExecutionDetail';
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
import Import from './pages/Import';
import RoleRoute from './components/RoleRoute';

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" replace />;
}

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

        <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/command-center" element={<ProtectedRoute><CommandCenter /></ProtectedRoute>} />
        <Route path="/students" element={<ProtectedRoute><Students /></ProtectedRoute>} />
        <Route path="/courses" element={<ProtectedRoute><Courses /></ProtectedRoute>} />
        <Route path="/knowledge" element={<ProtectedRoute><Knowledge /></ProtectedRoute>} />
        <Route path="/notifications" element={<ProtectedRoute><Notifications /></ProtectedRoute>} />

        <Route path="/analytics" element={<Guarded roles={['admin', 'super_admin', 'faculty']}><Analytics /></Guarded>} />
        <Route path="/tools" element={<Guarded roles={['admin', 'super_admin', 'faculty']}><Tools /></Guarded>} />
        <Route path="/integrations" element={<Guarded roles={['admin', 'super_admin']}><Integrations /></Guarded>} />
        <Route path="/workflows" element={<Guarded roles={['admin', 'super_admin', 'faculty']}><Workflows /></Guarded>} />
        <Route path="/audit" element={<Guarded roles={['admin', 'super_admin', 'faculty']}><AuditLogs /></Guarded>} />
          <Route path="/audit/:id" element={<Guarded roles={['admin', 'super_admin', 'faculty']}><ExecutionDetail /></Guarded>} />

        <Route path="/agents" element={<Guarded roles={['admin', 'super_admin']}><Agents /></Guarded>} />
        <Route path="/approvals" element={<Guarded roles={['admin', 'super_admin']}><Approvals /></Guarded>} />
        <Route path="/settings" element={<Guarded roles={['admin', 'super_admin']}><Settings /></Guarded>} />
        <Route path="/import" element={<Guarded roles={['admin', 'super_admin']}><Import /></Guarded>} />
      </Routes>
    </Router>
  );
}

export default App;
