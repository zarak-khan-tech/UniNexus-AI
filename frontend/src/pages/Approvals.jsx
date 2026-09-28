import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

// English: Format ISO timestamp to a short readable form.
// Roman Urdu: ISO timestamp ko short readable form mein convert karo.
function formatDate(iso) {
  if (!iso) return '—';
  const d = new Date(iso);
  return d.toLocaleString('en-US', {
    month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

const STATUS_META = {
  pending:  { bg: 'bg-amber-50',   text: 'text-amber-800',  border: 'border-amber-200', dot: 'bg-amber-500' },
  executed: { bg: 'bg-emerald-50', text: 'text-emerald-700',border: 'border-emerald-200', dot: 'bg-emerald-500' },
  rejected: { bg: 'bg-slate-100',  text: 'text-slate-700',  border: 'border-slate-200', dot: 'bg-slate-500' },
  failed:   { bg: 'bg-red-50',     text: 'text-red-700',    border: 'border-red-200',   dot: 'bg-red-500' },
};

function statusStyle(s) {
  return STATUS_META[s] || STATUS_META.pending;
}

export default function Approvals() {
  const [approvals, setApprovals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('pending'); // pending | all
  const [busy, setBusy] = useState({}); // id -> true while approving/rejecting

  const fetchApprovals = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get(`/approvals?status=${filter === 'all' ? 'all' : filter}`);
      setApprovals(response.data.approvals || []);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load approvals.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchApprovals(); }, [filter]);

  const handleApprove = async (id) => {
    setBusy((b) => ({ ...b, [id]: true }));
    try {
      await api.post(`/approvals/${id}/approve`);
      await fetchApprovals();
    } catch (err) {
      setError(err.response?.data?.detail || 'Approval failed.');
    } finally {
      setBusy((b) => ({ ...b, [id]: false }));
    }
  };

  const handleReject = async (id) => {
    setBusy((b) => ({ ...b, [id]: true }));
    try {
      await api.post(`/approvals/${id}/reject`);
      await fetchApprovals();
    } catch (err) {
      setError(err.response?.data?.detail || 'Rejection failed.');
    } finally {
      setBusy((b) => ({ ...b, [id]: false }));
    }
  };

  const pendingCount = approvals.filter((a) => a.status === 'pending').length;

  return (
    <Layout>
      <div className="p-8 max-w-6xl mx-auto animate-fade-in">
        {/* Header */}
        <div className="mb-8 flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 text-[11px] text-gold-700 font-bold uppercase tracking-widest mb-3">
              <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
              Human-in-the-Loop
            </div>
            <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">Approvals</h1>
            <p className="text-ink-500 text-[15px] leading-relaxed max-w-2xl">
              High-risk actions (grade changes, record updates) queued by the reasoning core.
              Review each one and approve or reject before execution.
            </p>
          </div>
          <button
            onClick={fetchApprovals}
            disabled={loading}
            className="inline-flex items-center gap-2 text-sm bg-ink-900 hover:bg-ink-800 disabled:bg-ink-400 text-white font-semibold px-4 py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover hover:-translate-y-0.5 disabled:hover:translate-y-0"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {loading ? 'Refreshing…' : 'Refresh'}
          </button>
        </div>

        {/* Filter tabs */}
        <div className="inline-flex items-center gap-1 p-1 bg-ink-100 border border-ink-200 rounded-xl mb-6 shadow-inset-soft">
          {[
            { id: 'pending', label: 'Pending' },
            { id: 'all', label: 'All' },
          ].map((t) => (
            <button
              key={t.id}
              onClick={() => setFilter(t.id)}
              className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
                filter === t.id
                  ? 'bg-ink-900 text-white shadow-card'
                  : 'text-ink-600 hover:text-ink-900 hover:bg-white'
              }`}
            >
              {t.label}
              {t.id === 'pending' && pendingCount > 0 && (
                <span className="ml-2 inline-flex items-center justify-center min-w-[18px] h-[18px] text-[10px] font-bold rounded-full bg-amber-500 text-white px-1.5">
                  {pendingCount}
                </span>
              )}
            </button>
          ))}
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 mb-6 text-sm font-medium">
            {error}
          </div>
        )}

        {loading && approvals.length === 0 && (
          <div className="bg-white border border-ink-200 rounded-xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading approvals…</div>
          </div>
        )}

        {!loading && approvals.length === 0 && (
          <div className="relative bg-white border-2 border-dashed border-ink-200 rounded-2xl p-16 text-center overflow-hidden">
            <div className="relative">
              <div className="w-16 h-16 mx-auto mb-5 rounded-2xl bg-emerald-100 flex items-center justify-center">
                <svg className="w-8 h-8 text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div className="font-display text-xl font-bold text-ink-900 mb-2">
                {filter === 'pending' ? 'No pending approvals' : 'No approvals yet'}
              </div>
              <div className="text-sm text-ink-500 max-w-md mx-auto">
                {filter === 'pending'
                  ? 'All caught up. When the reasoning core queues a high-risk action, it will appear here.'
                  : 'Try a high-risk action in the Command Center (e.g. "Change Ali Khan\'s MATH101 grade to A+").'}
              </div>
            </div>
          </div>
        )}

        {approvals.length > 0 && (
          <div className="space-y-4">
            {approvals.map((a) => {
              const style = statusStyle(a.status);
              const isPending = a.status === 'pending';
              const isBusy = !!busy[a.id];
              return (
                <div key={a.id} className="relative bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden">
                  <div className={`absolute top-0 left-0 right-0 h-1 ${style.dot}`} />
                  {/* Header row */}
                  <div className={`px-6 py-4 border-b border-ink-100 ${style.bg} flex flex-wrap items-center justify-between gap-3`}>
                    <div className="flex items-center gap-3">
                      <div className={`w-2.5 h-2.5 rounded-full ${style.dot}`} />
                      <code className="text-sm font-mono font-bold text-ink-900 bg-white border border-ink-200 rounded-md px-2.5 py-1">
                        {a.tool_name}
                      </code>
                      <span className={`inline-flex items-center gap-1.5 text-[10px] uppercase tracking-widest font-bold px-2.5 py-1 rounded-full border ${style.bg} ${style.text} ${style.border}`}>
                        {a.status}
                      </span>
                    </div>
                    <div className="flex items-center gap-4 text-xs text-ink-500">
                      <span className="font-mono">#{a.id}</span>
                      <span>{formatDate(a.created_at)}</span>
                    </div>
                  </div>

                  {/* Body */}
                  <div className="p-6 space-y-4">
                    {/* Requester */}
                    <div className="flex items-center gap-2 text-xs text-ink-500">
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      Requested by <span className="text-ink-800 font-medium">{a.user_email}</span>
                    </div>

                    {/* Reasoning */}
                    {a.reasoning && (
                      <div className="bg-ink-50/60 border border-ink-100 rounded-lg px-4 py-3">
                        <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1">Agent reasoning</div>
                        <div className="text-sm text-ink-700 italic">&ldquo;{a.reasoning}&rdquo;</div>
                      </div>
                    )}

                    {/* Arguments */}
                    <div>
                      <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-2">Arguments</div>
                      <pre className="text-xs text-ink-800 bg-ink-50/60 border border-ink-100 p-3 rounded-lg overflow-auto">
{JSON.stringify(a.args, null, 2)}
                      </pre>
                    </div>

                    {/* Resolved info */}
                    {a.resolved_at && (
                      <div className="flex items-center gap-3 pt-3 border-t border-ink-100 text-xs text-ink-500">
                        <span className="font-mono">Resolved: {formatDate(a.resolved_at)}</span>
                        {a.resolved_by_email && <span>by <span className="text-ink-800 font-medium">{a.resolved_by_email}</span></span>}
                        {a.error && <span className="text-red-600">Error: {a.error}</span>}
                      </div>
                    )}

                    {/* Result (if executed) */}
                    {a.result && (
                      <div>
                        <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-2">Execution result</div>
                        <pre className="text-xs text-emerald-800 bg-emerald-50/60 border border-emerald-100 p-3 rounded-lg overflow-auto">
{JSON.stringify(a.result, null, 2)}
                        </pre>
                      </div>
                    )}

                    {/* Actions */}
                    {isPending && (
                      <div className="flex flex-wrap items-center gap-3 pt-4 border-t border-ink-100">
                        <button
                          onClick={() => handleApprove(a.id)}
                          disabled={isBusy}
                          className="inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 disabled:bg-emerald-300 text-white font-bold px-5 py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover hover:-translate-y-0.5 disabled:hover:translate-y-0 text-sm"
                        >
                          {isBusy ? (
                            <><span className="inline-block w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>Processing…</>
                          ) : (
                            <>
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" /></svg>
                              Approve & Execute
                            </>
                          )}
                        </button>
                        <button
                          onClick={() => handleReject(a.id)}
                          disabled={isBusy}
                          className="inline-flex items-center gap-2 bg-white hover:bg-ink-50 disabled:opacity-50 text-red-700 border border-red-200 hover:border-red-400 font-bold px-5 py-2.5 rounded-lg transition-all text-sm"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" /></svg>
                          Reject
                        </button>
                        <div className="text-xs text-ink-500 italic ml-auto">
                          Approving will immediately execute <span className="font-mono text-ink-700">{a.tool_name}</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </Layout>
  );
}
