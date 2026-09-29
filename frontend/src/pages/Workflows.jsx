import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

function formatDate(iso) {
  if (!iso) return '—';
  const d = new Date(iso);
  return d.toLocaleString('en-US', {
    month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

const TRIGGER_META = {
  attendance_below: { label: 'Low attendance', accent: 'blue',
    desc: 'Fires when students drop below an attendance threshold' },
  execution_completed: { label: 'Execution completed', accent: 'violet',
    desc: 'Fires after an agent execution finishes' },
};

const ACTION_META = {
  send_notification: { label: 'Send notification', accent: 'amber' },
  log_only: { label: 'Log only', accent: 'slate' },
};

const ACCENT = {
  blue: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200', bar: 'bg-blue-500' },
  violet: { bg: 'bg-violet-50', text: 'text-violet-700', border: 'border-violet-200', bar: 'bg-violet-500' },
  amber: { bg: 'bg-amber-50', text: 'text-amber-800', border: 'border-amber-200', bar: 'bg-amber-500' },
  slate: { bg: 'bg-ink-50', text: 'text-ink-700', border: 'border-ink-200', bar: 'bg-ink-500' },
};

function CreateForm({ onCreate, onCancel }) {
  const [name, setName] = useState('Low attendance alert');
  const [threshold, setThreshold] = useState(60);
  const [title, setTitle] = useState('Low attendance detected');
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      await api.post('/workflows', {
        name,
        description: `Alert if any student drops below ${threshold}% average attendance`,
        trigger_type: 'attendance_below',
        trigger_config: { threshold: Number(threshold) },
        action_type: 'send_notification',
        action_config: {
          title,
          body: 'Workflow "{name}" triggered: {summary}',
          action_url: '/students',
        },
      });
      await onCreate();
    } catch (err) {
      console.error(err);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="bg-white border-2 border-ink-900 rounded-2xl p-6 shadow-float mb-6 animate-slide-up">
      <div className="flex items-center gap-3 mb-5">
        <div className="w-8 h-8 rounded-lg bg-ink-900 flex items-center justify-center">
          <svg className="w-4 h-4 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        </div>
        <h2 className="font-display text-lg font-bold text-ink-900">New Workflow</h2>
      </div>
      <form onSubmit={submit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-ink-700 mb-1.5">Workflow name</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} required
            className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-ink-700 mb-1.5">Trigger · threshold (%)</label>
            <input type="number" min="0" max="100" value={threshold} onChange={(e) => setThreshold(e.target.value)} required
              className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100" />
            <p className="text-xs text-ink-500 mt-1">Fires when a student's average attendance drops below this.</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-ink-700 mb-1.5">Action · notification title</label>
            <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required
              className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100" />
            <p className="text-xs text-ink-500 mt-1">Shown in the notification bell.</p>
          </div>
        </div>
        <div className="flex items-center gap-3 pt-2">
          <button type="submit" disabled={busy}
            className="inline-flex items-center gap-2 gradient-gold text-ink-950 font-bold px-5 py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover hover:-translate-y-0.5 disabled:opacity-60 disabled:hover:translate-y-0">
            {busy ? 'Creating…' : 'Create workflow'}
          </button>
          <button type="button" onClick={onCancel}
            className="text-sm text-ink-600 hover:text-ink-900 font-semibold px-4 py-2.5 transition-colors">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default function Workflows() {
  const [workflows, setWorkflows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [busy, setBusy] = useState({});
  const [runAllResult, setRunAllResult] = useState(null);

  const fetchAll = async () => {
    setLoading(true);
    try {
      const res = await api.get('/workflows');
      setWorkflows(res.data.workflows || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchAll(); }, []);

  const toggle = async (id) => {
    setBusy((b) => ({ ...b, [id]: true }));
    try {
      await api.post(`/workflows/${id}/toggle`);
      await fetchAll();
    } catch (err) { console.error(err); }
    finally { setBusy((b) => ({ ...b, [id]: false })); }
  };

  const runOne = async (id) => {
    setBusy((b) => ({ ...b, [id]: true }));
    try {
      const res = await api.post(`/workflows/${id}/run`);
      setRunAllResult({ single: res.data });
      await fetchAll();
    } catch (err) { console.error(err); }
    finally { setBusy((b) => ({ ...b, [id]: false })); }
  };

  const remove = async (id) => {
    if (!window.confirm('Delete this workflow?')) return;
    setBusy((b) => ({ ...b, [id]: true }));
    try {
      await api.delete(`/workflows/${id}`);
      await fetchAll();
    } catch (err) { console.error(err); }
    finally { setBusy((b) => ({ ...b, [id]: false })); }
  };

  const runAll = async () => {
    setBusy((b) => ({ ...b, __all: true }));
    try {
      const res = await api.post('/workflows/run-all');
      setRunAllResult({ all: res.data.results });
      await fetchAll();
    } catch (err) { console.error(err); }
    finally { setBusy((b) => ({ ...b, __all: false })); }
  };

  return (
    <Layout>
      <div className="p-8 max-w-5xl mx-auto animate-fade-in">
        {/* Header */}
        <div className="mb-8 flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 text-[11px] text-gold-700 font-bold uppercase tracking-widest mb-3">
              <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
              Automation
            </div>
            <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">Workflows</h1>
            <p className="text-ink-500 text-[15px] leading-relaxed max-w-2xl">
              Event-driven automation. Define a trigger and an action — the platform runs it whenever the condition is met.
            </p>
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            <button onClick={runAll} disabled={busy.__all || workflows.length === 0}
              className="inline-flex items-center gap-2 text-sm bg-white border border-ink-200 hover:border-ink-400 text-ink-700 hover:text-ink-900 font-semibold px-4 py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover disabled:opacity-50">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {busy.__all ? 'Running…' : 'Run all active'}
            </button>
            <button onClick={() => setShowCreate(true)} disabled={showCreate}
              className="inline-flex items-center gap-2 gradient-gold text-ink-950 font-bold px-4 py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover hover:-translate-y-0.5 disabled:opacity-60 disabled:hover:translate-y-0">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              New workflow
            </button>
          </div>
        </div>

        {showCreate && <CreateForm onCreate={async () => { setShowCreate(false); await fetchAll(); }} onCancel={() => setShowCreate(false)} />}

        {runAllResult && (
          <div className="bg-white border border-emerald-200 rounded-2xl p-5 mb-6 shadow-card">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-8 h-8 rounded-lg bg-emerald-100 flex items-center justify-center">
                <svg className="w-4 h-4 text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div className="text-sm font-semibold text-ink-900">
                {runAllResult.single ? 'Workflow executed' : 'All workflows executed'}
              </div>
              <button onClick={() => setRunAllResult(null)} className="ml-auto text-xs text-ink-500 hover:text-ink-900">Dismiss</button>
            </div>
            <pre className="text-[11px] text-ink-700 bg-ink-50/60 border border-ink-100 p-3 rounded-lg overflow-auto max-h-64">
{JSON.stringify(runAllResult.single || runAllResult.all, null, 2)}
            </pre>
          </div>
        )}

        {loading && (
          <div className="bg-white border border-ink-200 rounded-xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading workflows…</div>
          </div>
        )}

        {!loading && workflows.length === 0 && !showCreate && (
          <div className="relative bg-gradient-to-br from-white to-ink-50/50 border-2 border-dashed border-ink-200 rounded-2xl p-16 text-center overflow-hidden">
            <div className="relative">
              <div className="w-16 h-16 mx-auto mb-5 rounded-2xl bg-gradient-to-br from-ink-900 to-ink-700 flex items-center justify-center shadow-float">
                <svg className="w-8 h-8 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div className="font-display text-xl font-bold text-ink-900 mb-2">No workflows yet</div>
              <div className="text-sm text-ink-500 max-w-md mx-auto mb-5">
                Create your first automation. For example: "If any student drops below 60% attendance, notify me."
              </div>
              <button onClick={() => setShowCreate(true)}
                className="inline-flex items-center gap-2 gradient-gold text-ink-950 font-bold px-5 py-2.5 rounded-lg shadow-card hover:shadow-card-hover hover:-translate-y-0.5 transition-all">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Create your first workflow
              </button>
            </div>
          </div>
        )}

        {!loading && workflows.length > 0 && (
          <div className="space-y-4">
            {workflows.map((w) => {
              const tm = TRIGGER_META[w.trigger_type] || { label: w.trigger_type, accent: 'slate', desc: '' };
              const am = ACTION_META[w.action_type] || { label: w.action_type, accent: 'slate' };
              const t = ACCENT[tm.accent] || ACCENT.slate;
              const a = ACCENT[am.accent] || ACCENT.slate;
              const isBusy = !!busy[w.id];
              return (
                <div key={w.id} className={`relative bg-white border rounded-2xl shadow-card overflow-hidden transition-all ${w.is_active ? 'border-ink-200' : 'border-ink-100 opacity-75'}`}>
                  <div className={`absolute top-0 left-0 right-0 h-1 ${w.is_active ? t.bar : 'bg-ink-200'}`} />
                  <div className="p-6">
                    <div className="flex flex-wrap items-start justify-between gap-3 mb-4">
                      <div className="min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <h3 className="font-display text-xl font-bold text-ink-900">{w.name}</h3>
                          {!w.is_active && (
                            <span className="text-[10px] uppercase tracking-widest font-bold px-2 py-0.5 rounded-full bg-ink-100 text-ink-600 border border-ink-200">Paused</span>
                          )}
                          {w.is_active && (
                            <span className="inline-flex items-center gap-1.5 text-[10px] uppercase tracking-widest font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                              Active
                            </span>
                          )}
                        </div>
                        {w.description && <p className="text-sm text-ink-600">{w.description}</p>}
                      </div>
                      <div className="flex items-center gap-2">
                        <button onClick={() => runOne(w.id)} disabled={isBusy}
                          className="inline-flex items-center gap-1.5 text-xs font-semibold text-ink-700 hover:text-ink-900 bg-white border border-ink-200 hover:border-ink-400 rounded-lg px-3 py-1.5 transition-all disabled:opacity-50">
                          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          Run now
                        </button>
                        <button onClick={() => toggle(w.id)} disabled={isBusy}
                          className="text-xs font-semibold text-ink-700 hover:text-ink-900 bg-white border border-ink-200 hover:border-ink-400 rounded-lg px-3 py-1.5 transition-all disabled:opacity-50">
                          {w.is_active ? 'Pause' : 'Resume'}
                        </button>
                        <button onClick={() => remove(w.id)} disabled={isBusy}
                          className="text-xs font-semibold text-red-700 hover:text-red-900 bg-white border border-red-200 hover:border-red-400 rounded-lg px-3 py-1.5 transition-all disabled:opacity-50">
                          Delete
                        </button>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                      <div className={`rounded-xl border px-4 py-3 ${t.bg} ${t.border}`}>
                        <div className="text-[10px] uppercase tracking-widest font-bold opacity-70 mb-0.5">When</div>
                        <div className={`font-semibold ${t.text}`}>{tm.label}</div>
                        <div className="text-xs opacity-75 mt-0.5">
                          {w.trigger_type === 'attendance_below' && `Threshold: ${w.trigger_config.threshold}%`}
                          {w.trigger_type !== 'attendance_below' && tm.desc}
                        </div>
                      </div>
                      <div className={`rounded-xl border px-4 py-3 ${a.bg} ${a.border}`}>
                        <div className="text-[10px] uppercase tracking-widest font-bold opacity-70 mb-0.5">Then</div>
                        <div className={`font-semibold ${a.text}`}>{am.label}</div>
                        <div className="text-xs opacity-75 mt-0.5">
                          {w.action_type === 'send_notification' && (w.action_config.title || 'Send a notification')}
                          {w.action_type === 'log_only' && 'Log to audit trail'}
                        </div>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-ink-100 flex flex-wrap items-center gap-5 text-xs text-ink-500">
                      <span className="inline-flex items-center gap-1.5">
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                        </svg>
                        {w.run_count} run{w.run_count === 1 ? '' : 's'}
                      </span>
                      {w.last_run_at && (
                        <span className="inline-flex items-center gap-1.5">
                          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          Last run {formatDate(w.last_run_at)}
                        </span>
                      )}
                    </div>
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
