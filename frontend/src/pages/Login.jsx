import { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/client';

export default function Login() {
  const [email, setEmail] = useState('admin@demo.university.edu');
  const [password, setPassword] = useState('securepassword123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);
      const response = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      localStorage.setItem('token', response.data.access_token);
      window.location.href = '/';
    } catch (err) {
      setError('Invalid credentials or server error.');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
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
            Autonomous multi-agent intelligence for higher education.
          </h1>
          <p className="text-ink-200 text-lg leading-relaxed mb-8">
            A genuine orchestration layer over your university's data. Specialized AI agents plan, retrieve, analyze, and act with your institution's policies and audit trail intact.
          </p>
          <div className="grid grid-cols-3 gap-4 pt-8 border-t border-white/10">
            <div><div className="text-2xl font-display font-bold text-gold-300">4</div><div className="text-xs uppercase tracking-wider text-ink-300 mt-1">Agents</div></div>
            <div><div className="text-2xl font-display font-bold text-gold-300">Multi</div><div className="text-xs uppercase tracking-wider text-ink-300 mt-1">Tenant</div></div>
            <div><div className="text-2xl font-display font-bold text-gold-300">LLM</div><div className="text-xs uppercase tracking-wider text-ink-300 mt-1">Planned</div></div>
          </div>
        </div>
        <div className="relative z-10 text-xs text-ink-400">Built by <span className="text-ink-200 font-medium">ZARAK KHAN</span> · 2026</div>
      </div>

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
            <h2 className="font-display text-3xl font-bold text-ink-900 mb-2">Welcome back</h2>
            <p className="text-ink-500">Sign in to your university intelligence platform.</p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 text-sm p-3 rounded-lg mb-5">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-ink-700 mb-1.5">Email address</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 focus:outline-none focus:border-ink-500 focus:ring-2 focus:ring-ink-500/10 transition-all shadow-inset-soft"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-ink-700 mb-1.5">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 focus:outline-none focus:border-ink-500 focus:ring-2 focus:ring-ink-500/10 transition-all shadow-inset-soft"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-ink-900 hover:bg-ink-800 disabled:bg-ink-400 text-white font-medium py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </form>

          <div className="mt-8 text-center text-sm text-ink-500">
            Don't have an account?{' '}
            <Link to="/register" className="text-ink-900 hover:text-ink-700 font-semibold underline decoration-gold-400 underline-offset-4">
              Create one
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
