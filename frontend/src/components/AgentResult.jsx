// =============================================================================
// UniNexus AI — Human-readable agent result cards (light academic theme)
// Roman Urdu: Agents ke results ko insaan ke samajhne layak banaya hai.
// =============================================================================

// Risk color tokens — used across risk-related agents for consistent visual language.
// Roman Urdu: Risk wale agents ke liye ek hi color language use ki hai.
const RISK_COLORS = {
  High: { bg: 'bg-red-50', text: 'text-red-700', border: 'border-red-200', dot: 'bg-red-500' },
  Medium: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200', dot: 'bg-amber-500' },
  Low: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200', dot: 'bg-emerald-500' },
};

// English: Choose the bar color based on attendance threshold.
// Roman Urdu: Attendance ke percentage ke hisaab se bar ka color choose karte hain.
function attendanceColor(pct) {
  if (pct < 60) return 'bg-red-500';
  if (pct < 75) return 'bg-amber-500';
  return 'bg-emerald-500';
}

// =============================================================================
// AttendanceResult — table of students flagged for low attendance
// Roman Urdu: Kam attendance wale students ki table.
// =============================================================================
function AttendanceResult({ data }) {
  return (
    <div className="space-y-5">
      <div className="flex items-baseline gap-3">
        <div className="text-4xl font-display font-bold text-ink-900">{data.total_flagged}</div>
        <div className="text-sm text-ink-500">
          student{data.total_flagged === 1 ? '' : 's'} flagged for low attendance
        </div>
      </div>

      <div className="overflow-hidden rounded-xl border border-ink-200 bg-white">
        <table className="w-full text-sm">
          <thead className="bg-ink-50/70">
            <tr>
              <th className="text-left px-4 py-2.5 text-[11px] font-semibold uppercase tracking-wider text-ink-500">Student</th>
              <th className="text-left px-4 py-2.5 text-[11px] font-semibold uppercase tracking-wider text-ink-500">ID</th>
              <th className="text-left px-4 py-2.5 text-[11px] font-semibold uppercase tracking-wider text-ink-500">Course</th>
              <th className="text-left px-4 py-2.5 text-[11px] font-semibold uppercase tracking-wider text-ink-500">Attendance</th>
            </tr>
          </thead>
          <tbody>
            {data.data.map((student, idx) => (
              <tr key={idx} className="border-t border-ink-100 hover:bg-ink-50/50 transition-colors">
                <td className="px-4 py-3 text-ink-900 font-medium">{student.name}</td>
                <td className="px-4 py-3 text-ink-500 font-mono text-xs">{student.student_number}</td>
                <td className="px-4 py-3 text-ink-700">{student.course}</td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2.5">
                    <div className="w-24 bg-ink-100 rounded-full h-1.5 overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all ${attendanceColor(student.attendance_percentage)}`}
                        style={{ width: `${student.attendance_percentage}%` }}
                      />
                    </div>
                    <span className="text-xs text-ink-700 font-mono w-10 tabular-nums">
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
// PolicyResult — threshold + rule
// Roman Urdu: Policy ka threshold aur applicable rule dikhata hai.
// =============================================================================
function PolicyResult({ data }) {
  return (
    <div className="flex flex-col md:flex-row md:items-center gap-5">
      <div className="bg-gradient-to-br from-ink-50 to-white border border-ink-200 rounded-xl px-6 py-4 min-w-[160px] shadow-card">
        <div className="text-[11px] uppercase tracking-widest text-ink-500 font-semibold mb-1">Threshold</div>
        <div className="text-4xl font-display font-bold text-ink-900">
          {data.policy_threshold}
          <span className="text-lg text-ink-400 ml-0.5">%</span>
        </div>
      </div>
      <div className="flex-1">
        <div className="text-[11px] uppercase tracking-widest text-ink-500 font-semibold mb-1.5">Applicable Rule</div>
        <div className="text-sm text-ink-700 leading-relaxed">{data.rule}</div>
      </div>
    </div>
  );
}

// =============================================================================
// RiskResult — summary chips + risk cards per student
// Roman Urdu: Risk ka summary aur har student ka risk card dikhata hai.
// =============================================================================
function RiskResult({ data }) {
  // Count students per risk level for the summary chips.
  // Roman Urdu: Har risk level pe kitne students hain, wo summary chips ke liye count karte hain.
  const counts = data.at_risk_students.reduce((acc, s) => {
    acc[s.risk_level] = (acc[s.risk_level] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="space-y-5">
      <div className="flex items-center gap-3 flex-wrap">
        <div className="text-xs text-ink-500 font-medium">Risk summary:</div>
        {Object.entries(counts).map(([level, count]) => {
          const c = RISK_COLORS[level] || RISK_COLORS.Low;
          return (
            <span
              key={level}
              className={`inline-flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full border font-medium ${c.bg} ${c.text} ${c.border}`}
            >
              <span className={`w-1.5 h-1.5 rounded-full ${c.dot}`}></span>
              {count} {level}
            </span>
          );
        })}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {data.at_risk_students.map((student, idx) => {
          const c = RISK_COLORS[student.risk_level] || RISK_COLORS.Low;
          return (
            <div
              key={idx}
              className="bg-white border border-ink-200 rounded-xl p-4 shadow-card hover-lift transition-all"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="font-semibold text-ink-900">{student.name}</div>
                  <div className="text-xs text-ink-500 font-mono mt-0.5">ID: {student.student_id}</div>
                </div>
                <span className={`inline-flex items-center gap-1.5 text-xs px-2 py-1 rounded-full border font-medium ${c.bg} ${c.text} ${c.border}`}>
                  <span className={`w-1.5 h-1.5 rounded-full ${c.dot}`}></span>
                  {student.risk_level}
                </span>
              </div>
              <div className="flex items-center gap-5 text-xs pt-3 border-t border-ink-100">
                <div>
                  <div className="text-ink-400 mb-0.5">Attendance</div>
                  <div className="text-ink-900 font-mono font-medium">{student.attendance}%</div>
                </div>
                <div>
                  <div className="text-ink-400 mb-0.5">Grade</div>
                  <div className="text-ink-900 font-mono font-medium">{student.grade}</div>
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
// KnowledgeResult — document cards with title, category, preview
// Roman Urdu: Knowledge Base se mile documents ke cards.
// =============================================================================
function KnowledgeResult({ data }) {
  return (
    <div className="space-y-3">
      <div className="text-[11px] uppercase tracking-widest text-ink-500 font-semibold">
        {data.total_matches} document{data.total_matches === 1 ? '' : 's'} found
      </div>
      {data.documents.map((doc, idx) => (
        <div
          key={idx}
          className="bg-white border border-ink-200 rounded-xl p-4 shadow-card hover-lift transition-all"
        >
          <div className="flex items-center gap-2.5 mb-2">
            <div className="font-semibold text-ink-900">{doc.title}</div>
            {doc.category && (
              <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full bg-ink-100 text-ink-600 border border-ink-200 font-medium">
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
// Dispatcher — routes to the correct visual card based on agent name.
// Roman Urdu: Agent ke naam se decide karta hai konsa card dikhana hai.
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
        <pre className="text-xs text-ink-300 bg-ink-950 p-4 rounded-lg overflow-auto max-h-96">
          {JSON.stringify(result, null, 2)}
        </pre>
      );
  }
}
