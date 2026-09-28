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

const STATUS_META = {
  pending:  { label: 'Pending review', bg: 'bg-amber-50',   text: 'text-amber-800',  border: 'border-amber-200', dot: 'bg-amber-500' },
  executed: { label: 'Completed',      bg: 'bg-emerald-50', text: 'text-emerald-700',border: 'border-emerald-200', dot: 'bg-emerald-500' },
  rejected: { label: 'Declined',       bg: 'bg-slate-100',  text: 'text-slate-700',  border: 'border-slate-200', dot: 'bg-slate-500' },
  failed:   { label: 'Failed',         bg: 'bg-red-50',     text: 'text-red-700',    border: 'border-red-200',   dot: 'bg-red-500' },
};

// English: Icon components per action type — visual clarity for end users.
// Roman Urdu: Har action type ka icon — end users ke liye visual clarity.
const ACTION_ICON = {
  grade: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 10L12 5 2 10l10 5 10-5z" />
      <path d="M6 12v5c0 1.5 3 3 6 3s6-1.5 6-3v-5" />
    </svg>
  ),
  notification: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" />
      <path d="M13.73 21a2 2 0 01-3.46 0" />
    </svg>
  ),
  default: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M13 10V3L4 14h7v7l9-11h-7z" />
    </svg>
  ),
};

const ACCENT = {
  blue:   { iconBg: 'bg-blue-100',   iconText: 'text-blue-700',   bar: 'bg-blue-500',   chip: 'bg-blue-50 text-blue-700 border-blue-200' },
  amber:  { iconBg: 'bg-amber-100',  iconText: 'text-amber-700',  bar: 'bg-amber-500',  chip: 'bg-amber-50 text-amber-800 border-amber-200' },
  violet: { iconBg: 'bg-violet-100', iconText: 'text-violet-700', bar: 'bg-violet-500', chip: 'bg-violet-50 text-violet-700 border-violet-200' },
};

// English: Turn a raw approval into human-readable presentation.
// Roman Urdu: Raw approval ko human-readable presentation mein badlo.
function present(approval, studentsMap, coursesMap) {
  const args = approval.args || {};
  const tool = approval.tool_name;
  const result = approval.result || {};

  if (tool === 'update_student_grade') {
    const name = studentsMap[args.student_number] || args.student_number || 'Unknown student';
    const courseTitle = coursesMap[args.course_code] || '';
    const oldGrade = result.old_grade;
    const newGrade = args.new_grade || result.new_grade;
    return {
      icon: 'grade',
      accent: 'blue',
      category: 'Grade Change',
      headline: `${name}'s ${args.course_code} grade`,
      courseLine: courseTitle ? `${args.course_code} — ${courseTitle}` : args.course_code,
      studentLine: name,
      gradeChange: { from: oldGrade, to: newGrade },
      friendlyReason: oldGrade
        ? `Grade was ${oldGrade}, admin will change it to ${newGrade}.`
        : `Admin will set the grade to ${newGrade}.`,
    };
  }

  if (tool === 'send_student_notification') {
    const name = studentsMap[args.student_number] || args.student_number || 'Unknown student';
    return {
      icon: 'notification',
      accent: 'violet',
      category: 'Send Notification',
      headline: `Message to ${name}`,
      studentLine: name,
      message: args.message,
      friendlyReason: `A notification will be delivered to ${name}'s university account.`,
    };
  }

  return {
    icon: 'default',
    accent: 'amber',
    category: tool.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
    headline: approval.action_description || tool,
    friendlyReason: approval.reasoning || '',
  };
}

