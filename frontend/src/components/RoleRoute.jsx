import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/client';
import Layout from './Layout';

// English: Route wrapper that checks the current user's role before rendering.
//         Non-matching roles see a friendly Access Denied page (not a redirect).
// Roman Urdu: Route wrapper jo render se pehle current user ka role check karta
//             hai. Ghair-mutabiq roles ko friendly Access Denied page dikhta hai.
export default function RoleRoute({ children, allowedRoles }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get('/auth/me');
        setUser(res.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Could not verify your account.');
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, []);

  if (loading) {
    return (
      <Layout>
        <div className="p-8 max-w-3xl mx-auto">
          <div className="bg-white border border-ink-200 rounded-2xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Checking access…</div>
          </div>
        </div>
      </Layout>
    );
  }

  const role = (user?.role || '').toLowerCase();
  const allowed = (allowedRoles || []).map((r) => r.toLowerCase());
  const isAllowed = allowed.length === 0 || allowed.includes(role);

  if (error || !isAllowed) {
    return (
      <Layout>
        <div className="p-8 max-w-3xl mx-auto animate-fade-in">
          <div className="relative bg-gradient-to-br from-white to-ink-50/50 border-2 border-dashed border-ink-200 rounded-2xl p-16 text-center overflow-hidden">
            <div className="relative">
              <div className="w-16 h-16 mx-auto mb-5 rounded-2xl bg-amber-100 flex items-center justify-center">
                <svg className="w-8 h-8 text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M12 9v2m0 4h.01M5.07 19h13.86a2 2 0 001.71-3.01l-6.93-12a2 2 0 00-3.42 0l-6.93 12A2 2 0 005.07 19z" />
                </svg>
              </div>
              <h2 className="font-display text-2xl font-bold text-ink-900 mb-2">Access denied</h2>
              <p className="text-sm text-ink-500 max-w-md mx-auto mb-6">
                {error || (
                  <>
                    Your current role <span className="font-semibold text-ink-700">({role || 'unknown'})</span> does not have access to this page.
                    Contact your administrator if you believe this is a mistake.
                  </>
                )}
              </p>
              <div className="flex items-center justify-center gap-3">
                <Link
                  to="/"
                  className="inline-flex items-center gap-2 gradient-gold text-ink-950 font-bold px-5 py-2.5 rounded-lg shadow-card hover:shadow-card-hover hover:-translate-y-0.5 transition-all"
                >
                  Back to Dashboard
                </Link>
                <Link
                  to="/command-center"
                  className="inline-flex items-center gap-2 bg-white border border-ink-200 hover:border-ink-400 text-ink-700 hover:text-ink-900 font-semibold px-5 py-2.5 rounded-lg shadow-card transition-all"
                >
                  Open Command Center
                </Link>
              </div>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return children;
}
