// =============================================================================
// UniNexus AI — Agent result cards with distinct visual identity per agent.
// Roman Urdu: Har agent ke result ka apna color aur style hai — sab alag alag.
// =============================================================================

// Per-agent theme — each agent gets its own color identity.
// Roman Urdu: Har agent ka apna rang hai taake user turant pehchane.
const AGENT_THEME = {
  AttendanceAgent: {
    bg: 'from-blue-50 to-white',
    border: 'border-blue-200',
    accent: 'bg-blue-500',
    icon_bg: 'bg-blue-100',
    icon_fg: 'text-blue-700',
  },
  PolicyAgent: {
    bg: 'from-amber-50 to-white',
    border: 'border-amber-200',
    accent: 'bg-amber-500',
    icon_bg: 'bg-amber-100',
    icon_fg: 'text-amber-700',
  },
  RiskAgent: {
    bg: 'from-red-50 to-white',
    border: 'border-red-200',
    accent: 'bg-red-500',
    icon_bg: 'bg-red-100',
    icon_fg: 'text-red-700',
  },
  KnowledgeAgent: {
    bg: 'from-violet-50 to-white',
    border: 'border-violet-200',
    accent: 'bg-violet-500',
    icon_bg: 'bg-violet-100',
    icon_fg: 'text-violet-700',
  },
};

const RISK_THEME = {
  High:   { bg: 'bg-red-50',    border: 'border-red-200',    text: 'text-red-700',    chip: 'bg-red-100',    dot: 'bg-red-500' },
  Medium: { bg: 'bg-amber-50',  border: 'border-amber-200',  text: 'text-amber-800',  chip: 'bg-amber-100',  dot: 'bg-amber-500' },
  Low:    { bg: 'bg-emerald-50',border: 'border-emerald-200',text: 'text-emerald-700',chip: 'bg-emerald-100',dot: 'bg-emerald-500' },
};

function attendanceColor(pct) {
  if (pct < 60) return 'bg-red-500';
  if (pct < 75) return 'bg-amber-500';
  return 'bg-emerald-500';
}

