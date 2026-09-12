import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/client';

export default function Register() {
  const [form, setForm] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    role: 'admin',
    tenantId: 1,
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (form.password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }
    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      await api.post('/auth/register', {
        email: form.email,
        password: form.password,
        role: form.role,
        tenant_id: parseInt(form.tenantId, 10),
      });
      // On success, log the user in
      const formData = new URLSearchParams();
      formData.append('username', form.email);
      formData.append('password', form.password);
      const loginRes = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      localStorage.setItem('token', loginRes.data.access_token);
      window.location.href = '/';
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : 'Registration failed. Email may already be registered.');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 px-4">
      <div className="bg-slate-800 p-8 rounded-xl shadow-2xl w-full max-w-md border border-slate-700">
        <h2 className="text-2xl font-bold text-white mb-2">Create Account</h2>
        <p className="text-sm text-slate-400 mb-6">Join the UniNexus AI platform</p>

        {error && (
          <div className="bg-red-900/50 text-red-200 text-sm p-3 rounded mb-4 border border-red-700">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1">Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
              placeholder="you@university.edu"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1">Password</label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
              placeholder="At least 8 characters"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1">Confirm Password</label>
            <input
              type="password"
              name="confirmPassword"
              value={form.confirmPassword}
              onChange={handleChange}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
              placeholder="Repeat password"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1">Role</label>
            <select
              name="role"
              value={form.role}
              onChange={handleChange}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
            >
              <option value="admin">University Admin</option>
              <option value="faculty">Faculty</option>
              <option value="student">Student</option>
              <option value="researcher">Researcher</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1">Tenant ID</label>
            <input
              type="number"
              name="tenantId"
              value={form.tenantId}
              onChange={handleChange}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
              required
            />
            <p className="text-xs text-slate-500 mt-1">
              For the demo: use <span className="text-slate-300 font-mono">1</span> (Demo University)
            </p>
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 text-white font-medium py-2 rounded-lg transition-colors"
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-slate-400">
          Already have an account?{' '}
          <Link to="/login" className="text-blue-400 hover:text-blue-300 font-medium">
            Sign in
          </Link>
        </div>
      </div>
    </div>
  );
}
