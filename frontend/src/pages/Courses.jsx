import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

const DEPT_COLORS = {
  'Computer Science': { text: 'text-blue-700', border: 'border-blue-200', dot: 'bg-blue-500' },
  'Mathematics':      { text: 'text-violet-700', border: 'border-violet-200', dot: 'bg-violet-500' },
  'Physics':          { text: 'text-emerald-700', border: 'border-emerald-200', dot: 'bg-emerald-500' },
  'English':          { text: 'text-amber-800', border: 'border-amber-200', dot: 'bg-amber-500' },
  'Statistics':       { text: 'text-rose-700', border: 'border-rose-200', dot: 'bg-rose-500' },
};

function deptStyle(dept) {
  return DEPT_COLORS[dept] || { text: 'text-ink-700', border: 'border-ink-200', dot: 'bg-ink-500' };
}

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await api.get('/academic/courses');
        setCourses(response.data.courses);
      } catch (err) {
        console.error('Failed to fetch courses', err);
      } finally {
        setLoading(false);
      }
    };
    fetchCourses();
  }, []);

  const filtered = courses.filter((c) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      c.course_code.toLowerCase().includes(q) ||
      c.title.toLowerCase().includes(q) ||
      c.department.toLowerCase().includes(q)
    );
  });

  const totalCourses = courses.length;
  const totalEnrollments = courses.reduce((sum, c) => sum + (c.enrolled_students || 0), 0);
  const departments = new Set(courses.map((c) => c.department)).size;

  return (
    <Layout>
      <div className="p-8 max-w-6xl mx-auto animate-fade-in">
        <div className="mb-8">
          <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">Courses</h1>
          <p className="text-ink-500 text-[15px] leading-relaxed">
            All courses offered at your institution, with live enrollment data.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">Total Courses</div>
            <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">
              {loading ? '—' : totalCourses}
            </div>
          </div>
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">Total Enrollments</div>
            <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">
              {loading ? '—' : totalEnrollments}
            </div>
          </div>
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">Departments</div>
            <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">
              {loading ? '—' : departments}
            </div>
          </div>
        </div>

        <div className="bg-white border border-ink-200 rounded-xl p-4 mb-6 shadow-card">
          <div className="relative">
            <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
            </svg>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by course code, title, or department…"
              className="w-full bg-ink-50/50 border border-ink-200 rounded-lg pl-10 pr-4 py-2.5 text-ink-900 placeholder-ink-400 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100 transition-all"
            />
          </div>
        </div>

        {loading && (
          <div className="bg-white border border-ink-200 rounded-xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading courses…</div>
          </div>
        )}

        {!loading && filtered.length === 0 && (
          <div className="bg-white border-2 border-dashed border-ink-200 rounded-xl p-16 text-center">
            <div className="text-ink-500">
              {search ? 'No courses match your search.' : 'No courses found.'}
            </div>
          </div>
        )}

        {!loading && filtered.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filtered.map((c) => {
              const style = deptStyle(c.department);
              return (
                <div key={c.id} className="relative bg-white border border-ink-200 rounded-xl p-6 shadow-card hover-lift transition-all overflow-hidden">
                  <div className={`absolute top-0 left-0 right-0 h-1 ${style.dot}`} />
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <div className="font-mono text-xs text-ink-500 mb-1">{c.course_code}</div>
                      <h3 className="font-display font-bold text-ink-900 text-lg leading-tight">{c.title}</h3>
                    </div>
                    <span className="text-[11px] px-2.5 py-1 rounded-full bg-ink-100 text-ink-700 font-semibold border border-ink-200 whitespace-nowrap">
                      {c.credit_hours} credits
                    </span>
                  </div>
                  <div className="flex items-center gap-2 mb-5">
                    <span className={`inline-block w-1.5 h-1.5 rounded-full ${style.dot}`}></span>
                    <span className={`text-xs font-semibold ${style.text}`}>{c.department}</span>
                  </div>
                  <div className="pt-4 border-t border-ink-100 flex items-center justify-between">
                    <div className="flex items-center gap-2 text-ink-600">
                      <svg className="w-4 h-4 text-ink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                      </svg>
                      <span className="text-sm">
                        <span className="font-bold text-ink-900">{c.enrolled_students}</span>
                        <span className="text-ink-500"> enrolled</span>
                      </span>
                    </div>
                    <div className="text-[11px] uppercase tracking-widest text-ink-400 font-bold">
                      {c.enrolled_students >= 10 ? 'Popular' : c.enrolled_students >= 5 ? 'Active' : 'Open'}
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