// =============================================================================
// AttendanceResult
// =============================================================================
function AttendanceResult({ data }) {
  return (
    <div className="space-y-4">
      <div className="flex items-baseline gap-3">
        <div className="text-5xl font-display font-bold text-blue-900 leading-none">
          {data.total_flagged}
        </div>
        <div className="text-sm text-ink-600 pb-1">
          student{data.total_flagged === 1 ? '' : 's'} flagged for low attendance
        </div>
      </div>

      <div className="rounded-xl border border-blue-100 overflow-hidden bg-white">
        <table className="w-full text-sm">
          <thead className="bg-blue-50/70">
            <tr>
              <th className="text-left px-4 py-2.5 text-[11px] font-bold uppercase tracking-wider text-blue-800">Student</th>
              <th className="text-left px-4 py-2.5 text-[11px] font-bold uppercase tracking-wider text-blue-800">ID</th>
              <th className="text-left px-4 py-2.5 text-[11px] font-bold uppercase tracking-wider text-blue-800">Course</th>
              <th className="text-left px-4 py-2.5 text-[11px] font-bold uppercase tracking-wider text-blue-800">Attendance</th>
            </tr>
          </thead>
          <tbody>
            {data.data.map((student, idx) => (
              <tr key={idx} className="border-t border-blue-100/60 hover:bg-blue-50/40 transition-colors">
                <td className="px-4 py-3 text-ink-900 font-semibold">{student.name}</td>
                <td className="px-4 py-3 text-ink-500 font-mono text-xs">{student.student_number}</td>
                <td className="px-4 py-3 text-ink-700 font-medium">{student.course}</td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2.5">
                    <div className="w-24 bg-ink-100 rounded-full h-2 overflow-hidden">
                      <div
                        className={`h-full rounded-full ${attendanceColor(student.attendance_percentage)}`}
                        style={{ width: `${student.attendance_percentage}%` }}
                      />
                    </div>
                    <span className="text-xs text-ink-800 font-mono font-semibold w-10 tabular-nums">
                      {student.attendance_percentage}%
                    </span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// =============================================================================
// PolicyResult
// =============================================================================
function PolicyResult({ data }) {
  return (
    <div className="flex flex-col md:flex-row md:items-stretch gap-4">
      <div className="bg-gradient-to-br from-amber-100 to-amber-50 border border-amber-200 rounded-xl px-7 py-5 min-w-[190px] shadow-card">
        <div className="text-[11px] uppercase tracking-widest text-amber-800 font-bold mb-1">Threshold</div>
        <div className="text-5xl font-display font-bold text-amber-900 leading-none">
          {data.policy_threshold}<span className="text-2xl text-amber-600 ml-1">%</span>
        </div>
      </div>
      <div className="flex-1 bg-white border border-amber-100 rounded-xl px-6 py-5">
        <div className="text-[11px] uppercase tracking-widest text-amber-800 font-bold mb-2">Applicable Rule</div>
        <div className="text-[15px] text-ink-800 leading-relaxed font-medium">{data.rule}</div>
      </div>
    </div>
  );
}

// =============================================================================
// RiskResult
// =============================================================================
function RiskResult({ data }) {
  const counts = data.at_risk_students.reduce((acc, s) => {
    acc[s.risk_level] = (acc[s.risk_level] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="space-y-5">
      <div className="flex items-center gap-3 flex-wrap">
        <div className="text-[11px] uppercase tracking-widest text-ink-500 font-bold">Risk Summary</div>
        {Object.entries(counts).map(([level, count]) => {
          const t = RISK_THEME[level] || RISK_THEME.Low;
          return (
            <span
              key={level}
              className={`inline-flex items-center gap-2 text-xs px-3 py-1.5 rounded-full border-2 font-bold ${t.bg} ${t.text} ${t.border}`}
            >
              <span className={`w-2 h-2 rounded-full ${t.dot}`}></span>
              {count} {level}
            </span>
          );
        })}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {data.at_risk_students.map((student, idx) => {
          const t = RISK_THEME[student.risk_level] || RISK_THEME.Low;
          return (
            <div
              key={idx}
              className={`relative border-2 rounded-xl p-5 ${t.bg} ${t.border} shadow-card hover-lift transition-all overflow-hidden`}
            >
              <div className={`absolute top-0 left-0 right-0 h-1 ${t.dot}`} />
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="font-bold text-ink-900 text-base">{student.name}</div>
                  <div className="text-xs text-ink-500 font-mono mt-0.5">ID: {student.student_id}</div>
                </div>
                <span className={`inline-flex items-center gap-1.5 text-[11px] px-2.5 py-1 rounded-full font-bold uppercase tracking-wide ${t.chip} ${t.text}`}>
                  <span className={`w-1.5 h-1.5 rounded-full ${t.dot}`}></span>
                  {student.risk_level}
                </span>
              </div>
              <div className="grid grid-cols-2 gap-4 pt-3 border-t border-ink-200/50">
                <div>
                  <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1">Attendance</div>
                  <div className="text-lg text-ink-900 font-bold font-mono">{student.attendance}%</div>
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1">Grade</div>
                  <div className="text-lg text-ink-900 font-bold font-mono">{student.grade}</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// =============================================================================
// KnowledgeResult
// =============================================================================
function KnowledgeResult({ data }) {
  return (
    <div className="space-y-3">
      <div className="text-[11px] uppercase tracking-widest text-violet-800 font-bold">
        {data.total_matches} document{data.total_matches === 1 ? '' : 's'} retrieved
      </div>
      {data.documents.map((doc, idx) => (
        <div
          key={idx}
          className="bg-white border border-violet-100 rounded-xl p-4 shadow-card hover-lift transition-all"
        >
          <div className="flex items-center gap-2.5 mb-2">
            <div className="font-bold text-ink-900">{doc.title}</div>
            {doc.category && (
              <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full bg-violet-100 text-violet-700 border border-violet-200 font-bold">
                {doc.category}
              </span>
            )}
          </div>
          <div className="text-sm text-ink-600 leading-relaxed">{doc.content_preview}</div>
        </div>
      ))}
    </div>
  );
}

// =============================================================================
// Dispatcher
// =============================================================================
export default function AgentResult({ agentName, result }) {
  if (!result || result.status !== 'success') {
    return (
      <div className="text-sm text-ink-500 italic bg-ink-50 border border-dashed border-ink-200 rounded-lg p-4">
        No results available for this step.
      </div>
    );
  }

  switch (agentName) {
    case 'AttendanceAgent': return <AttendanceResult data={result} />;
    case 'PolicyAgent':     return <PolicyResult data={result} />;
    case 'RiskAgent':       return <RiskResult data={result} />;
    case 'KnowledgeAgent':  return <KnowledgeResult data={result} />;
    default:
      return (
        <pre className="text-xs text-ink-100 bg-ink-950 p-4 rounded-lg overflow-auto max-h-96">
          {JSON.stringify(result, null, 2)}
        </pre>
      );
  }
}