function ApprovalCard({ approval, studentsMap, coursesMap, onApprove, onReject, busy }) {
  const status = STATUS_META[approval.status] || STATUS_META.pending;
  const p = present(approval, studentsMap, coursesMap);
  const accent = ACCENT[p.accent] || ACCENT.blue;
  const [showTech, setShowTech] = useState(false);
  const isPending = approval.status === 'pending';

  return (
    <div className="relative bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden">
      <div className={`absolute top-0 left-0 right-0 h-1 ${accent.bar}`} />

      {/* Header */}
      <div className="px-6 py-5 flex flex-wrap items-start justify-between gap-4">
        <div className="flex items-start gap-4 min-w-0">
          <div className={`w-12 h-12 rounded-xl ${accent.iconBg} ${accent.iconText} flex items-center justify-center flex-shrink-0`}>
            <div className="w-6 h-6">{ACTION_ICON[p.icon]}</div>
          </div>
          <div className="min-w-0">
            <div className="text-[11px] uppercase tracking-widest text-ink-500 font-bold mb-1">
              {p.category}
            </div>
            <h3 className="font-display text-xl font-bold text-ink-900 leading-tight">
              {p.headline}
            </h3>
            {p.courseLine && (
              <div className="text-sm text-ink-600 mt-1">{p.courseLine}</div>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          <span className={`inline-flex items-center gap-1.5 text-[11px] font-bold px-2.5 py-1 rounded-full border ${status.bg} ${status.text} ${status.border}`}>
            <span className={`w-1.5 h-1.5 rounded-full ${status.dot}`}></span>
            {status.label}
          </span>
          <span className="text-[11px] text-ink-400 font-mono">#{approval.id}</span>
        </div>
      </div>

      {/* Body */}
      <div className="px-6 pb-6 space-y-4">
        {/* Friendly summary */}
        <div className={`rounded-xl border px-5 py-4 ${accent.chip}`}>
          {p.gradeChange && (
            <div className="flex items-center gap-4 mb-2">
              <div>
                <div className="text-[10px] uppercase tracking-widest font-bold opacity-70 mb-0.5">Current</div>
                <div className="text-3xl font-display font-bold">{p.gradeChange.from || '—'}</div>
              </div>
              <svg className="w-6 h-6 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
              <div>
                <div className="text-[10px] uppercase tracking-widest font-bold opacity-70 mb-0.5">New</div>
                <div className="text-3xl font-display font-bold">{p.gradeChange.to}</div>
              </div>
            </div>
          )}
          {p.message && (
            <div className="text-[15px] leading-relaxed font-medium">{p.message}</div>
          )}
          <div className="text-xs opacity-80 mt-1">{p.friendlyReason}</div>
        </div>

        {/* Meta row */}
        <div className="flex flex-wrap items-center gap-x-5 gap-y-2 text-xs text-ink-500">
          <span className="inline-flex items-center gap-1.5">
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Requested by <span className="text-ink-800 font-medium">{approval.user_email?.split('@')[0] || 'System'}</span>
          </span>
          <span className="inline-flex items-center gap-1.5">
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {formatDate(approval.created_at)}
          </span>
          {approval.resolved_at && (
            <span className="inline-flex items-center gap-1.5 text-emerald-700">
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
              </svg>
              {approval.status === 'executed' ? 'Completed' : 'Resolved'} {formatDate(approval.resolved_at)}
            </span>
          )}
        </div>

        {/* Technical details toggle */}
        <div>
          <button
            onClick={() => setShowTech((v) => !v)}
            className="inline-flex items-center gap-1.5 text-xs text-ink-500 hover:text-ink-900 font-medium transition-colors"
          >
            <svg className={`w-3.5 h-3.5 transition-transform ${showTech ? 'rotate-90' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
            {showTech ? 'Hide' : 'Show'} technical details
          </button>
          {showTech && (
            <div className="mt-3 space-y-3">
              <div>
                <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1.5">Tool</div>
                <code className="text-xs font-mono bg-ink-50 border border-ink-200 rounded px-2 py-1 text-ink-800">{approval.tool_name}</code>
              </div>
              <div>
                <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1.5">Arguments</div>
                <pre className="text-[11px] text-ink-800 bg-ink-50/60 border border-ink-100 p-3 rounded-lg overflow-auto">
{JSON.stringify(approval.args, null, 2)}
                </pre>
              </div>
              {approval.reasoning && (
                <div>
                  <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1.5">Agent reasoning</div>
                  <div className="text-xs text-ink-600 italic bg-ink-50/60 border border-ink-100 rounded-lg px-3 py-2">
                    &ldquo;{approval.reasoning}&rdquo;
                  </div>
                </div>
              )}
              {approval.result && (
                <div>
                  <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1.5">Execution result</div>
                  <pre className="text-[11px] text-emerald-800 bg-emerald-50/60 border border-emerald-100 p-3 rounded-lg overflow-auto">
{JSON.stringify(approval.result, null, 2)}
                  </pre>
                </div>
              )}
              {approval.error && (
                <div>
                  <div className="text-[10px] uppercase tracking-widest text-red-500 font-bold mb-1.5">Error</div>
                  <div className="text-xs text-red-700 bg-red-50 border border-red-100 rounded-lg px-3 py-2">{approval.error}</div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Action buttons */}
        {isPending && (
          <div className="flex flex-wrap items-center gap-3 pt-4 border-t border-ink-100">
            <button
              onClick={() => onApprove(approval.id)}
              disabled={busy}
              className="inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 disabled:bg-emerald-300 text-white font-bold px-6 py-3 rounded-xl transition-all shadow-card hover:shadow-card-hover hover:-translate-y-0.5 disabled:hover:translate-y-0"
            >
              {busy ? (
                <><span className="inline-block w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>Processing…</>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                  </svg>
                  Approve
                </>
              )}
            </button>
            <button
              onClick={() => onReject(approval.id)}
              disabled={busy}
              className="inline-flex items-center gap-2 bg-white hover:bg-ink-50 disabled:opacity-50 text-ink-700 border-2 border-ink-200 hover:border-ink-400 font-bold px-6 py-3 rounded-xl transition-all"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
              </svg>
              Decline
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default function Approvals() {
  const [approvals, setApprovals] = useState([]);
  const [studentsMap, setStudentsMap] = useState({});
  const [coursesMap, setCoursesMap] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('pending');
  const [busy, setBusy] = useState({});

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

  // English: Load students + courses once so we can display names instead of codes.
  // Roman Urdu: Students aur courses ek dafa load karo taake codes ki jagah naam dikha sakein.
  useEffect(() => {
    (async () => {
      try {
        const [sRes, cRes] = await Promise.all([
          api.get('/academic/students'),
          api.get('/academic/courses'),
        ]);
        const sm = {};
        (sRes.data.students || []).forEach((s) => {
          sm[s.student_number] = `${s.first_name} ${s.last_name}`;
        });
        setStudentsMap(sm);
        const cm = {};
        (cRes.data.courses || []).forEach((c) => {
          cm[c.course_code] = c.title;
        });
        setCoursesMap(cm);
      } catch (err) {
        console.error('Failed to load lookup data', err);
      }
    })();
  }, []);

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
      <div className="p-8 max-w-4xl mx-auto animate-fade-in">
        {/* Header */}
        <div className="mb-8 flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 text-[11px] text-gold-700 font-bold uppercase tracking-widest mb-3">
              <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
              Pending Reviews
            </div>
            <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">Approvals</h1>
            <p className="text-ink-500 text-[15px] leading-relaxed max-w-2xl">
              Sensitive actions queued by the AI are held here until a human approves them.
              Review each request and click Approve or Decline.
            </p>
          </div>
          <button
            onClick={fetchApprovals}
            disabled={loading}
            className="inline-flex items-center gap-2 text-sm bg-white border border-ink-200 hover:border-ink-400 text-ink-700 hover:text-ink-900 font-semibold px-4 py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover"
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
            { id: 'pending', label: 'Needs review' },
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
          <div className="bg-white border border-ink-200 rounded-2xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading approvals…</div>
          </div>
        )}

        {!loading && approvals.length === 0 && (
          <div className="relative bg-gradient-to-br from-white to-ink-50/50 border-2 border-dashed border-ink-200 rounded-2xl p-16 text-center overflow-hidden">
            <div className="relative">
              <div className="w-16 h-16 mx-auto mb-5 rounded-2xl bg-emerald-100 flex items-center justify-center">
                <svg className="w-8 h-8 text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div className="font-display text-xl font-bold text-ink-900 mb-2">
                {filter === 'pending' ? 'Nothing waiting for you' : 'No requests yet'}
              </div>
              <div className="text-sm text-ink-500 max-w-md mx-auto">
                {filter === 'pending'
                  ? 'All caught up. Sensitive actions requested by the AI will appear here for your review.'
                  : 'When the AI needs approval for a sensitive action, it will show up here.'}
              </div>
            </div>
          </div>
        )}

        {approvals.length > 0 && (
          <div className="space-y-5">
            {approvals.map((a) => (
              <ApprovalCard
                key={a.id}
                approval={a}
                studentsMap={studentsMap}
                coursesMap={coursesMap}
                onApprove={handleApprove}
                onReject={handleReject}
                busy={!!busy[a.id]}
              />
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}
