import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

// English: Color the attendance badge based on thresholds.
// Roman Urdu: Attendance ke hisaab se badge ka rang set karte hain.
function attendanceBadge(pct) {
  if (pct < 60) return 'bg-red-50 text-red-700 border-red-200';
  if (pct < 75) return 'bg-amber-50 text-amber-800 border-amber-200';
  return 'bg-emerald-50 text-emerald-700 border-emerald-200';
}

// English: Small bar showing attendance visual.
// Roman Urdu: Chhota bar jo attendance ko visually dikhata hai.
function AttendanceBar({ pct }) {
  const color = pct < 60 ? 'bg-red-500' : pct < 75 ? 'bg-amber-500' : 'bg-emerald-500';
  return (
    <div className="flex items-center gap-2.5">
      <div className="w-20 bg-ink-100 rounded-full h-1.5 overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs text-ink-700 font-mono tabular-nums w-12">{pct}%</span>
    </div>
  );
}

export default function Students() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  // English: Load all students with aggregate enrollment + attendance data.
  // Roman Urdu: Sab students load karo enrollment aur attendance ke saath.
  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await api.get('/academic/students');
        setStudents(response.data.students);
      } catch (err) {
        console.error('Failed to fetch students', err);
      } finally {
        setLoading(false);
      }
    };
    fetchStudents();
  }, []);

  // English: Filter rows as the user types.
  // Roman Urdu: Jab user type kare to rows filter karo.
  const filtered = students.filter((s) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      s.first_name.toLowerCase().includes(q) ||
      s.last_name.toLowerCase().includes(q) ||
      s.email.toLowerCase().includes(q) ||
      s.student_number.toLowerCase().includes(q)
    );
  });

  // English: Summary metrics across all students.
  // Roman Urdu: Sab students ke summary metrics.
  const totalStudents = students.length;
  const avgAttendance = totalStudents
    ? Math.round(students.reduce((sum, s) => sum + (s.average_attendance || 0), 0) / totalStudents)
    : 0;
  const atRisk = students.filter((s) => (s.average_attendance || 0) < 75).length;

  return (
    <Layout>
      <div className="p-8 max-w-6xl mx-auto animate-fade-in">
        {/* ==================== Header ==================== */}
        <div className="mb-8">
          <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">
            Students
          </h1>
          <p className="text-ink-500 text-[15px] leading-relaxed">
            All students registered in your institution, with live enrollment and attendance data.
          </p>
        </div>

        {/* ==================== Summary Cards ==================== */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">
              Total Students
            </div>
            <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">
              {loading ? '—' : totalStudents}
            </div>
          </div>
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">
              Average Attendance
            </div>
            <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">
              {loading ? '—' : avgAttendance + '%'}
            </div>
          </div>
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">
              Below 75% Threshold
            </div>
            <div className="text-3xl font-display font-bold text-red-600 tracking-tight">
              {loading ? '—' : atRisk}
            </div>
          </div>
        </div>

        {/* ==================== Search ==================== */}
        <div className="bg-white border border-ink-200 rounded-xl p-4 mb-6 shadow-card">
          <div className="relative">
            <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
            </svg>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by name, email, or student number…"
              className="w-full bg-ink-50/50 border border-ink-200 rounded-lg pl-10 pr-4 py-2.5 text-ink-900 placeholder-ink-400 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100 transition-all"
            />
          </div>
        </div>

        {/* ==================== Loading ==================== */}
        {loading && (
          <div className="bg-white border border-ink-200 rounded-xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading students…</div>
          </div>
        )}

        {/* ==================== Empty ==================== */}
        {!loading && filtered.length === 0 && (
          <div className="bg-white border-2 border-dashed border-ink-200 rounded-xl p-16 text-center">
            <div className="text-ink-500">
              {search ? 'No students match your search.' : 'No students found.'}
            </div>
          </div>
        )}

        {/* ==================== Table ==================== */}
        {!loading && filtered.length > 0 && (
          <div className="bg-white border border-ink-200 rounded-xl overflow-hidden shadow-card">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-ink-50/70 border-b border-ink-200">
                  <tr>
                    <th className="text-left px-4 py-3 text-[11px] font-bold uppercase tracking-widest text-ink-500">ID</th>
                    <th className="text-left px-4 py-3 text-[11px] font-bold uppercase tracking-widest text-ink-500">Student</th>
                    <th className="text-left px-4 py-3 text-[11px] font-bold uppercase tracking-widest text-ink-500">Email</th>
                    <th className="text-left px-4 py-3 text-[11px] font-bold uppercase tracking-widest text-ink-500">Year</th>
                    <th className="text-left px-4 py-3 text-[11px] font-bold uppercase tracking-widest text-ink-500">Courses</th>
                    <th className="text-left px-4 py-3 text-[11px] font-bold uppercase tracking-widest text-ink-500">Avg Attendance</th>
                    <th className="text-right px-4 py-3 text-[11px] font-bold uppercase tracking-widest text-ink-500">Badge</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((s) => {
                    const attendance = s.average_attendance || 0;
                    return (
                      <tr key={s.id} className="border-t border-ink-100 hover:bg-ink-50/40 transition-colors">
                        <td className="px-4 py-3 text-ink-500 font-mono text-xs">{s.student_number}</td>
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-ink-900 text-gold-300 flex items-center justify-center text-[10px] font-bold flex-shrink-0">
                              {s.first_name[0]}{s.last_name[0]}
                            </div>
                            <span className="text-ink-900 font-semibold">
                              {s.first_name} {s.last_name}
                            </span>
                          </div>
                        </td>
                        <td className="px-4 py-3 text-ink-600 text-xs">{s.email}</td>
                        <td className="px-4 py-3 text-ink-600 text-xs">{s.enrollment_year}</td>
                        <td className="px-4 py-3 text-ink-700">{s.total_courses}</td>
                        <td className="px-4 py-3">
                          <AttendanceBar pct={attendance} />
                        </td>
                        <td className="px-4 py-3 text-right">
                          <span className={`inline-block text-[10px] font-bold uppercase tracking-widest px-2 py-1 rounded-full border ${attendanceBadge(attendance)}`}>
                            {attendance < 60 ? 'Critical' : attendance < 75 ? 'At Risk' : 'Good'}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            <div className="px-4 py-3 border-t border-ink-100 bg-ink-50/40 text-xs text-ink-500">
              Showing {filtered.length} of {totalStudents} student{totalStudents === 1 ? '' : 's'}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
