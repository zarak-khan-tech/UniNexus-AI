import { useState, useEffect } from 'react';
import api from '../api/client';
import AgentResult from '../components/AgentResult';

// =============================================================================
// UniNexus AI — Command Center (flagship page)
// Roman Urdu: Ye platform ka main page hai jahan user natural language task deta hai.
// =============================================================================

// =============================================================================
// ExecutionTimeline — visual flow of the plan: Task → Orchestrator → Agents
// Roman Urdu: Ye timeline dikhati hai ke task se lekar result tak kya kya hua.
// =============================================================================
function ExecutionTimeline({ plan, status }) {
  if (!plan || plan.length === 0) return null;

  return (
    <div className="bg-white border border-ink-200 rounded-2xl p-6 shadow-card">
      <div className="flex items-center justify-between mb-5">
        <h2 className="font-display text-lg font-semibold text-ink-900">Execution Flow</h2>
        <span className="text-[11px] uppercase tracking-widest text-ink-400 font-medium">
          {plan.length + 2} stages
        </span>
      </div>

      {/* Horizontal flow: Task → Orchestrator → Agent 1 → ... → Result */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {/* Start: Task */}
        <div className="flex-shrink-0">
          <div className="w-20 h-20 rounded-xl bg-gradient-to-br from-ink-100 to-ink-50 border border-ink-200 flex flex-col items-center justify-center gap-1">
            <svg className="w-5 h-5 text-ink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.6a2 2 0 011.4.6l3.4 3.4a2 2 0 01.6 1.4V19a2 2 0 01-2 2z" />
            </svg>
            <span className="text-[10px] uppercase tracking-wider font-semibold text-ink-600">Task</span>
          </div>
        </div>

        {/* Connector */}
        <div className="flex-shrink-0 w-8 h-0.5 bg-gradient-to-r from-ink-200 to-ink-300 rounded-full" />

        {/* Orchestrator */}
        <div className="flex-shrink-0">
          <div className="w-20 h-20 rounded-xl gradient-gold border border-gold-400 flex flex-col items-center justify-center gap-1 shadow-[0_8px_16px_-6px_rgba(209,158,11,0.5)]">
            <svg className="w-5 h-5 text-ink-950" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3z" />
            </svg>
            <span className="text-[10px] uppercase tracking-wider font-bold text-ink-950">Orchestrator</span>
          </div>
        </div>

        {/* Connector */}
        <div className="flex-shrink-0 w-8 h-0.5 bg-gradient-to-r from-ink-300 to-ink-200 rounded-full" />

        {/* Agents */}
        {plan.map((step, idx) => (
          <div key={step.step} className="flex items-center gap-2 flex-shrink-0">
            <div className="w-20 h-20 rounded-xl bg-white border border-ink-200 flex flex-col items-center justify-center gap-1 shadow-card hover-lift transition-all">
              <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
              <span className="text-[10px] uppercase tracking-wider font-semibold text-ink-700 text-center leading-tight px-1">
                {step.agent.replace('Agent', '')}
              </span>
            </div>
            {idx < plan.length - 1 && (
              <div className="w-8 h-0.5 bg-gradient-to-r from-ink-200 to-ink-300 rounded-full" />
            )}
          </div>
        ))}

        {/* Connector */}
        <div className="flex-shrink-0 w-8 h-0.5 bg-gradient-to-r from-ink-200 to-emerald-300 rounded-full" />

        {/* Result */}
        <div className="flex-shrink-0">
          <div className="w-20 h-20 rounded-xl bg-gradient-to-br from-emerald-100 to-emerald-50 border border-emerald-200 flex flex-col items-center justify-center gap-1">
            <svg className="w-5 h-5 text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span className="text-[10px] uppercase tracking-wider font-bold text-emerald-700">Result</span>
          </div>
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// Main CommandCenter component
// =============================================================================
export default function CommandCenter() {
  const [task, setTask] = useState('Show me students with attendance risk');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showRaw, setShowRaw] = useState({});
  const [llmStatus, setLlmStatus] = useState(null);

  // English: Check whether the local LLM is available on mount.
  // Roman Urdu: Page load hone par check karte hain ke local LLM available hai ya nahi.
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

  // English: Send the task to the orchestrator and receive the execution result.
  // Roman Urdu: Task orchestrator ko bhejte hain aur uska result lete hain.
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
      {/* ==================== Header ==================== */}
      <div className="mb-8 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">
            AI Command Center
          </h1>
          <p className="text-ink-500 max-w-2xl text-[15px] leading-relaxed">
            Issue natural-language tasks. The Orchestrator will plan, delegate, and execute across the agent ecosystem.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs bg-white border border-ink-200 rounded-full px-3.5 py-2 shadow-card">
          <span className={`inline-block w-2 h-2 rounded-full ${llmReady ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}`}></span>
          <span className="text-ink-700 font-medium">
            {llmReady
              ? `LLM: ${llmStatus.default_model}`
              : llmStatus?.available
                ? 'LLM: model not installed'
                : 'LLM: unavailable (keyword router)'}
          </span>
        </div>
      </div>

      {/* ==================== Task input ==================== */}
      <div className="bg-white border border-ink-200 rounded-2xl p-6 mb-6 shadow-card">
        <label className="block text-sm font-medium text-ink-700 mb-2">Natural Language Task</label>
        <textarea
          value={task}
          onChange={(e) => setTask(e.target.value)}
          rows={3}
          className="w-full bg-white border border-ink-200 rounded-lg px-4 py-3 text-ink-900 placeholder-ink-400 focus:outline-none focus:border-ink-500 focus:ring-2 focus:ring-ink-500/10 resize-none shadow-inset-soft transition-all"
        />
        <div className="flex flex-wrap items-center justify-between gap-3 mt-4">
          <div className="text-xs text-ink-500">
            Try: <span className="text-ink-700 font-medium">"attendance risk"</span> or <span className="text-ink-700 font-medium">"exam rules"</span> or <span className="text-ink-700 font-medium">"university policy"</span>
          </div>
          <button
            onClick={handleRun}
            disabled={loading}
            className="group inline-flex items-center gap-2 bg-ink-900 hover:bg-ink-800 disabled:bg-ink-400 text-white font-medium px-6 py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover hover:-translate-y-0.5 disabled:hover:translate-y-0"
          >
            {loading ? (
              <>
                <span className="inline-block w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                Executing...
              </>
            ) : (
              <>
                Run Agents
                <svg className="w-4 h-4 transition-transform group-hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </>
            )}
          </button>
        </div>
      </div>

      {/* ==================== Error ==================== */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 mb-6 text-sm">
          {error}
        </div>
      )}

      {/* ==================== Results ==================== */}
      {result && (
        <div className="space-y-6">
          {/* Workflow Execution summary */}
          <div className="bg-white border border-ink-200 rounded-2xl p-6 shadow-card">
            <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
              <h2 className="font-display text-lg font-semibold text-ink-900">Workflow Execution</h2>
              <div className="flex items-center gap-2 flex-wrap">
                {result.duration_ms != null && (
                  <span className="text-xs px-3 py-1 rounded-full bg-ink-100 text-ink-600 border border-ink-200 font-mono">
                    {result.duration_ms} ms
                  </span>
                )}
                <span className="text-xs px-3 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200 font-medium">
                  {result.planning_source === 'llm' ? 'LLM planned' : 'rule-based'}
                </span>
                <span className="text-xs px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-medium">
                  {result.status}
                </span>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <div className="text-[11px] uppercase tracking-widest text-ink-400 font-medium mb-1">Execution ID</div>
                <div className="text-ink-900 font-mono">#{result.execution_id}</div>
              </div>
              <div>
                <div className="text-[11px] uppercase tracking-widest text-ink-400 font-medium mb-1">Orchestrator</div>
                <div className="text-ink-900">{result.orchestrator}</div>
              </div>
              <div>
                <div className="text-[11px] uppercase tracking-widest text-ink-400 font-medium mb-1">Request</div>
                <div className="text-ink-900 truncate">{result.original_request}</div>
              </div>
            </div>
          </div>

          {/* Visual execution timeline */}
          <ExecutionTimeline plan={result.execution_plan} status={result.status} />

          {/* Plan (textual detail) */}
          <div className="bg-white border border-ink-200 rounded-2xl p-6 shadow-card">
            <h2 className="font-display text-lg font-semibold text-ink-900 mb-4">Execution Plan</h2>
            <div className="space-y-2.5">
              {result.execution_plan.map((step) => (
                <div key={step.step} className="flex items-start gap-4 p-3 rounded-lg hover:bg-ink-50/60 transition-colors">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-ink-900 text-gold-300 flex items-center justify-center text-xs font-bold shadow-card">
                    {step.step}
                  </div>
                  <div className="flex-1 pt-0.5">
                    <div className="text-sm font-semibold text-ink-900">{step.agent}</div>
                    <div className="text-xs text-ink-500 mt-0.5">{step.action}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Agent Results — human-readable cards */}
          <div className="space-y-4">
            <h2 className="font-display text-lg font-semibold text-ink-900">Agent Results</h2>
            {result.execution_results.map((step, idx) => (
              <div key={step.step} className="bg-white border border-ink-200 rounded-2xl overflow-hidden shadow-card">
                <div className="bg-ink-50/60 px-6 py-3.5 border-b border-ink-200 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.6)]"></div>
                    <span className="font-semibold text-ink-900">{step.agent}</span>
                    <span className="text-[10px] uppercase tracking-wider text-ink-400 border border-ink-200 rounded px-1.5 py-0.5">
                      Step {step.step}
                    </span>
                  </div>
                  <button
                    onClick={() => toggleRaw(idx)}
                    className="text-xs text-ink-500 hover:text-ink-900 transition-colors border border-ink-200 hover:border-ink-400 rounded-md px-2.5 py-1 font-medium"
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
            ))}
          </div>
        </div>
      )}

      {/* Empty state */}
      {!result && !loading && !error && (
        <div className="bg-white/60 border border-dashed border-ink-300 rounded-2xl p-16 text-center">
          <div className="w-14 h-14 mx-auto mb-4 rounded-xl bg-ink-100 flex items-center justify-center">
            <svg className="w-7 h-7 text-ink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div className="text-ink-700 font-medium mb-1">No task executed yet</div>
          <div className="text-sm text-ink-500">
            Enter a task above and click "Run Agents" to see the multi-agent workflow in action.
          </div>
        </div>
      )}
    </div>
  );
}
