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

function formatDuration(ms) {
  if (ms == null) return '—';
  if (ms < 1000) return Math.round(ms) + ' ms';
  return (ms / 1000).toFixed(2) + ' s';
}

// =============================================================================
// Reasoning execution renderer (answer + sources + tool trace)
// =============================================================================
function ReasoningResults({ answer, plan }) {
  return (
    <div className="space-y-6">
      {/* Answer card */}
      <div className="bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden">
        <div className="px-6 py-4 border-b border-ink-100 bg-gradient-to-r from-violet-50/60 to-white flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-violet-100 flex items-center justify-center">
            <svg className="w-4 h-4 text-violet-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <h2 className="font-display text-lg font-bold text-ink-900">Answer</h2>
        </div>
        <div className="p-6">
          <p className="text-[15px] text-ink-800 leading-relaxed whitespace-pre-wrap">{answer}</p>
        </div>
      </div>

      {/* Tool trace */}
      {Array.isArray(plan) && plan.length > 0 && (
        <div className="bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden">
          <div className="px-6 py-4 border-b border-ink-100 bg-ink-50/60">
            <h2 className="font-display text-lg font-bold text-ink-900">Tool Trace</h2>
            <p className="text-xs text-ink-500">{plan.length} tool call(s)</p>
          </div>
          <div className="p-6 space-y-3">
            {plan.map((tc, idx) => (
              <div key={idx} className="flex items-start gap-4">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-violet-500 text-white flex items-center justify-center text-xs font-bold">
                  {tc.iteration || idx + 1}
                </div>
                <div className="flex-1 pt-1">
                  <div className="flex items-center gap-2 flex-wrap mb-1">
                    <span className="text-xs font-bold text-ink-900">Called</span>
                    <code className="text-xs font-mono px-2 py-0.5 rounded bg-violet-50 text-violet-700 border border-violet-200 font-semibold">
                      {tc.tool}
                    </code>
                    {tc.summary?.success && (
                      <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                        ✓ {tc.summary.count != null ? `${tc.summary.count} results` : 'ok'}
                      </span>
                    )}
                  </div>
                  {tc.reasoning && <div className="text-xs text-ink-500 italic">{tc.reasoning}</div>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// =============================================================================
// Workflow execution renderer (agent results array)
// =============================================================================
function WorkflowResults({ results }) {
  return (
    <div className="space-y-4">
      <h2 className="font-display text-lg font-bold text-ink-900">Agent Results</h2>
      {results.map((step, idx) => {
        const meta = agentStyle(step.agent);
        const result = step.result || {};
        return (
          <div key={idx} className="bg-white border border-ink-200 rounded-2xl overflow-hidden shadow-card">
            <div className={`relative px-6 py-3.5 border-b border-ink-100 flex items-center justify-between ${meta.lightBg}`}>
              <div className={`absolute top-0 left-0 right-0 h-1 ${meta.color}`} />
              <div className="flex items-center gap-3">
                <div className={`w-2.5 h-2.5 rounded-full ${meta.color}`} />
                <span className="font-bold text-ink-900">{step.agent}</span>
                {step.action && <span className="text-xs text-ink-500">— {step.action}</span>}
              </div>
              <span className="text-[10px] uppercase tracking-wider text-ink-500 font-bold">Step {step.step}</span>
            </div>
            <div className="p-6">
              {step.error ? (
                <div className="text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg p-3">
                  {step.error}
                </div>
              ) : (
                <div className="text-sm text-ink-700 space-y-2">
                  {result.total_flagged != null && (
                    <div>Flagged <span className="font-bold text-ink-900">{result.total_flagged}</span> student(s) below <span className="font-mono">{result.threshold}%</span>.</div>
                  )}
                  {result.thresholds && (
                    <div>Risk thresholds — High: <span className="font-mono">{result.thresholds.high}%</span>, Medium: <span className="font-mono">{result.thresholds.medium}%</span>.</div>
                  )}
                  {result.at_risk_students && (
                    <div>Identified <span className="font-bold text-ink-900">{result.at_risk_students.length}</span> at-risk enrollment(s).</div>
                  )}
                  {result.policy_threshold != null && (
                    <div>Policy threshold: <span className="font-bold">{result.policy_threshold}%</span> — {result.rule}</div>
                  )}
                  {result.total_matches != null && (
                    <div>Retrieved <span className="font-bold text-ink-900">{result.total_matches}</span> document(s) from the knowledge base.</div>
                  )}
                  {result.data && Array.isArray(result.data) && (
                    <div className="text-xs text-ink-500">+ {result.data.length} row(s) of detail</div>
                  )}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

// =============================================================================
// Main
// =============================================================================
export default function ExecutionDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showRaw, setShowRaw] = useState(false);

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

  // Figure out execution shape
  const isReasoning = data && data.execution_results && typeof data.execution_results === 'object' && !Array.isArray(data.execution_results) && 'answer' in data.execution_results;
  const isWorkflow = data && Array.isArray(data.execution_results);

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
            {/* Header */}
            <div className="bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden mb-6">
              <div className="px-6 py-4 border-b border-ink-100 bg-gradient-to-r from-ink-50/60 to-white flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-ink-900 text-gold-300 flex items-center justify-center text-xs font-bold">
                    #{data.id}
                  </div>
                  <h1 className="font-display text-xl font-bold text-ink-900">Execution Detail</h1>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`text-xs px-3 py-1.5 rounded-full font-bold ${isReasoning ? 'bg-violet-100 text-violet-700 border border-violet-200' : 'bg-blue-100 text-blue-700 border border-blue-200'}`}>
                    {isReasoning ? 'Reasoning Loop' : 'Agent Workflow'}
                  </span>
                  <span className="text-xs px-3 py-1.5 rounded-full bg-emerald-500 text-white font-bold">
                    {data.status}
                  </span>
                </div>
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
                  <div className="text-sm text-ink-900 font-mono">{formatDuration(data.duration_ms)}</div>
                </div>
              </div>
              <div className="px-6 pb-6">
                <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1">Original Request</div>
                <div className="text-[15px] text-ink-800 leading-relaxed whitespace-pre-wrap bg-ink-50/60 border border-ink-100 rounded-lg p-3">
                  {data.original_request}
                </div>
              </div>
            </div>

            {/* Human-friendly results */}
            {isReasoning && (
              <ReasoningResults
                answer={data.execution_results.answer || 'No answer recorded.'}
                plan={Array.isArray(data.execution_plan) ? data.execution_plan : []}
              />
            )}

            {isWorkflow && data.execution_results.length > 0 && (
              <WorkflowResults results={data.execution_results} />
            )}

            {/* Raw JSON — hidden by default */}
            <div className="mt-6 flex items-center justify-end">
              <button
                onClick={() => setShowRaw((v) => !v)}
                className="text-xs font-semibold text-ink-500 hover:text-ink-900 transition-colors inline-flex items-center gap-1.5"
              >
                <svg className={`w-3.5 h-3.5 transition-transform ${showRaw ? 'rotate-90' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M9 5l7 7-7 7" />
                </svg>
                {showRaw ? 'Hide' : 'Show'} raw JSON
              </button>
            </div>

            {showRaw && (
              <div className="mt-3 bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden">
                <div className="px-6 py-3 border-b border-ink-100 bg-ink-50/60">
                  <h2 className="text-xs uppercase tracking-widest text-ink-500 font-bold">Technical details</h2>
                </div>
                <div className="p-6">
                  <pre className="text-xs text-ink-100 bg-ink-950 p-4 rounded-lg overflow-auto max-h-[70vh]">
                    {JSON.stringify({ plan: data.execution_plan, results: data.execution_results }, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </Layout>
  );
}
