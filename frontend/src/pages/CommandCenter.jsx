import { useState, useEffect, useRef } from 'react';
import api from '../api/client';
import AgentResult from '../components/AgentResult';

const AGENT_META = {
  AttendanceAgent: { label: 'Attendance', color: 'bg-blue-500', lightBg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
  PolicyAgent: { label: 'Policy', color: 'bg-amber-500', lightBg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
  RiskAgent: { label: 'Risk', color: 'bg-red-500', lightBg: 'bg-red-50', text: 'text-red-700', border: 'border-red-200' },
  KnowledgeAgent: { label: 'Knowledge', color: 'bg-violet-500', lightBg: 'bg-violet-50', text: 'text-violet-700', border: 'border-violet-200' },
};

// English: localStorage key for persisting reasoning conversation across refresh.
// Roman Urdu: Reasoning conversation ko refresh ke baad bachane ke liye localStorage key.
const STORAGE_KEY = 'uninexus_reasoning_conversation';

function ProviderSwitcher({ llmStatus, onChange }) {
  const [open, setOpen] = useState(false);
  const [switching, setSwitching] = useState(false);
  const ref = useRef(null);
  useEffect(() => {
    const handler = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);
  const ready = llmStatus?.available && llmStatus?.model_ready;
  const providers = llmStatus?.gateway?.providers || [];
  const active = llmStatus?.gateway?.primary_provider || 'unknown';
  const switchTo = async (name) => {
    if (name === active) { setOpen(false); return; }
    setSwitching(true);
    try {
      await api.post('/agents/llm/provider', { provider: name });
      setOpen(false);
      if (onChange) await onChange();
    } catch (err) { console.error(err); }
    finally { setSwitching(false); }
  };
  return (
    <div className="relative" ref={ref}>
      <button onClick={() => setOpen((v) => !v)}
        className={`flex items-center gap-2 text-xs rounded-full px-3.5 py-2 shadow-card border-2 transition-all hover:shadow-card-hover ${ready ? 'bg-emerald-50 border-emerald-200 text-emerald-800' : 'bg-amber-50 border-amber-200 text-amber-800'}`}>
        <span className={`inline-block w-2 h-2 rounded-full ${ready ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}`}></span>
        <span className="font-semibold">{ready ? `LLM: ${llmStatus.default_model}` : 'LLM: offline'}</span>
        <svg className={`w-3.5 h-3.5 transition-transform ${open ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {open && (
        <div className="absolute right-0 mt-2 w-72 bg-white border border-ink-200 rounded-xl shadow-float z-30 overflow-hidden animate-slide-up">
          <div className="px-4 py-2.5 border-b border-ink-100 bg-ink-50/60">
            <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold">Active Provider</div>
            <div className="text-sm font-semibold text-ink-900 mt-0.5 capitalize">{active}</div>
          </div>
          <div className="p-1.5 max-h-80 overflow-y-auto">
            {providers.map((p) => (
              <button key={p.name} onClick={() => switchTo(p.name)} disabled={switching || !p.available}
                className={`w-full text-left px-3 py-2.5 rounded-lg flex items-center justify-between transition-colors ${p.name === active ? 'bg-ink-900 text-white' : p.available ? 'hover:bg-ink-50 text-ink-900' : 'opacity-50 cursor-not-allowed text-ink-500'}`}>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span className={`inline-block w-1.5 h-1.5 rounded-full ${p.available ? (p.name === active ? 'bg-gold-400' : 'bg-emerald-500') : 'bg-red-500'}`}></span>
                    <span className="text-sm font-semibold capitalize">{p.name}</span>
                  </div>
                  <div className={`text-[11px] mt-0.5 truncate ${p.name === active ? 'text-ink-200' : 'text-ink-500'}`}>{p.model || 'unknown'}</div>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function ModeToggle({ mode, onChange }) {
  const modes = [
    { id: 'workflow', label: 'Agent Workflow', sub: 'Plan → Delegate', icon: (<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3z" /></svg>) },
    { id: 'reasoning', label: 'Reasoning Loop', sub: 'Think → Tool-call → Answer', icon: (<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>) },
  ];
  return (
    <div className="inline-flex items-center gap-1 p-1 bg-ink-100 border border-ink-200 rounded-xl shadow-inset-soft">
      {modes.map((m) => (
        <button key={m.id} onClick={() => onChange(m.id)}
          className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-semibold transition-all ${mode === m.id ? 'bg-ink-900 text-white shadow-card' : 'text-ink-600 hover:text-ink-900 hover:bg-white'}`}>
          {m.icon}
          <div className="text-left leading-tight">
            <div>{m.label}</div>
            <div className={`text-[9px] uppercase tracking-wider ${mode === m.id ? 'text-gold-300' : 'text-ink-400'}`}>{m.sub}</div>
          </div>
        </button>
      ))}
    </div>
  );
}

