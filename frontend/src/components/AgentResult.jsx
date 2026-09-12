// Color thresholds and styling
const RISK_COLORS = {
  High: 'bg-red-500/15 text-red-300 border-red-500/40',
  Medium: 'bg-yellow-500/15 text-yellow-300 border-yellow-500/40',
  Low: 'bg-green-500/15 text-green-300 border-green-500/40',
};

function attendanceColor(pct) {
  if (pct < 60) return 'bg-red-500';
  if (pct < 75) return 'bg-yellow-500';
  return 'bg-green-500';
}

// ========== AttendanceAgent ==========
function AttendanceResult({ data }) {
  return (
    <div className="space-y-4">
      <div className="flex items-baseline gap-3">
        <div className="text-3xl font-bold text-white">{data.total_flagged}</div>
        <div className="text-sm text-slate-400">students flagged for low attendance</div>
      </div>
      <div className="overflow-hidden rounded-lg border border-slate-700">
        <table className="w-full text-sm">
          <thead className="bg-slate-900/50">
            <tr>
              <th className="text-left px-4 py-2 font-medium text-slate-400 text-xs uppercase tracking-wider">Student</th>
              <th className="text-left px-4 py-2 font-medium text-slate-400 text-xs uppercase tracking-wider">ID</th>
              <th className="text-left px-4 py-2 font-medium text-slate-400 text-xs uppercase tracking-wider">Course</th>
              <th className="text-left px-4 py-2 font-medium text-slate-400 text-xs uppercase tracking-wider">Attendance</th>
            </tr>
          </thead>
          <tbody>
            {data.data.map((student, idx) => (
              <tr key={idx} className="border-t border-slate-700/50 hover:bg-slate-700/20 transition-colors">
                <td className="px-4 py-3 text-white font-medium">{student.name}</td>
                <td className="px-4 py-3 text-slate-400 font-mono text-xs">{student.student_number}</td>
                <td className="px-4 py-3 text-slate-300">{student.course}</td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <div className="w-20 bg-slate-700 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${attendanceColor(student.attendance_percentage)}`}
                        style={{ width: `${student.attendance_percentage}%` }}
                      />
                    </div>
                    <span className="text-xs text-slate-300 font-mono w-10">{student.attendance_percentage}%</span>
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

// ========== PolicyAgent ==========
function PolicyResult({ data }) {
  return (
    <div className="flex flex-col md:flex-row md:items-center gap-4">
      <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg px-6 py-4 min-w-[140px]">
        <div className="text-xs uppercase tracking-wider text-blue-400 mb-1">Threshold</div>
        <div className="text-3xl font-bold text-white">{data.policy_threshold}<span className="text-lg text-slate-400">%</span></div>
      </div>
      <div className="flex-1">
        <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">Applicable Rule</div>
        <div className="text-sm text-slate-200 leading-relaxed">{data.rule}</div>
      </div>
    </div>
  );
}

// ========== RiskAgent ==========
function RiskResult({ data }) {
  const counts = data.at_risk_students.reduce((acc, s) => {
    acc[s.risk_level] = (acc[s.risk_level] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3 flex-wrap">
        <div className="text-sm text-slate-400">Risk summary:</div>
        {Object.entries(counts).map(([level, count]) => (
          <span key={level} className={`text-xs px-2.5 py-1 rounded border font-medium ${RISK_COLORS[level]}`}>
            {count} {level}
          </span>
        ))}
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {data.at_risk_students.map((student, idx) => (
          <div key={idx} className="bg-slate-900 border border-slate-700 rounded-lg p-4 hover:border-slate-500 transition-colors">
            <div className="flex items-start justify-between mb-3">
              <div>
                <div className="font-medium text-white">{student.name}</div>
                <div className="text-xs text-slate-500 font-mono">ID: {student.student_id}</div>
              </div>
              <span className={`text-xs px-2 py-1 rounded border font-medium ${RISK_COLORS[student.risk_level] || 'bg-slate-700 text-slate-300 border-slate-600'}`}>
                {student.risk_level}
              </span>
            </div>
            <div className="flex items-center gap-4 text-xs pt-3 border-t border-slate-700/50">
              <div>
                <div className="text-slate-500 mb-0.5">Attendance</div>
                <div className="text-slate-100 font-mono">{student.attendance}%</div>
              </div>
              <div>
                <div className="text-slate-500 mb-0.5">Grade</div>
                <div className="text-slate-100 font-mono">{student.grade}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ========== KnowledgeAgent ==========
function KnowledgeResult({ data }) {
  return (
    <div className="space-y-3">
      <div className="text-xs uppercase tracking-wider text-slate-500">
        {data.total_matches} document{data.total_matches === 1 ? '' : 's'} found
      </div>
      {data.documents.map((doc, idx) => (
        <div key={idx} className="bg-slate-900 border border-slate-700 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <div className="font-medium text-white">{doc.title}</div>
            {doc.category && (
              <span className="text-xs px-2 py-0.5 rounded bg-slate-700 text-slate-300">
                {doc.category}
              </span>
            )}
          </div>
          <div className="text-sm text-slate-400 leading-relaxed">{doc.content_preview}</div>
        </div>
      ))}
    </div>
  );
}

// ========== Dispatcher ==========
export default function AgentResult({ agentName, result }) {
  if (!result || result.status !== 'success') {
    return <div className="text-sm text-slate-400 italic">No results available.</div>;
  }

  switch (agentName) {
    case 'AttendanceAgent':
      return <AttendanceResult data={result} />;
    case 'PolicyAgent':
      return <PolicyResult data={result} />;
    case 'RiskAgent':
      return <RiskResult data={result} />;
    case 'KnowledgeAgent':
      return <KnowledgeResult data={result} />;
    default:
      return (
        <pre className="text-xs text-slate-300 bg-slate-950 p-4 rounded-lg overflow-auto max-h-96">
          {JSON.stringify(result, null, 2)}
        </pre>
      );
  }
}
