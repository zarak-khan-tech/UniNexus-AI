import { useState, useEffect } from 'react';
import api from '../api/client';
import AgentResult from '../components/AgentResult';

// =============================================================================
// Per-agent identity — used in timeline + result cards + plan.
// Roman Urdu: Har agent ka rang aur icon yahan define kiya hai.
// =============================================================================
const AGENT_META = {
  AttendanceAgent: {
    label: 'Attendance',
    color: 'bg-blue-500',
    lightBg: 'bg-blue-50',
    text: 'text-blue-700',
    border: 'border-blue-200',
  },
  PolicyAgent: {
    label: 'Policy',
    color: 'bg-amber-500',
    lightBg: 'bg-amber-50',
    text: 'text-amber-700',
    border: 'border-amber-200',
  },
  RiskAgent: {
    label: 'Risk',
    color: 'bg-red-500',
    lightBg: 'bg-red-50',
    text: 'text-red-700',
    border: 'border-red-200',
  },
  KnowledgeAgent: {
    label: 'Knowledge',
    color: 'bg-violet-500',
    lightBg: 'bg-violet-50',
    text: 'text-violet-700',
    border: 'border-violet-200',
  },
};

// =============================================================================
// ExecutionTimeline — the flagship visual flow
// Roman Urdu: Ye platform ka sabse important visual hai — task se result tak ka safar.
// =============================================================================
function ExecutionTimeline({ plan }) {
  if (!plan || plan.length === 0) return null;

  return (
    <div className="relative bg-gradient-to-br from-ink-950 via-ink-900 to-ink-950 rounded-2xl p-8 shadow-float overflow-hidden">
      {/* Ambient glow */}
      <div className="absolute -top-32 right-0 w-96 h-96 rounded-full bg-gold-500/10 blur-3xl" />
      <div className="absolute -bottom-32 left-0 w-96 h-96 rounded-full bg-blue-500/10 blur-3xl" />
      {/* Subtle grid */}
      <div className="absolute inset-0 ink-grid-pattern opacity-40" />

      <div className="relative z-10">
        <div className="flex items-center justify-between mb-7">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-gold-400 animate-pulse" />
            <h2 className="font-display text-xl font-bold text-white">Execution Flow</h2>
          </div>
          <span className="text-[11px] uppercase tracking-widest text-ink-300 font-bold">
            {plan.length + 2} stages
          </span>
        </div>

        <div className="flex items-center gap-3 overflow-x-auto pb-3">
          {/* Task node */}
          <div className="flex-shrink-0">
            <div className="w-24 h-24 rounded-2xl bg-white/5 backdrop-blur border border-white/10 flex flex-col items-center justify-center gap-2">
              <svg className="w-6 h-6 text-ink-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.6a2 2 0 011.4.6l3.4 3.4a2 2 0 01.6 1.4V19a2 2 0 01-2 2z" />
              </svg>
              <span className="text-[10px] uppercase tracking-widest font-bold text-white">Task</span>
            </div>
          </div>

          <div className="flex-shrink-0 w-10 h-0.5 bg-gradient-to-r from-white/10 to-gold-400/60 rounded-full" />

          {/* Orchestrator — hero node */}
          <div className="flex-shrink-0">
            <div className="relative w-24 h-24 rounded-2xl gradient-gold flex flex-col items-center justify-center gap-2 shadow-[0_16px_40px_-12px_rgba(209,158,11,0.6)]">
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-white/30 to-transparent" />
              <svg className="relative w-6 h-6 text-ink-950" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3z" />
              </svg>
              <span className="relative text-[10px] uppercase tracking-widest font-bold text-ink-950">Orchestrator</span>
            </div>
          </div>

          <div className="flex-shrink-0 w-10 h-0.5 bg-gradient-to-r from-gold-400/60 to-white/10 rounded-full" />

          {/* Agent nodes */}
          {plan.map((step, idx) => {
            const meta = AGENT_META[step.agent] || { label: step.agent, color: 'bg-ink-500' };
            return (
              <div key={step.step} className="flex items-center gap-3 flex-shrink-0">
                <div className="w-24 h-24 rounded-2xl bg-white/5 backdrop-blur border border-white/10 flex flex-col items-center justify-center gap-2 hover:bg-white/10 transition-colors">
                  <div className={`w-2.5 h-2.5 rounded-full ${meta.color} shadow-[0_0_12px_currentColor]`} />
                  <span className="text-[10px] uppercase tracking-widest font-bold text-white text-center px-1 leading-tight">
                    {meta.label}
                  </span>
                </div>
                {idx < plan.length - 1 && (
                  <div className="w-10 h-0.5 bg-white/10 rounded-full" />
                )}
              </div>
            );
          })}

          <div className="flex-shrink-0 w-10 h-0.5 bg-gradient-to-r from-white/10 to-emerald-400/60 rounded-full" />

          {/* Result node */}
          <div className="flex-shrink-0">
            <div className="w-24 h-24 rounded-2xl bg-emerald-500/15 backdrop-blur border border-emerald-400/30 flex flex-col items-center justify-center gap-2">
              <svg className="w-6 h-6 text-emerald-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
              </svg>
              <span className="text-[10px] uppercase tracking-widest font-bold text-emerald-200">Result</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// StatPill — small icon + label + value used in workflow summary bar
// Roman Urdu: Workflow summary bar mein chhote stats ke liye component.
// =============================================================================
function StatPill({ icon, label, value, mono = false }) {
  return (
    <div className="flex items-center gap-3 bg-ink-50/60 border border-ink-100 rounded-xl px-4 py-3">
      <div className="w-8 h-8 rounded-lg bg-white border border-ink-200 flex items-center justify-center text-ink-600 flex-shrink-0">
        {icon}
      </div>
      <div className="min-w-0">
        <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold">{label}</div>
        <div className={`text-sm font-semibold text-ink-900 truncate ${mono ? 'font-mono' : ''}`}>{value}</div>
      </div>
    </div>
  );
}

// =============================================================================
// Main component
// =============================================================================
export default function CommandCenter() {
  const [task, setTask] = useState('Show me students with attendance risk');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showRaw, setShowRaw] = useState({});
  const [llmStatus, setLlmStatus] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await api.get('/agents/llm/status');
        setLlmStatus(response.data);
      } catch (err) {
        setLlmStatus({ available: false, reason: 'Could not reach backend' });
      }
    };
    fetchStatus();
  }, []);

  const handleRun = async () => {
    if (!task.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    setShowRaw({});
    try {
      const response = await api.post('/agents/run', { request: task });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to run agents.');
    } finally {
      setLoading(false);
    }
  };

  const toggleRaw = (idx) => {
    setShowRaw((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  const llmReady = llmStatus?.available && llmStatus?.model_ready;

  return (
    <div className="p-8 max-w-6xl mx-auto animate-fade-in">
      {/* ==================== Hero Header ==================== */}
      <div className="relative bg-gradient-to-br from-white via-white to-ink-50/50 border border-ink-200 rounded-2xl p-8 mb-6 shadow-card overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 rounded-full bg-gold-100/40 blur-3xl" />
        <div className="relative z-10 flex flex-wrap items-start justify-between gap-4">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 text-[11px] text-gold-700 font-bold uppercase tracking-widest mb-3">
              <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
              Orchestration Engine
            </div>
            <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">
              AI Command Center
            </h1>
            <p className="text-ink-500 text-[15px] leading-relaxed">
              Issue natural-language tasks. The Orchestrator plans, delegates, and executes across your agent ecosystem.
            </p>
          </div>
          <div className={`inline-flex items-center gap-2 text-xs border-2 rounded-full px-4 py-2 font-bold shadow-card ${
            llmReady ? 'bg-emerald-50 border-emerald-200 text-emerald-800' : 'bg-amber-50 border-amber-200 text-amber-800'
          }`}>
            <span className={`inline-block w-2 h-2 rounded-full ${llmReady ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}`}></span>
            {llmReady
              ? `LLM Online · ${llmStatus.default_model}`
              : llmStatus?.available
                ? 'LLM: model not installed'
                : 'Fallback mode'}
          </div>
        </div>
      </div>

      {/* ==================== Task Input ==================== */}
      <div className="bg-white border border-ink-200 rounded-2xl p-6 mb-6 shadow-card">
        <div className="flex items-center gap-2 mb-3">
          <div className="w-7 h-7 rounded-lg bg-ink-900 flex items-center justify-center">
            <svg className="w-3.5 h-3.5 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <label className="text-sm font-bold text-ink-900 uppercase tracking-wider">Natural Language Task</label>
        </div>
        <textarea
          value={task}
          onChange={(e) => setTask(e.target.value)}
          rows={3}
          className="w-full bg-ink-50/50 border border-ink-200 rounded-xl px-4 py-3.5 text-ink-900 placeholder-ink-400 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100 resize-none transition-all text-[15px]"
        />
        <div className="flex flex-wrap items-center justify-between gap-3 mt-4">
          <div className="text-xs text-ink-500">
            Try:&nbsp;
            <button onClick={() => setTask('Show me students with attendance risk')} className="text-ink-700 font-semibold hover:text-gold-700 underline decoration-dotted underline-offset-2">attendance risk</button>
            &nbsp;·&nbsp;
            <button onClick={() => setTask('What is the exam policy?')} className="text-ink-700 font-semibold hover:text-gold-700 underline decoration-dotted underline-offset-2">exam rules</button>
            &nbsp;·&nbsp;
            <button onClick={() => setTask('Tell me the attendance rules')} className="text-ink-700 font-semibold hover:text-gold-700 underline decoration-dotted underline-offset-2">university policy</button>
          </div>
          <button
            onClick={handleRun}
            disabled={loading}
            className="group inline-flex items-center gap-2 gradient-gold text-ink-950 font-bold px-7 py-3 rounded-xl transition-all shadow-[0_8px_20px_-6px_rgba(209,158,11,0.5)] hover:shadow-[0_12px_28px_-6px_rgba(209,158,11,0.7)] hover:-translate-y-0.5 disabled:opacity-60 disabled:hover:translate-y-0"
          >
            {loading ? (
              <>
                <span className="inline-block w-4 h-4 border-2 border-ink-950/30 border-t-ink-950 rounded-full animate-spin"></span>
                Executing...
              </>
            ) : (
              <>
                Run Agents
                <svg className="w-4 h-4 transition-transform group-hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </>
            )}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 mb-6 text-sm font-medium">
          {error}
        </div>
      )}

      {/* ==================== Results ==================== */}
      {result && (
        <div className="space-y-6">
          {/* Workflow summary — status + stats bar */}
          <div className="bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden">
            <div className="px-6 py-4 border-b border-ink-100 bg-gradient-to-r from-ink-50/60 to-white flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-emerald-100 flex items-center justify-center">
                  <svg className="w-4 h-4 text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <h2 className="font-display text-lg font-bold text-ink-900">Workflow Execution</h2>
              </div>
              <div className="flex items-center gap-2 flex-wrap">
                {result.duration_ms != null && (
                  <span className="text-xs px-3 py-1.5 rounded-full bg-ink-900 text-gold-300 border border-ink-900 font-mono font-bold">
                    {result.duration_ms} ms
                  </span>
                )}
                <span className={`text-xs px-3 py-1.5 rounded-full font-bold border-2 ${
                  result.planning_source === 'llm'
                    ? 'bg-violet-50 text-violet-700 border-violet-200'
                    : 'bg-blue-50 text-blue-700 border-blue-200'
                }`}>
                  {result.planning_source === 'llm' ? 'LLM planned' : 'rule-based'}
                </span>
                <span className="text-xs px-3 py-1.5 rounded-full bg-emerald-500 text-white font-bold">
                  {result.status}
                </span>
              </div>
            </div>

            <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-3">
              <StatPill
                label="Execution ID"
                value={`#${result.execution_id}`}
                mono
                icon={<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" /></svg>}
              />
              <StatPill
                label="Orchestrator"
                value={result.orchestrator}
                icon={<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3z" /></svg>}
              />
              <StatPill
                label="Request"
                value={result.original_request}
                icon={<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M21 12c0 4.418-4.03 8-9 8a9.86 9.86 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>}
              />
            </div>
          </div>

          {/* Execution flow timeline — the flagship visual */}
          <ExecutionTimeline plan={result.execution_plan} />

          {/* Execution Plan — cards with agent color identity */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 rounded-lg bg-ink-900 flex items-center justify-center">
                <svg className="w-4 h-4 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <h2 className="font-display text-xl font-bold text-ink-900">Execution Plan</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {result.execution_plan.map((step) => {
                const meta = AGENT_META[step.agent] || { label: step.agent, lightBg: 'bg-ink-50', text: 'text-ink-700', border: 'border-ink-200' };
                return (
                  <div
                    key={step.step}
                    className={`relative bg-white border-2 ${meta.border} rounded-xl p-5 shadow-card hover-lift transition-all overflow-hidden`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <span className={`inline-flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full ${meta.lightBg} ${meta.text}`}>
                        Step {step.step}
                      </span>
                      <div className={`w-2 h-2 rounded-full ${meta.color || 'bg-ink-500'}`}></div>
                    </div>
                    <div className="font-bold text-ink-900 text-base mb-1">{step.agent}</div>
                    <div className="text-xs text-ink-500 leading-relaxed">{step.action}</div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Agent Results — colored identity cards */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 rounded-lg bg-ink-900 flex items-center justify-center">
                <svg className="w-4 h-4 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h2 className="font-display text-xl font-bold text-ink-900">Agent Results</h2>
            </div>

            <div className="space-y-4">
              {result.execution_results.map((step, idx) => {
                const meta = AGENT_META[step.agent] || { label: step.agent, color: 'bg-ink-500', lightBg: 'bg-ink-50', text: 'text-ink-700' };
                return (
                  <div key={step.step} className="bg-white border border-ink-200 rounded-2xl overflow-hidden shadow-card hover:shadow-card-hover transition-shadow">
                    <div className={`relative px-6 py-3.5 border-b border-ink-100 flex items-center justify-between ${meta.lightBg}`}>
                      <div className={`absolute top-0 left-0 right-0 h-1 ${meta.color}`} />
                      <div className="flex items-center gap-3">
                        <div className={`w-2.5 h-2.5 rounded-full ${meta.color}`}></div>
                        <span className="font-bold text-ink-900">{step.agent}</span>
                        <span className={`text-[10px] uppercase tracking-widest font-bold px-2 py-0.5 rounded-full bg-white ${meta.text} border border-white/80`}>
                          Step {step.step}
                        </span>
                      </div>
                      <button
                        onClick={() => toggleRaw(idx)}
                        className="text-xs text-ink-600 hover:text-ink-900 transition-colors bg-white border border-ink-200 hover:border-ink-400 rounded-lg px-3 py-1.5 font-semibold"
                      >
                        {showRaw[idx] ? 'Hide raw' : 'View raw'}
                      </button>
                    </div>
                    <div className="p-6">
                      {showRaw[idx] ? (
                        <pre className="text-xs text-ink-100 bg-ink-950 p-4 rounded-lg overflow-auto max-h-96">
                          {JSON.stringify(step.result, null, 2)}
                        </pre>
                      ) : (
                        <AgentResult agentName={step.agent} result={step.result} />
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Empty state */}
      {!result && !loading && !error && (
        <div className="relative bg-gradient-to-br from-white to-ink-50/50 border-2 border-dashed border-ink-200 rounded-2xl p-16 text-center overflow-hidden">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 rounded-full bg-gold-100/30 blur-3xl" />
          <div className="relative">
            <div className="w-16 h-16 mx-auto mb-5 rounded-2xl bg-gradient-to-br from-ink-900 to-ink-700 flex items-center justify-center shadow-float">
              <svg className="w-8 h-8 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div className="font-display text-xl font-bold text-ink-900 mb-2">Ready when you are</div>
            <div className="text-sm text-ink-500 max-w-md mx-auto">
              Enter a task above and click <span className="font-semibold text-ink-700">Run Agents</span> to see the multi-agent workflow in action.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
