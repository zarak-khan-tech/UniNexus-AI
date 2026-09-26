import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

// English: Format duration into a human-readable string.
// Roman Urdu: Duration ko insaan ke parhne layak format mein convert karo.
function formatDuration(ms) {
  if (ms == null) return '—';
  if (ms < 1000) return Math.round(ms) + ' ms';
  return (ms / 1000).toFixed(2) + ' s';
}

// English: Format ISO timestamp to a short readable form.
// Roman Urdu: ISO timestamp ko chhote readable form mein convert karo.
function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

// English: Success rate and average duration summary.
// Roman Urdu: Success rate aur average duration ka summary.
function computeStats(rows) {
  if (rows.length === 0) return { total: 0, completed: 0, avgMs: 0 };
  const completed = rows.filter((r) => r.status === 'completed').length;
  const durations = rows.map((r) => r.duration_ms || 0).filter((m) => m > 0);
  const avgMs = durations.length
    ? Math.round(durations.reduce((a, b) => a + b, 0) / durations.length)
    : 0;
  return { total: rows.length, completed, avgMs };
}

export default function AuditLogs() {
  const [executions, setExecutions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');

  const fetchLogs = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/agents/executions?limit=50');
      setExecutions(response.data.executions);
    } catch (err) {
      console.error('Failed to fetch audit logs:', err);
      setError(err.response?.data?.detail || 'Failed to load audit logs.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  const filtered = executions.filter((r) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      (r.user_email || '').toLowerCase().includes(q) ||
      (r.original_request || '').toLowerCase().includes(q) ||
      String(r.id).includes(q)
    );
  });

  const stats = computeStats(executions);

  return (
    <Layout>
      <div className="p-8 max-w-6xl mx-auto animate-fade-in">
        {/* ==================== Header ==================== */}
        <div className="mb-8 flex flex-wrap items-start justify-between gap-4">
          <div>
            <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">
              Audit Logs
            </h1>
            <p className="text-ink-500 text-[15px] leading-relaxed">
              Complete history of every agent execution for your institution.
            </p>
          </div>
          <button
            onClick={fetchLogs}
            disabled={loading}
            className="inline-flex items-center gap-2 text-sm bg-ink-900 hover:bg-ink-800 disabled:bg-ink-400 text-white font-semibold px-4 py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover hover:-translate-y-0.5 disabled:hover:translate-y-0"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {loading ? 'Refreshing…' : 'Refresh'}
          </button>
        </div>

        {/* ==================== Summary Cards ==================== */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">
              Total Executions
            </div>
            <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">
              {loading ? '—' : stats.total}
            </div>
          </div>
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">
              Successful
            </div>
            <div className="text-3xl font-display font-bold text-emerald-600 tracking-tight">
              {loading ? '—' : stats.completed}
            </div>
          </div>
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">
              Avg Duration
            </div>
            <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">
              {loading ? '—' : formatDuration(stats.avgMs)}
            </div>
          </div>
        </div>

        {/* ==================== Search ==================== */}
        <div className="bg-white border border-ink-200 rounded-xl p-4 mb-6 shadow-card">
          <div className="relative">
            <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
            </svg>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by execution ID, user, or request…"
              className="w-full bg-ink-50/50 border border-ink-200 rounded-lg pl-10 pr-4 py-2.5 text-ink-900 placeholder-ink-400 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100 transition-all"
            />
          </div>
        </div>

        {/* ==================== Error ==================== */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 mb-6 text-sm font-medium">
            {error}
          </div>
        )}

        {/* ==================== Loading ==================== */}
        {loading && executions.length === 0 && (
          <div className="bg-white border border-ink-200 rounded-xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading audit logs…</div>
          </div>
        )}

        {/* ==================== Empty ==================== */}
        {!loading && filtered.length === 0 && (
          <div className="bg-white border-2 border-dashed border-ink-200 rounded-xl p-16 text-center">
            <div className="text-ink-500">
              {search ? 'No executions match your search.' : 'No executions recorded yet.'}
            </div>
          </div>
        )}

        {/* ==================== Table ==================== */}
        {filtered.length > 0 && (
          <div className="bg-white border border-ink-200 rounded-xl overflow-hidden shadow-card">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-ink-50/70 border-b border-ink-200">
                  <tr>
                    <th className="text-left px-4 py-3 text-[11px] font-bold uppercase tracking-widest text-ink-500">ID</th>
                    <th className="text-left px-4 py-3 text-[11px] font-bold uppercase tracking-widest text-ink-500">Time</th>
                    <th className="text-left px-4 py-3 text-[11px] font-bold uppercase tracking-widest text-ink-500">User</th>
                    <th className="text-left px-4 py-3 text-[11px] font-bold uppercase tracking-widest text-ink-500">Request</th>
                    <th className="text-left px-4 py-3 text-[11px] font-bold uppercase tracking-widest text-ink-500">Duration</th>
                    <th className="text-right px-4 py-3 text-[11px] font-bold uppercase tracking-widest text-ink-500">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((row) => (
                    <tr key={row.id} className="border-t border-ink-100 hover:bg-ink-50/40 transition-colors">
                      <td className="px-4 py-3 text-ink-500 font-mono text-xs">#{row.id}</td>
                      <td className="px-4 py-3 text-ink-700 whitespace-nowrap text-xs">{formatDate(row.created_at)}</td>
                      <td className="px-4 py-3 text-ink-700 text-xs">{row.user_email}</td>
                      <td className="px-4 py-3 text-ink-900 font-medium max-w-md truncate">{row.original_request}</td>
                      <td className="px-4 py-3 text-ink-600 font-mono text-xs">{formatDuration(row.duration_ms)}</td>
                      <td className="px-4 py-3 text-right">
                        <span
                          className={`inline-block text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full border ${
                            row.status === 'completed'
                              ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                              : 'bg-amber-50 text-amber-800 border-amber-200'
                          }`}
                        >
                          {row.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="px-4 py-3 border-t border-ink-100 bg-ink-50/40 text-xs text-ink-500">
              Showing {filtered.length} of {stats.total} execution{stats.total === 1 ? '' : 's'}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
