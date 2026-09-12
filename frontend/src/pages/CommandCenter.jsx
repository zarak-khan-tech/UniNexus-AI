import { useState } from 'react';
import api from '../api/client';
import AgentResult from '../components/AgentResult';

export default function CommandCenter() {
  const [task, setTask] = useState('Show me students with attendance risk');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showRaw, setShowRaw] = useState({});

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
      setError(err.response?.data?.detail || 'Failed to run agents. Check your connection.');
    } finally {
      setLoading(false);
    }
  };

  const toggleRaw = (idx) => {
    setShowRaw((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-white mb-2">AI Command Center</h1>
        <p className="text-slate-400">
          Issue natural-language tasks. The Orchestrator will plan, delegate, and execute across the agent ecosystem.
        </p>
      </div>

      {/* Task Input */}
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 mb-6">
        <label className="block text-sm font-medium text-slate-300 mb-2">Natural Language Task</label>
        <textarea
          value={task}
          onChange={(e) => setTask(e.target.value)}
          rows={3}
          className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500 resize-none"
          placeholder="e.g., Show me students with attendance risk"
        />
        <div className="flex items-center justify-between mt-4">
          <div className="text-xs text-slate-500">
            Try: "attendance risk" or "exam rules" or "university policy"
          </div>
          <button
            onClick={handleRun}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 text-white font-medium px-6 py-2 rounded-lg transition-colors flex items-center gap-2"
          >
            {loading ? (
              <>
                <span className="inline-block w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                Executing...
              </>
            ) : (
              'Run Agents'
            )}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-900/30 border border-red-700 rounded-xl p-4 mb-6 text-red-200">
          {error}
        </div>
      )}

      {result && (
        <div className="space-y-6">
          {/* Workflow Status */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-white">Workflow Execution</h2>
              <span className="text-xs px-3 py-1 rounded-full bg-green-500/20 text-green-300 border border-green-500/30">
                {result.status}
              </span>
            </div>
            <div className="text-sm text-slate-400 mb-1">
              <span className="text-slate-500">Orchestrator:</span> <span className="text-slate-200">{result.orchestrator}</span>
            </div>
            <div className="text-sm text-slate-400">
              <span className="text-slate-500">Request:</span> <span className="text-slate-200">{result.original_request}</span>
            </div>
          </div>

          {/* Execution Plan */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Execution Plan</h2>
            <div className="space-y-3">
              {result.execution_plan.map((step) => (
                <div key={step.step} className="flex items-start gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600/20 border border-blue-500/40 flex items-center justify-center text-blue-300 text-sm font-semibold">
                    {step.step}
                  </div>
                  <div className="flex-1 pt-1">
                    <div className="text-sm font-medium text-white">{step.agent}</div>
                    <div className="text-xs text-slate-400">{step.action}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Agent Results - Human Friendly */}
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-white">Agent Results</h2>
            {result.execution_results.map((step, idx) => (
              <div key={step.step} className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
                <div className="bg-slate-900/50 px-6 py-3 border-b border-slate-700 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-green-400"></div>
                    <span className="font-medium text-white">{step.agent}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-xs text-slate-500">Step {step.step}</span>
                    <button
                      onClick={() => toggleRaw(idx)}
                      className="text-xs text-slate-400 hover:text-slate-200 transition-colors border border-slate-700 hover:border-slate-500 rounded px-2 py-0.5"
                    >
                      {showRaw[idx] ? 'Hide' : 'View'} Raw
                    </button>
                  </div>
                </div>
                <div className="p-6">
                  {showRaw[idx] ? (
                    <pre className="text-xs text-slate-300 bg-slate-950 p-4 rounded-lg overflow-auto max-h-96">
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

      {!result && !loading && !error && (
        <div className="bg-slate-800/50 border border-dashed border-slate-700 rounded-xl p-16 text-center">
          <div className="text-slate-500 mb-2">No task executed yet</div>
          <div className="text-xs text-slate-600">
            Enter a task above and click "Run Agents" to see the multi-agent workflow in action
          </div>
        </div>
      )}
    </div>
  );
}
