import { useEffect, useState } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import api from '../api/client';

const AGENT_META = {
  AttendanceAgent: { color: 'bg-blue-500', lightBg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
  PolicyAgent: { color: 'bg-amber-500', lightBg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
  RiskAgent: { color: 'bg-red-500', lightBg: 'bg-red-50', text: 'text-red-700', border: 'border-red-200' },
  KnowledgeAgent: { color: 'bg-violet-500', lightBg: 'bg-violet-50', text: 'text-violet-700', border: 'border-violet-200' },
};
function agentStyle(name) {
  return AGENT_META[name] || { color: 'bg-ink-500', lightBg: 'bg-ink-50', text: 'text-ink-700', border: 'border-ink-200' };
}

function formatDate(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  });
}

export default function ExecutionDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get(`/agents/executions/${id}`);
        setData(res.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load execution.');
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  return (
    <Layout>
      <div className="p-8 max-w-5xl mx-auto animate-fade-in">
        {/* Breadcrumb */}
        <div className="mb-6 flex items-center gap-2 text-xs text-ink-500">
          <Link to="/audit" className="hover:text-ink-900 transition-colors">Audit Logs</Link>
          <span>›</span>
          <span className="text-ink-900 font-medium">Execution #{id}</span>
        </div>

        <button
          onClick={() => navigate('/audit')}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-ink-600 hover:text-ink-900 mb-4 transition-colors"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Audit Logs
        </button>

        {loading && (
          <div className="bg-white border border-ink-200 rounded-2xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading execution…</div>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 text-sm font-medium">
            {error}
          </div>
        )}

        {!loading && data && (
          <>
            {/* Header card */}
            <div className="bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden mb-6">
              <div className="px-6 py-4 border-b border-ink-100 bg-gradient-to-r from-ink-50/60 to-white flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-ink-900 text-gold-300 flex items-center justify-center text-xs font-bold">
                    #{data.id}
                  </div>
                  <h1 className="font-display text-xl font-bold text-ink-900">Execution Detail</h1>
                </div>
                <span className="text-xs px-3 py-1.5 rounded-full bg-emerald-500 text-white font-bold">
                  {data.status}
                </span>
              </div>
              <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1">Requested by</div>
                  <div className="text-sm text-ink-900 truncate">{data.user_email}</div>
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1">When</div>
                  <div className="text-sm text-ink-900">{formatDate(data.created_at)}</div>
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1">Duration</div>
                  <div className="text-sm text-ink-900 font-mono">{data.duration_ms} ms</div>
                </div>
              </div>
              <div className="px-6 pb-6">
                <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1">Original Request</div>
                <div className="text-[15px] text-ink-800 leading-relaxed whitespace-pre-wrap bg-ink-50/60 border border-ink-100 rounded-lg p-3">
                  {data.original_request}
                </div>
              </div>
            </div>

            {/* Plan */}
            {Array.isArray(data.execution_plan) && data.execution_plan.length > 0 && (
              <div className="bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden mb-6">
                <div className="px-6 py-4 border-b border-ink-100 bg-ink-50/60">
                  <h2 className="font-display text-lg font-bold text-ink-900">Execution Plan</h2>
                  <p className="text-xs text-ink-500">{data.execution_plan.length} step(s)</p>
                </div>
                <div className="p-6 space-y-3">
                  {data.execution_plan.map((step, idx) => {
                    const meta = agentStyle(step.agent || step.tool || 'unknown');
                    return (
                      <div key={idx} className="flex items-start gap-4">
                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-ink-900 text-gold-300 flex items-center justify-center text-xs font-bold">
                          {step.step || idx + 1}
                        </div>
                        <div className="flex-1 pt-1">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className={`text-xs font-mono font-bold px-2 py-0.5 rounded border ${meta.lightBg} ${meta.text} ${meta.border}`}>
                              {step.agent || step.tool}
                            </span>
                            <span className="text-xs text-ink-500">{step.action || ''}</span>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Raw results */}
            <div className="bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden">
              <div className="px-6 py-4 border-b border-ink-100 bg-ink-50/60">
                <h2 className="font-display text-lg font-bold text-ink-900">Execution Results</h2>
                <p className="text-xs text-ink-500">Raw output (JSON)</p>
              </div>
              <div className="p-6">
                <pre className="text-xs text-ink-100 bg-ink-950 p-4 rounded-lg overflow-auto max-h-[70vh]">
                  {JSON.stringify(data.execution_results, null, 2)}
                </pre>
              </div>
            </div>
          </>
        )}
      </div>
    </Layout>
  );
}
