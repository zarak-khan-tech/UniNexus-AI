import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

// English: Permission-level color identity — consistent across the platform.
// Roman Urdu: Permission-level color identity — pooray platform mein consistent.
const PERMISSION_META = {
  read: { label: 'Read', short: 'READ', bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200', dot: 'bg-blue-500' },
  write_low: { label: 'Write (Low Risk)', short: 'WRITE_LOW', bg: 'bg-amber-50', text: 'text-amber-800', border: 'border-amber-200', dot: 'bg-amber-500' },
  write_high: { label: 'Write (High Risk)', short: 'WRITE_HIGH', bg: 'bg-red-50', text: 'text-red-700', border: 'border-red-200', dot: 'bg-red-500' },
};

function permStyle(p) {
  return PERMISSION_META[p] || { label: p, short: p, bg: 'bg-ink-50', text: 'text-ink-700', border: 'border-ink-200', dot: 'bg-ink-500' };
}

// English: Category grouping for nicer UX.
// Roman Urdu: Behtar UX ke liye category grouping.
function groupTool(tool) {
  const n = tool.name;
  if (n === 'semantic_search') return 'Knowledge';
  if (n.startsWith('update_') || n.startsWith('send_')) return 'Actions';
  return 'Academic Data';
}

const GROUP_ICON = {
  'Academic Data': (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
  ),
  'Knowledge': (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" /></svg>
  ),
  'Actions': (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
  ),
};

export default function Tools() {
  const [tools, setTools] = useState([]);
  const [counts, setCounts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const fetchTools = async () => {
      try {
        const response = await api.get('/tools');
        setTools(response.data.tools || []);
        setCounts(response.data.counts || null);
      } catch (err) {
        console.error('Failed to fetch tools', err);
      } finally {
        setLoading(false);
      }
    };
    fetchTools();
  }, []);

  const filtered = tools.filter((t) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      t.name.toLowerCase().includes(q) ||
      t.description.toLowerCase().includes(q) ||
      t.permission.toLowerCase().includes(q)
    );
  });

  // English: Group tools by category for a cleaner layout.
  // Roman Urdu: Behtar layout ke liye tools ko category mein group karo.
  const grouped = filtered.reduce((acc, t) => {
    const g = groupTool(t);
    (acc[g] = acc[g] || []).push(t);
    return acc;
  }, {});

  return (
    <Layout>
      <div className="p-8 max-w-6xl mx-auto animate-fade-in">
        {/* Header */}
        <div className="mb-8">
          <div className="inline-flex items-center gap-2 text-[11px] text-gold-700 font-bold uppercase tracking-widest mb-3">
            <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
            Tool Registry
          </div>
          <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">Tools</h1>
          <p className="text-ink-500 text-[15px] leading-relaxed">
            Internal capability registry — these are the actions the AI can perform on your behalf.
            You don't need to interact with them directly; high-risk actions are automatically routed to the <span className="text-ink-800 font-semibold">Approvals</span> page.
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">Total Tools</div>
            <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">{loading ? '—' : counts?.total ?? tools.length}</div>
          </div>
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">Read-only</div>
            <div className="text-3xl font-display font-bold text-blue-700 tracking-tight">{loading ? '—' : counts?.read ?? 0}</div>
          </div>
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">Write (Low)</div>
            <div className="text-3xl font-display font-bold text-amber-700 tracking-tight">{loading ? '—' : counts?.write_low ?? 0}</div>
          </div>
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">Write (High)</div>
            <div className="text-3xl font-display font-bold text-red-700 tracking-tight">{loading ? '—' : counts?.write_high ?? 0}</div>
          </div>
        </div>

        {/* Search */}
        <div className="bg-white border border-ink-200 rounded-xl p-4 mb-6 shadow-card">
          <div className="relative">
            <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
            </svg>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search tools by name, description, or permission…"
              className="w-full bg-ink-50/50 border border-ink-200 rounded-lg pl-10 pr-4 py-2.5 text-ink-900 placeholder-ink-400 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100 transition-all"
            />
          </div>
        </div>

        {loading && (
          <div className="bg-white border border-ink-200 rounded-xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading tools…</div>
          </div>
        )}

        {!loading && filtered.length === 0 && (
          <div className="bg-white border-2 border-dashed border-ink-200 rounded-xl p-16 text-center">
            <div className="text-ink-500">{search ? 'No tools match your search.' : 'No tools registered.'}</div>
          </div>
        )}

        {!loading && Object.entries(grouped).map(([groupName, groupTools]) => (
          <div key={groupName} className="mb-8">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-ink-900 text-gold-300 flex items-center justify-center">
                {GROUP_ICON[groupName]}
              </div>
              <h2 className="font-display text-xl font-bold text-ink-900">{groupName}</h2>
              <span className="text-xs text-ink-500 font-mono ml-2">({groupTools.length})</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {groupTools.map((tool) => {
                const style = permStyle(tool.permission);
                const args = tool.input_schema?.properties || {};
                const required = tool.input_schema?.required || [];
                const argEntries = Object.entries(args);
                return (
                  <div key={tool.name} className="relative bg-white border border-ink-200 rounded-2xl p-6 shadow-card hover-lift transition-all overflow-hidden">
                    <div className={`absolute top-0 left-0 right-0 h-1 ${style.dot}`} />
                    <div className="flex items-start justify-between gap-3 mb-3">
                      <code className="text-sm font-mono font-bold text-ink-900 bg-ink-50 border border-ink-200 rounded-md px-2.5 py-1">
                        {tool.name}
                      </code>
                      <span className={`inline-flex items-center gap-1.5 text-[10px] uppercase tracking-widest font-bold px-2.5 py-1 rounded-full border ${style.bg} ${style.text} ${style.border} whitespace-nowrap`}>
                        <span className={`w-1.5 h-1.5 rounded-full ${style.dot}`}></span>
                        {style.short}
                      </span>
                    </div>
                    <p className="text-sm text-ink-600 leading-relaxed mb-4">{tool.description}</p>
                    {argEntries.length > 0 && (
                      <div className="pt-4 border-t border-ink-100">
                        <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-2">Arguments</div>
                        <div className="flex flex-wrap gap-1.5">
                          {argEntries.map(([argName, argMeta]) => {
                            const isReq = required.includes(argName);
                            return (
                              <span key={argName} className={`text-[11px] font-mono px-2 py-0.5 rounded border ${isReq ? 'bg-ink-900 text-gold-300 border-ink-900' : 'bg-ink-50 text-ink-600 border-ink-200'}`}>
                                {argName}
                                <span className="opacity-60">:{argMeta.type || 'any'}</span>
                                {isReq && <span className="ml-1 text-[9px] font-bold">REQ</span>}
                              </span>
                            );
                          })}
                        </div>
                      </div>
                    )}
                    {tool.permission === 'write_high' && (
                      <div className="mt-4 pt-3 border-t border-red-100 flex items-center gap-2 text-xs text-red-700">
                        <svg className="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M12 9v2m0 4h.01M5.07 19h13.86a2 2 0 001.71-3.01l-6.93-12a2 2 0 00-3.42 0l-6.93 12A2 2 0 005.07 19z" />
                        </svg>
                        <span>Requires human approval before execution.</span>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </Layout>
  );
}
