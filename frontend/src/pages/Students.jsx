import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

function attendanceBadge(pct) {
  if (pct < 60) return 'bg-red-500/15 text-red-300 border-red-500/40';
  if (pct < 75) return 'bg-yellow-500/15 text-yellow-300 border-yellow-500/40';
  return 'bg-green-500/15 text-green-300 border-green-500/40';
}

export default function Students() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await api.get('/academic/students');
        setStudents(response.data.students);
      } catch (err) {
        console.error('Failed to fetch students', err);
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  return (
    <Layout>
      <div className="p-8 max-w-6xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-white mb-2">Students</h1>
          <p className="text-slate-400">
            All students registered in your institution, with live enrollment and attendance data.
          </p>
        </div>

        {loading && (
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-16 text-center">
            <div className="text-slate-500">Loading students...</div>
          </div>
        )}

        {!loading && students.length === 0 && (
          <div className="bg-slate-800/50 border border-dashed border-slate-700 rounded-xl p-16 text-center">
            <div className="text-slate-500">No students found.</div>
          </div>
        )}

        {students.length > 0 && (
          <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-slate-900/50">
                <tr>
                  <th className="text-left px-4 py-3 text-xs uppercase tracking-wider text-slate-400 font-medium">ID</th>
                  <th className="text-left px-4 py-3 text-xs uppercase tracking-wider text-slate-400 font-medium">Name</th>
                  <th className="text-left px-4 py-3 text-xs uppercase tracking-wider text-slate-400 font-medium">Email</th>
                  <th className="text-left px-4 py-3 text-xs uppercase tracking-wider text-slate-400 font-medium">Year</th>
                  <th className="text-left px-4 py-3 text-xs uppercase tracking-wider text-slate-400 font-medium">Courses</th>
                  <th className="text-left px-4 py-3 text-xs uppercase tracking-wider text-slate-400 font-medium">Avg Attendance</th>
                </tr>
              </thead>
              <tbody>
                {students.map((s) => (
                  <tr key={s.id} className="border-t border-slate-700/50 hover:bg-slate-700/20 transition-colors">
                    <td className="px-4 py-3 text-slate-400 font-mono text-xs">{s.student_number}</td>
                    <td className="px-4 py-3 text-white font-medium">{s.first_name} {s.last_name}</td>
                    <td className="px-4 py-3 text-slate-300">{s.email}</td>
                    <td className="px-4 py-3 text-slate-300">{s.enrollment_year}</td>
                    <td className="px-4 py-3 text-slate-300">{s.total_courses}</td>
                    <td className="px-4 py-3">
                      <span className={`text-xs px-2 py-1 rounded border font-mono ${attendanceBadge(s.average_attendance)}`}>
                        {s.average_attendance}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="px-4 py-3 border-t border-slate-700 bg-slate-900/30 text-xs text-slate-500">
              Showing {students.length} student{students.length === 1 ? '' : 's'}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
