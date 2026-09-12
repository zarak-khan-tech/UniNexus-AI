import { useEffect, useState } from 'react';
import api from '../api/client';

function formatDuration(ms) {
  if (ms == null) return '—';
  if (ms < 1000) return `${Math.round(ms)} ms`;
  return `${(ms / 1000).toFixed(2)} s`;
}

function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
}

export default function AuditLogs() {
  const [executions, setExecutions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Audit Logs</h1>
          <p className="text-slate-400">
            Complete history of every agent execution for your institution.
          </p>
        </div>
        <button
          onClick={fetchLogs}
          disabled={loading}
          className="text-sm bg-slate-700 hover:bg-slate-600 disabled:bg-slate-800 text-slate-200 px-4 py-2 rounded-lg transition-colors"
        >
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      {error && (
        <div className="bg-red-900/30 border border-red-700 rounded-xl p-4 mb-6 text-red-200">
          {error}
        </div>
      )}

      {loading && !executions.length && (
        <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-16 text-center">
          <div className="text-slate-500">Loading audit logs...</div>
        </div>
      )}

      {!loading && executions.length === 0 && (
        <div className="bg-slate-800/50 border border-dashed border-slate-700 rounded-xl p-16 text-center">
          <div className="text-slate-500 mb-2">No executions recorded yet</div>
          <div className="text-xs text-slate-600">
            Run a task in the AI Command Center to see it appear here.
          </div>
        </div>
      )}

      {executions.length > 0 && (
        <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-900/50">
                <tr>
                  <th className="text-left px-4 py-3 text-xs uppercase tracking-wider text-slate-400 font-medium">ID</th>
                  <th className="text-left px-4 py-3 text-xs uppercase tracking-wider text-slate-400 font-medium">Time</th>
                  <th className="text-left px-4 py-3 text-xs uppercase tracking-wider text-slate-400 font-medium">User</th>
                  <th className="text-left px-4 py-3 text-xs uppercase tracking-wider text-slate-400 font-medium">Request</th>
                  <th className="text-left px-4 py-3 text-xs uppercase tracking-wider text-slate-400 font-medium">Duration</th>
                  <th className="text-left px-4 py-3 text-xs uppercase tracking-wider text-slate-400 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {executions.map((row) => (
                  <tr key={row.id} className="border-t border-slate-700/50 hover:bg-slate-700/20 transition-colors">
                    <td className="px-4 py-3 text-slate-400 font-mono text-xs">#{row.id}</td>
                    <td className="px-4 py-3 text-slate-300 whitespace-nowrap">{formatDate(row.created_at)}</td>
                    <td className="px-4 py-3 text-slate-300">{row.user_email}</td>
                    <td className="px-4 py-3 text-slate-100 max-w-md truncate">{row.original_request}</td>
                    <td className="px-4 py-3 text-slate-300 font-mono text-xs">{formatDuration(row.duration_ms)}</td>
                    <td className="px-4 py-3">
                      <span className={`text-xs px-2 py-1 rounded-full border ${
                        row.status === 'completed'
                          ? 'bg-green-500/15 text-green-300 border-green-500/40'
                          : 'bg-yellow-500/15 text-yellow-300 border-yellow-500/40'
                      }`}>
                        {row.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="px-4 py-3 border-t border-slate-700 bg-slate-900/30 text-xs text-slate-500">
            Showing {executions.length} execution{executions.length === 1 ? '' : 's'}
          </div>
        </div>
      )}
    </div>
  );
}
