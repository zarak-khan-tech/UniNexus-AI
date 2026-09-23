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
    <div className="min-h-screen flex">
      {/* Left panel — academic brand story */}
      <div className="hidden lg:flex lg:w-1/2 relative bg-ink-950 text-white p-12 flex-col justify-between overflow-hidden">
        <div className="absolute -top-40 -right-40 w-96 h-96 rounded-full bg-ink-800/40 blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-96 h-96 rounded-full bg-gold-500/10 blur-3xl" />

        <div className="relative z-10 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center font-display font-bold text-ink-950 text-lg">U</div>
          <div>
            <div className="font-display font-bold text-lg tracking-tight">UniNexus AI</div>
            <div className="text-xs text-ink-300 tracking-widest uppercase">Academic Intelligence</div>
          </div>
        </div>

        <div className="relative z-10 max-w-md">
          <h1 className="font-display text-4xl xl:text-5xl font-bold leading-tight mb-6 text-white">
            Join the platform.
          </h1>
          <p className="text-ink-200 text-lg leading-relaxed mb-8">
            Create an account to access your university's intelligence layer — from AI-driven academic insights to autonomous multi-agent workflows.
          </p>

          <div className="space-y-4 pt-6 border-t border-white/10">
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-gold-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                <svg className="w-3.5 h-3.5 text-gold-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" /></svg>
              </div>
              <div>
                <div className="text-white font-medium">Multi-tenant by design</div>
                <div className="text-sm text-ink-300">Your institution's data stays isolated.</div>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-gold-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                <svg className="w-3.5 h-3.5 text-gold-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" /></svg>
              </div>
              <div>
                <div className="text-white font-medium">Full audit trail</div>
                <div className="text-sm text-ink-300">Every agent action is traceable.</div>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-gold-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                <svg className="w-3.5 h-3.5 text-gold-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" /></svg>
              </div>
              <div>
                <div className="text-white font-medium">Local-first AI</div>
                <div className="text-sm text-ink-300">Runs with your own models. No paid APIs required.</div>
              </div>
            </div>
          </div>
        </div>

        <div className="relative z-10 text-xs text-ink-400">Built by <span className="text-ink-200 font-medium">ZARAK KHAN</span> · 2026</div>
      </div>

      {/* Right panel — registration form */}
      <div className="flex-1 flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-md animate-slide-up">
          <div className="lg:hidden flex items-center gap-3 mb-8">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center font-display font-bold text-ink-950">U</div>
            <div>
              <div className="font-display font-bold text-lg tracking-tight text-ink-900">UniNexus AI</div>
              <div className="text-xs text-ink-400 tracking-widest uppercase">Academic Intelligence</div>
            </div>
          </div>

          <div className="mb-8">
            <h2 className="font-display text-3xl font-bold text-ink-900 mb-2">Create your account</h2>
            <p className="text-ink-500">Get started with your university intelligence platform.</p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 text-sm p-3 rounded-lg mb-5">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-ink-700 mb-1.5">Email address</label>
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                placeholder="you@university.edu"
                className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 placeholder-ink-400 focus:outline-none focus:border-ink-500 focus:ring-2 focus:ring-ink-500/10 transition-all shadow-inset-soft"
                required
              />
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-ink-700 mb-1.5">Password</label>
                <input
                  type="password"
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  placeholder="8+ characters"
                  className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 placeholder-ink-400 focus:outline-none focus:border-ink-500 focus:ring-2 focus:ring-ink-500/10 transition-all shadow-inset-soft"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-ink-700 mb-1.5">Confirm</label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={form.confirmPassword}
                  onChange={handleChange}
                  placeholder="Repeat"
                  className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 placeholder-ink-400 focus:outline-none focus:border-ink-500 focus:ring-2 focus:ring-ink-500/10 transition-all shadow-inset-soft"
                  required
                />
              </div>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-ink-700 mb-1.5">Role</label>
                <select
                  name="role"
                  value={form.role}
                  onChange={handleChange}
                  className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 focus:outline-none focus:border-ink-500 focus:ring-2 focus:ring-ink-500/10 transition-all shadow-inset-soft"
                >
                  <option value="admin">University Admin</option>
                  <option value="faculty">Faculty</option>
                  <option value="student">Student</option>
                  <option value="researcher">Researcher</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-ink-700 mb-1.5">Tenant ID</label>
                <input
                  type="number"
                  name="tenantId"
                  value={form.tenantId}
                  onChange={handleChange}
                  className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 focus:outline-none focus:border-ink-500 focus:ring-2 focus:ring-ink-500/10 transition-all shadow-inset-soft"
                  required
                />
              </div>
            </div>
            <p className="text-xs text-ink-400 -mt-1">For the demo, use tenant ID <span className="font-mono text-ink-600">1</span> (Demo University).</p>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-ink-900 hover:bg-ink-800 disabled:bg-ink-400 text-white font-medium py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover mt-2"
            >
              {loading ? 'Creating your account...' : 'Create account'}
            </button>
          </form>

          <div className="mt-8 text-center text-sm text-ink-500">
            Already have an account?{' '}
            <Link to="/login" className="text-ink-900 hover:text-ink-700 font-semibold underline decoration-gold-400 underline-offset-4">
              Sign in
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
