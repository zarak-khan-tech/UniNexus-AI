import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';

// English: Global search — icon opens a dropdown; typing debounced-hits the 
// backend; clicking a result navigates.
// Roman Urdu: Global search — icon dropdown kholta hai; typing debounced 
// backend call karti hai; result click pe navigate.
export default function SearchBox() {
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef(null);
  const wrapRef = useRef(null);
  const navigate = useNavigate();

  // English: Close dropdown on outside click.
  // Roman Urdu: Bahar click pe dropdown band.
  useEffect(() => {
    const handler = (e) => {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  // English: Focus input when dropdown opens.
  // Roman Urdu: Dropdown khulne pe input focus karo.
  useEffect(() => {
    if (open && inputRef.current) inputRef.current.focus();
  }, [open]);

  // English: Debounced search — 300ms after typing stops.
  // Roman Urdu: Debounced search — typing rukne ke 300ms baad.
  useEffect(() => {
    if (!q.trim() || q.trim().length < 2) {
      setResults(null);
      return;
    }
    setLoading(true);
    const t = setTimeout(async () => {
      try {
        const res = await api.get(`/search?q=${encodeURIComponent(q.trim())}`);
        setResults(res.data);
      } catch (err) {
        setResults(null);
      } finally {
        setLoading(false);
      }
    }, 300);
    return () => clearTimeout(t);
  }, [q]);

  const goTo = (url) => {
    setOpen(false);
    setQ('');
    setResults(null);
    navigate(url);
  };

  const sections = results ? [
    { key: 'students', label: 'Students', items: results.students || [], render: (s) => ({ primary: s.name, secondary: s.student_number + ' · ' + s.email }) },
    { key: 'courses', label: 'Courses', items: results.courses || [], render: (c) => ({ primary: `${c.course_code} — ${c.title}`, secondary: c.department }) },
    { key: 'documents', label: 'Documents', items: results.documents || [], render: (d) => ({ primary: d.title, secondary: d.category }) },
    { key: 'agents', label: 'Agents', items: results.agents || [], render: (a) => ({ primary: a.name, secondary: a.description }) },
    { key: 'tools', label: 'Tools', items: results.tools || [], render: (t) => ({ primary: t.name, secondary: t.description }) },
  ] : [];

  const anyResults = sections.some((s) => s.items.length > 0);

  return (
    <div className="relative" ref={wrapRef}>
      <button
        onClick={() => setOpen((v) => !v)}
        className="p-2 rounded-lg hover:bg-ink-50 transition-colors"
        title="Search (Ctrl+K)"
      >
        <svg className="w-5 h-5 text-ink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
        </svg>
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-[420px] bg-white border border-ink-200 rounded-xl shadow-float z-30 overflow-hidden animate-slide-up">
          <div className="px-3 py-2.5 border-b border-ink-100 bg-ink-50/60">
            <div className="relative">
              <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
              </svg>
              <input
                ref={inputRef}
                type="text"
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder="Search students, courses, docs, agents, tools…"
                className="w-full bg-white border border-ink-200 rounded-lg pl-9 pr-3 py-2 text-sm text-ink-900 placeholder-ink-400 focus:outline-none focus:border-gold-400 focus:ring-2 focus:ring-gold-100"
              />
            </div>
          </div>

          <div className="max-h-96 overflow-y-auto">
            {!q.trim() && (
              <div className="p-8 text-center text-xs text-ink-500">
                Type at least 2 characters to search across the platform.
              </div>
            )}
            {q.trim() && q.trim().length < 2 && (
              <div className="p-8 text-center text-xs text-ink-500">Keep typing…</div>
            )}
            {loading && q.trim().length >= 2 && (
              <div className="p-6 text-center text-xs text-ink-500">Searching…</div>
            )}
            {!loading && results && !anyResults && (
              <div className="p-8 text-center text-xs text-ink-500">
                No results for “{q}”.
              </div>
            )}
            {!loading && results && sections.map((sec) => {
              if (sec.items.length === 0) return null;
              return (
                <div key={sec.key} className="border-b border-ink-100 last:border-b-0">
                  <div className="px-4 py-1.5 text-[10px] uppercase tracking-widest text-ink-500 font-bold bg-ink-50/40">
                    {sec.label}
                  </div>
                  {sec.items.map((it, idx) => {
                    const { primary, secondary } = sec.render(it);
                    return (
                      <button
                        key={`${sec.key}-${idx}`}
                        onClick={() => goTo(it.url)}
                        className="w-full text-left px-4 py-2.5 hover:bg-ink-50 transition-colors"
                      >
                        <div className="text-sm font-medium text-ink-900 truncate">{primary}</div>
                        {secondary && <div className="text-xs text-ink-500 truncate">{secondary}</div>}
                      </button>
                    );
                  })}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
