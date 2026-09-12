import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await api.get('/academic/courses');
        setCourses(response.data.courses);
      } catch (err) {
        console.error('Failed to fetch courses', err);
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
          <h1 className="text-3xl font-bold text-white mb-2">Courses</h1>
          <p className="text-slate-400">
            All courses offered at your institution.
          </p>
        </div>

        {loading && (
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-16 text-center">
            <div className="text-slate-500">Loading courses...</div>
          </div>
        )}

        {!loading && courses.length === 0 && (
          <div className="bg-slate-800/50 border border-dashed border-slate-700 rounded-xl p-16 text-center">
            <div className="text-slate-500">No courses found.</div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {courses.map((c) => (
            <div key={c.id} className="bg-slate-800 border border-slate-700 rounded-xl p-6 hover:border-blue-500/40 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="font-mono text-xs text-blue-300 mb-1">{c.course_code}</div>
                  <h3 className="font-semibold text-white text-lg">{c.title}</h3>
                </div>
                <span className="text-xs px-2 py-0.5 rounded bg-slate-700 text-slate-300">
                  {c.credit_hours} credits
                </span>
              </div>
              <div className="text-sm text-slate-400 mb-4">{c.department}</div>
              <div className="flex items-center gap-4 pt-3 border-t border-slate-700/50 text-xs">
                <div>
                  <div className="text-slate-500 mb-0.5">Enrolled</div>
                  <div className="text-slate-100 font-medium">{c.enrolled_students} student{c.enrolled_students === 1 ? '' : 's'}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
}