function ExecutionTimeline({ plan }) {
  if (!plan || plan.length === 0) return null;
  return (
    <div className="relative bg-gradient-to-br from-ink-950 via-ink-900 to-ink-950 rounded-2xl p-8 shadow-float overflow-hidden">
      <div className="absolute -top-32 right-0 w-96 h-96 rounded-full bg-gold-500/10 blur-3xl" />
      <div className="absolute -bottom-32 left-0 w-96 h-96 rounded-full bg-blue-500/10 blur-3xl" />
      <div className="absolute inset-0 ink-grid-pattern opacity-40" />
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-7">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-gold-400 animate-pulse" />
            <h2 className="font-display text-xl font-bold text-white">Execution Flow</h2>
          </div>
          <span className="text-[11px] uppercase tracking-widest text-ink-300 font-bold">{plan.length + 2} stages</span>
        </div>
        <div className="flex items-center gap-3 overflow-x-auto pb-3">
          <div className="flex-shrink-0">
            <div className="w-24 h-24 rounded-2xl bg-white/5 backdrop-blur border border-white/10 flex flex-col items-center justify-center gap-2">
              <svg className="w-6 h-6 text-ink-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.6a2 2 0 011.4.6l3.4 3.4a2 2 0 01.6 1.4V19a2 2 0 01-2 2z" /></svg>
              <span className="text-[10px] uppercase tracking-widest font-bold text-white">Task</span>
            </div>
          </div>
          <div className="flex-shrink-0 w-10 h-0.5 bg-gradient-to-r from-white/10 to-gold-400/60 rounded-full" />
          <div className="flex-shrink-0">
            <div className="relative w-24 h-24 rounded-2xl gradient-gold flex flex-col items-center justify-center gap-2 shadow-[0_16px_40px_-12px_rgba(209,158,11,0.6)]">
              <svg className="relative w-6 h-6 text-ink-950" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3z" /></svg>
              <span className="relative text-[10px] uppercase tracking-widest font-bold text-ink-950">Orchestrator</span>
            </div>
          </div>
          <div className="flex-shrink-0 w-10 h-0.5 bg-gradient-to-r from-gold-400/60 to-white/10 rounded-full" />
          {plan.map((step, idx) => {
            const meta = AGENT_META[step.agent] || { label: step.agent, color: 'bg-ink-500' };
            return (
              <div key={step.step} className="flex items-center gap-3 flex-shrink-0">
                <div className="w-24 h-24 rounded-2xl bg-white/5 backdrop-blur border border-white/10 flex flex-col items-center justify-center gap-2 hover:bg-white/10 transition-colors">
                  <div className={`w-2.5 h-2.5 rounded-full ${meta.color}`} />
                  <span className="text-[10px] uppercase tracking-widest font-bold text-white text-center px-1 leading-tight">{meta.label}</span>
                </div>
                {idx < plan.length - 1 && <div className="w-10 h-0.5 bg-white/10 rounded-full" />}
              </div>
            );
          })}
          <div className="flex-shrink-0 w-10 h-0.5 bg-gradient-to-r from-white/10 to-emerald-400/60 rounded-full" />
          <div className="flex-shrink-0">
            <div className="w-24 h-24 rounded-2xl bg-emerald-500/15 backdrop-blur border border-emerald-400/30 flex flex-col items-center justify-center gap-2">
              <svg className="w-6 h-6 text-emerald-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" /></svg>
              <span className="text-[10px] uppercase tracking-widest font-bold text-emerald-200">Result</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ReasoningTrace({ toolCalls, iterations }) {
  if (!toolCalls || toolCalls.length === 0) {
    return (
      <div className="bg-white border border-ink-200 rounded-2xl p-6 shadow-card">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-violet-100 flex items-center justify-center">
            <svg className="w-4 h-4 text-violet-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
          </div>
          <div>
            <div className="text-sm font-semibold text-ink-900">Direct answer — no tools needed</div>
            <div className="text-xs text-ink-500">LLM decided this didn't require any tool calls.</div>
          </div>
        </div>
      </div>
    );
  }
  return (
    <div className="bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden">
      <div className="px-6 py-4 border-b border-ink-100 bg-gradient-to-r from-violet-50/60 to-white">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-violet-100 flex items-center justify-center">
            <svg className="w-4 h-4 text-violet-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>
          </div>
          <div>
            <h2 className="font-display text-lg font-bold text-ink-900">Reasoning Trace</h2>
            <p className="text-xs text-ink-500">{iterations} iteration{iterations === 1 ? '' : 's'} · {toolCalls.length} tool call{toolCalls.length === 1 ? '' : 's'}</p>
          </div>
        </div>
      </div>
      <div className="p-6 space-y-4">
        {toolCalls.map((tc, idx) => (
          <div key={idx} className="flex gap-4">
            <div className="flex flex-col items-center flex-shrink-0">
              <div className="w-8 h-8 rounded-full bg-violet-500 text-white flex items-center justify-center text-xs font-bold shadow-card">{tc.iteration}</div>
              {idx < toolCalls.length - 1 && <div className="flex-1 w-0.5 bg-violet-100 my-2 rounded-full" />}
            </div>
            <div className="flex-1 min-w-0 pb-4">
              <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                <span className="text-xs font-bold text-ink-900">Called</span>
                <code className="text-xs font-mono px-2 py-0.5 rounded bg-violet-50 text-violet-700 border border-violet-200 font-semibold">{tc.tool}</code>
                {tc.summary?.success ? (
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">✓ {tc.summary.count != null ? `${tc.summary.count} results` : 'ok'}</span>
                ) : (
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-red-50 text-red-700 border border-red-200">✗ error</span>
                )}
              </div>
              <div className="text-xs text-ink-500 italic mb-1.5">&ldquo;{tc.reasoning}&rdquo;</div>
              <details className="group">
                <summary className="text-[11px] font-semibold text-ink-500 cursor-pointer hover:text-ink-900 list-none">
                  <span className="group-open:hidden">▸ Show arguments</span>
                  <span className="hidden group-open:inline">▾ Hide arguments</span>
                </summary>
                <pre className="mt-2 text-[11px] text-ink-700 bg-ink-50/60 p-3 rounded-lg border border-ink-100 overflow-auto">{JSON.stringify(tc.args, null, 2)}</pre>
              </details>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function ChatMessage({ turn }) {
  if (turn.role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="max-w-2xl bg-ink-900 text-white rounded-2xl rounded-tr-sm px-5 py-3 shadow-card">
          <div className="text-[10px] uppercase tracking-widest text-gold-300 font-bold mb-1">You</div>
          <div className="text-sm leading-relaxed whitespace-pre-wrap">{turn.content}</div>
        </div>
      </div>
    );
  }
  return (
    <div className="flex justify-start">
      <div className="max-w-3xl w-full">
        <div className="bg-white border border-ink-200 rounded-2xl rounded-tl-sm shadow-card overflow-hidden">
          <div className="px-5 py-3 border-b border-ink-100 bg-gradient-to-r from-violet-50/60 to-white flex items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-lg bg-violet-100 flex items-center justify-center">
                <svg className="w-3.5 h-3.5 text-violet-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>
              </div>
              <span className="text-xs font-bold text-ink-900">Reasoning Loop</span>
            </div>
            <div className="flex items-center gap-2 text-[10px] text-ink-500 font-mono">
              {turn.meta?.model && <span>{turn.meta.model}</span>}
              {turn.meta?.duration_ms != null && <span>· {turn.meta.duration_ms} ms</span>}
              {turn.meta?.iterations != null && <span>· {turn.meta.iterations} iter</span>}
            </div>
          </div>
          <div className="p-5">
            <p className="text-[15px] text-ink-800 leading-relaxed whitespace-pre-wrap">{turn.content}</p>
          </div>
        </div>
        {turn.reasoning && <div className="mt-3"><ReasoningTrace toolCalls={turn.reasoning.tool_calls} iterations={turn.reasoning.iterations} /></div>}
      </div>
    </div>
  );
}

// English: Load conversation from localStorage (survives refresh).
// Roman Urdu: localStorage se conversation load karo (refresh ke baad bachi rahe).
function loadConversation() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (e) {
    return [];
  }
}

// English: Save conversation to localStorage.
// Roman Urdu: Conversation ko localStorage mein save karo.
function saveConversation(conversation) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(conversation));
  } catch (e) {
    console.error('Failed to save conversation', e);
  }
}

export default function CommandCenter() {
  const [mode, setMode] = useState('reasoning');
  const [task, setTask] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [llmStatus, setLlmStatus] = useState(null);

  // English: Initialize from localStorage so the chat survives refresh.
  // Roman Urdu: localStorage se initialize karo taake refresh ke baad chat rahe.
  const [conversation, setConversation] = useState(loadConversation);
  const [workflowResult, setWorkflowResult] = useState(null);
  const [showRaw, setShowRaw] = useState({});

  const scrollRef = useRef(null);

  const loadStatus = async () => {
    try {
      const response = await api.get('/agents/llm/status');
      setLlmStatus(response.data);
    } catch (err) {
      setLlmStatus({ available: false, reason: 'Could not reach backend' });
    }
  };
  useEffect(() => { loadStatus(); }, []);

  // English: Persist conversation to localStorage on every change.
  // Roman Urdu: Har change pe conversation localStorage mein save karo.
  useEffect(() => {
    saveConversation(conversation);
  }, [conversation]);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [conversation, loading]);

  const handleRun = async () => {
    if (!task.trim()) return;
    const userMessage = task.trim();
    setTask('');
    setLoading(true);
    setError(null);

    if (mode === 'reasoning') {
      const history = conversation
        .filter(t => t.role === 'user' || (t.role === 'assistant' && t.content))
        .map(t => ({ role: t.role, content: t.content }));
      setConversation(prev => [...prev, { role: 'user', content: userMessage }]);
      try {
        const response = await api.post('/agents/reason', { request: userMessage, history });
        const r = response.data;
        setConversation(prev => [...prev, {
          role: 'assistant',
          content: r.answer || 'No answer.',
          meta: { model: r.model, duration_ms: r.duration_ms, iterations: r.iterations, provider: r.provider },
          reasoning: { tool_calls: r.tool_calls || [], iterations: r.iterations || 0 },
        }]);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to reason. Try again.');
        setConversation(prev => [...prev, { role: 'assistant', content: '⚠️ Failed to respond. Check your connection and try again.' }]);
      } finally {
        setLoading(false);
      }
    } else {
      setWorkflowResult(null);
      setShowRaw({});
      try {
        const response = await api.post('/agents/run', { request: userMessage });
        setWorkflowResult(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to run agents.');
      } finally {
        setLoading(false);
      }
    }
  };

  const clearConversation = () => {
    setConversation([]);
    localStorage.removeItem(STORAGE_KEY);
    setError(null);
  };

  const toggleRaw = (idx) => setShowRaw((prev) => ({ ...prev, [idx]: !prev[idx] }));
  const isReasoning = mode === 'reasoning';

  return (
    <div className="p-8 max-w-6xl mx-auto animate-fade-in">
      <div className="relative bg-gradient-to-br from-white via-white to-ink-50/50 border border-ink-200 rounded-2xl p-8 mb-6 shadow-card">
        <div className="absolute top-0 right-0 w-64 h-64 rounded-full bg-gold-100/40 blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-wrap items-start justify-between gap-4">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 text-[11px] text-gold-700 font-bold uppercase tracking-widest mb-3">
              <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
              Orchestration Engine
            </div>
            <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">AI Command Center</h1>
            <p className="text-ink-500 text-[15px] leading-relaxed">
              Deterministic agent workflows and real LLM reasoning with persistent conversation memory.
            </p>
          </div>
          <ProviderSwitcher llmStatus={llmStatus} onChange={loadStatus} />
        </div>
      </div>

      <div className="flex flex-wrap items-center justify-center gap-3 mb-6">
        <ModeToggle mode={mode} onChange={(m) => { setMode(m); setError(null); setWorkflowResult(null); }} />
        {isReasoning && conversation.length > 0 && (
          <button onClick={clearConversation}
            className="inline-flex items-center gap-2 text-xs font-semibold text-ink-600 hover:text-ink-900 bg-white border border-ink-200 hover:border-ink-400 rounded-xl px-3.5 py-2.5 shadow-card hover:shadow-card-hover transition-all">
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M1 7h22M9 7V4a2 2 0 012-2h2a2 2 0 012 2v3" /></svg>
            New conversation
          </button>
        )}
      </div>

      <div className="bg-white border border-ink-200 rounded-2xl p-6 mb-6 shadow-card">
        <div className="flex items-center gap-2 mb-3">
          <div className="w-7 h-7 rounded-lg bg-ink-900 flex items-center justify-center">
            <svg className="w-3.5 h-3.5 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
          </div>
          <label className="text-sm font-bold text-ink-900 uppercase tracking-wider">
            {isReasoning ? 'Ask anything (reasoning mode)' : 'Natural Language Task'}
          </label>
          {isReasoning && conversation.length > 0 && (
            <span className="ml-auto text-[10px] uppercase tracking-widest font-bold text-violet-700 bg-violet-50 border border-violet-200 rounded-full px-2 py-0.5">
              {conversation.filter(t => t.role === 'user').length} turns in memory
            </span>
          )}
        </div>
        <textarea
          value={task}
          onChange={(e) => setTask(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) handleRun(); }}
          rows={2}
          placeholder={isReasoning ? "Ask a follow-up — I'll remember the previous turns. (Ctrl+Enter to send)" : "Describe the task..."}
          className="w-full bg-ink-50/50 border border-ink-200 rounded-xl px-4 py-3.5 text-ink-900 placeholder-ink-400 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100 resize-none transition-all text-[15px]"
        />
        <div className="flex flex-wrap items-center justify-between gap-3 mt-4">
          <div className="text-xs text-ink-500">
            Try:&nbsp;
            {['show me students with low attendance', 'which of them might fail?', 'how much does a semester cost?', 'hello, how are you?'].map((s, i, arr) => (
              <span key={s}>
                <button onClick={() => setTask(s)} className="text-ink-700 font-semibold hover:text-gold-700 underline decoration-dotted underline-offset-2">{s}</button>
                {i < arr.length - 1 && ' · '}
              </span>
            ))}
          </div>
          <button onClick={handleRun} disabled={loading}
            className="group inline-flex items-center gap-2 gradient-gold text-ink-950 font-bold px-7 py-3 rounded-xl transition-all shadow-[0_8px_20px_-6px_rgba(209,158,11,0.5)] hover:shadow-[0_12px_28px_-6px_rgba(209,158,11,0.7)] hover:-translate-y-0.5 disabled:opacity-60 disabled:hover:translate-y-0">
            {loading ? (
              <><span className="inline-block w-4 h-4 border-2 border-ink-950/30 border-t-ink-950 rounded-full animate-spin"></span>{isReasoning ? 'Reasoning…' : 'Executing…'}</>
            ) : (
              <>{isReasoning ? 'Send' : 'Run Agents'}<svg className="w-4 h-4 transition-transform group-hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 7l5 5m0 0l-5 5m5-5H6" /></svg></>
            )}
          </button>
        </div>
      </div>

      {error && <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 mb-6 text-sm font-medium">{error}</div>}

      {isReasoning && conversation.length > 0 && (
        <div ref={scrollRef} className="space-y-5">
          {conversation.map((turn, idx) => (
            <ChatMessage key={idx} turn={turn} />
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-white border border-ink-200 rounded-2xl rounded-tl-sm px-5 py-4 shadow-card">
                <div className="flex items-center gap-3">
                  <div className="inline-block w-4 h-4 border-2 border-violet-300 border-t-violet-700 rounded-full animate-spin"></div>
                  <span className="text-sm text-ink-600">Thinking…</span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {!isReasoning && workflowResult && (
        <div className="space-y-6">
          <div className="bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden">
            <div className="px-6 py-4 border-b border-ink-100 bg-gradient-to-r from-ink-50/60 to-white flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-emerald-100 flex items-center justify-center">
                  <svg className="w-4 h-4 text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" /></svg>
                </div>
                <h2 className="font-display text-lg font-bold text-ink-900">Workflow Execution</h2>
              </div>
              <div className="flex items-center gap-2 flex-wrap">
                {workflowResult.duration_ms != null && <span className="text-xs px-3 py-1.5 rounded-full bg-ink-900 text-gold-300 border border-ink-900 font-mono font-bold">{workflowResult.duration_ms} ms</span>}
                <span className={`text-xs px-3 py-1.5 rounded-full font-bold border-2 ${workflowResult.planning_source === 'llm' ? 'bg-violet-50 text-violet-700 border-violet-200' : 'bg-blue-50 text-blue-700 border-blue-200'}`}>
                  {workflowResult.planning_source === 'llm' ? 'LLM planned' : 'rule-based'}
                </span>
                <span className="text-xs px-3 py-1.5 rounded-full bg-emerald-500 text-white font-bold">{workflowResult.status}</span>
              </div>
            </div>
            <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-3">
              <div className="flex items-center gap-3 bg-ink-50/60 border border-ink-100 rounded-xl px-4 py-3">
                <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold">Execution ID</div>
                <div className="text-sm font-semibold text-ink-900 font-mono ml-auto">#{workflowResult.execution_id}</div>
              </div>
              <div className="flex items-center gap-3 bg-ink-50/60 border border-ink-100 rounded-xl px-4 py-3">
                <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold">Orchestrator</div>
                <div className="text-sm font-semibold text-ink-900 ml-auto">{workflowResult.orchestrator}</div>
              </div>
              <div className="flex items-center gap-3 bg-ink-50/60 border border-ink-100 rounded-xl px-4 py-3">
                <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold">Request</div>
                <div className="text-sm font-semibold text-ink-900 truncate ml-auto max-w-[140px]" title={workflowResult.original_request}>{workflowResult.original_request}</div>
              </div>
            </div>
          </div>

          {workflowResult.execution_plan && workflowResult.execution_plan.length > 0 && (
            <>
              <ExecutionTimeline plan={workflowResult.execution_plan} />
              <div className="space-y-4">
                <h2 className="font-display text-xl font-bold text-ink-900">Agent Results</h2>
                {workflowResult.execution_results.map((step, idx) => {
                  const meta = AGENT_META[step.agent] || { color: 'bg-ink-500', lightBg: 'bg-ink-50', text: 'text-ink-700' };
                  return (
                    <div key={step.step} className="bg-white border border-ink-200 rounded-2xl overflow-hidden shadow-card hover:shadow-card-hover transition-shadow">
                      <div className={`relative px-6 py-3.5 border-b border-ink-100 flex items-center justify-between ${meta.lightBg}`}>
                        <div className={`absolute top-0 left-0 right-0 h-1 ${meta.color}`} />
                        <div className="flex items-center gap-3">
                          <div className={`w-2.5 h-2.5 rounded-full ${meta.color}`}></div>
                          <span className="font-bold text-ink-900">{step.agent}</span>
                          <span className={`text-[10px] uppercase tracking-widest font-bold px-2 py-0.5 rounded-full bg-white ${meta.text} border border-white/80`}>Step {step.step}</span>
                        </div>
                        <button onClick={() => toggleRaw(idx)} className="text-xs text-ink-600 hover:text-ink-900 transition-colors bg-white border border-ink-200 hover:border-ink-400 rounded-lg px-3 py-1.5 font-semibold">
                          {showRaw[idx] ? 'Hide raw' : 'View raw'}
                        </button>
                      </div>
                      <div className="p-6">
                        {showRaw[idx] ? (
                          <pre className="text-xs text-ink-100 bg-ink-950 p-4 rounded-lg overflow-auto max-h-96">{JSON.stringify(step.result, null, 2)}</pre>
                        ) : (
                          <AgentResult agentName={step.agent} result={step.result} />
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </>
          )}

          {workflowResult.mode === 'direct_answer' && workflowResult.direct_answer && (
            <div className="bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden">
              <div className="px-6 py-4 border-b border-ink-100 bg-gradient-to-r from-violet-50/60 to-white">
                <h2 className="font-display text-lg font-bold text-ink-900">Direct Answer</h2>
              </div>
              <div className="p-6">
                <p className="text-[15px] text-ink-800 leading-relaxed whitespace-pre-wrap">{workflowResult.direct_answer}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {!loading && !error && (
        (isReasoning && conversation.length === 0) ||
        (!isReasoning && !workflowResult)
      ) && (
        <div className="relative bg-gradient-to-br from-white to-ink-50/50 border-2 border-dashed border-ink-200 rounded-2xl p-16 text-center overflow-hidden">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 rounded-full bg-gold-100/30 blur-3xl" />
          <div className="relative">
            <div className="w-16 h-16 mx-auto mb-5 rounded-2xl bg-gradient-to-br from-ink-900 to-ink-700 flex items-center justify-center shadow-float">
              <svg className="w-8 h-8 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            </div>
            <div className="font-display text-xl font-bold text-ink-900 mb-2">Ready when you are</div>
            <div className="text-sm text-ink-500 max-w-md mx-auto">
              {isReasoning ? 'Start a conversation. Every turn is remembered (even after refresh), so follow-ups work naturally.' : 'Enter a task and click "Run Agents".'}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
