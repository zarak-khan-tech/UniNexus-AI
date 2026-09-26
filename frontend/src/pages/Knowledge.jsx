import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

// English: Category color identity — matches the visual language used across the platform.
// Roman Urdu: Category ka rang — pooray platform ke visual language se match karta hai.
const CATEGORY_COLORS = {
  Policy:     { bg: 'bg-blue-50',   text: 'text-blue-700',   border: 'border-blue-200',   dot: 'bg-blue-500' },
  Handbook:   { bg: 'bg-violet-50', text: 'text-violet-700', border: 'border-violet-200', dot: 'bg-violet-500' },
  Regulation: { bg: 'bg-amber-50',  text: 'text-amber-800',  border: 'border-amber-200',  dot: 'bg-amber-500' },
};

function categoryStyle(cat) {
  return CATEGORY_COLORS[cat] || { bg: 'bg-ink-50', text: 'text-ink-700', border: 'border-ink-200', dot: 'bg-ink-500' };
}

export default function Knowledge() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    const fetchDocs = async () => {
      try {
        const response = await api.get('/academic/documents');
        setDocuments(response.data.documents);
      } catch (err) {
        console.error('Failed to fetch documents', err);
      } finally {
        setLoading(false);
      }
    };
    fetchDocs();
  }, []);

  const filtered = documents.filter((d) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      d.title.toLowerCase().includes(q) ||
      (d.category || '').toLowerCase().includes(q) ||
      d.content.toLowerCase().includes(q)
    );
  });

  const totalDocs = documents.length;
  const categories = new Set(documents.map((d) => d.category).filter(Boolean)).size;

  return (
    <Layout>
      <div className="p-8 max-w-6xl mx-auto animate-fade-in">
        {/* ==================== Header ==================== */}
        <div className="mb-8">
          <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">
            Knowledge Base
          </h1>
          <p className="text-ink-500 text-[15px] leading-relaxed">
            University policies, handbooks, and regulations that the KnowledgeAgent retrieves from.
          </p>
        </div>

        {/* ==================== Summary Cards ==================== */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">
              Total Documents
            </div>
            <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">
              {loading ? '—' : totalDocs}
            </div>
          </div>
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">
              Categories
            </div>
            <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">
              {loading ? '—' : categories}
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
              placeholder="Search documents by title, category, or content…"
              className="w-full bg-ink-50/50 border border-ink-200 rounded-lg pl-10 pr-4 py-2.5 text-ink-900 placeholder-ink-400 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100 transition-all"
            />
          </div>
        </div>

        {/* ==================== Loading ==================== */}
        {loading && (
          <div className="bg-white border border-ink-200 rounded-xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading documents…</div>
          </div>
        )}

        {/* ==================== Empty ==================== */}
        {!loading && filtered.length === 0 && (
          <div className="bg-white border-2 border-dashed border-ink-200 rounded-xl p-16 text-center">
            <div className="text-ink-500">
              {search ? 'No documents match your search.' : 'No documents in the knowledge base yet.'}
            </div>
          </div>
        )}

        {/* ==================== Cards ==================== */}
        {!loading && filtered.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filtered.map((doc) => {
              const style = categoryStyle(doc.category);
              return (
                <div
                  key={doc.id}
                  className="relative bg-white border border-ink-200 rounded-xl p-6 shadow-card hover-lift transition-all overflow-hidden flex flex-col"
                >
                  <div className={`absolute top-0 left-0 right-0 h-1 ${style.dot}`} />

                  <div className="flex items-start justify-between gap-3 mb-3">
                    <h3 className="font-display font-bold text-ink-900 text-lg leading-tight flex-1">
                      {doc.title}
                    </h3>
                    {doc.category && (
                      <span className={`text-[10px] uppercase tracking-widest font-bold px-2.5 py-1 rounded-full border ${style.bg} ${style.text} ${style.border} whitespace-nowrap`}>
                        {doc.category}
                      </span>
                    )}
                  </div>

                  <p className="text-sm text-ink-600 leading-relaxed mb-5 flex-1">
                    {doc.content.length > 220 ? doc.content.slice(0, 220) + '…' : doc.content}
                  </p>

                  <div className="pt-4 border-t border-ink-100">
                    <button
                      onClick={() => setSelected(doc)}
                      className="inline-flex items-center gap-1.5 text-xs font-semibold text-ink-900 hover:text-gold-700 transition-colors"
                    >
                      View full content
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* ==================== Modal ==================== */}
        {selected && (
          <div
            className="fixed inset-0 bg-ink-950/70 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in"
            onClick={() => setSelected(null)}
          >
            <div
              className="bg-white border border-ink-200 rounded-2xl max-w-2xl w-full max-h-[85vh] overflow-hidden flex flex-col shadow-float"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="px-6 py-4 border-b border-ink-200 flex items-start justify-between gap-4">
                <div className="flex-1">
                  <h2 className="font-display text-xl font-bold text-ink-900 mb-1">
                    {selected.title}
                  </h2>
                  {selected.category && (() => {
                    const style = categoryStyle(selected.category);
                    return (
                      <span className={`inline-block text-[10px] uppercase tracking-widest font-bold px-2.5 py-1 rounded-full border ${style.bg} ${style.text} ${style.border}`}>
                        {selected.category}
                      </span>
                    );
                  })()}
                </div>
                <button
                  onClick={() => setSelected(null)}
                  className="text-ink-400 hover:text-ink-900 transition-colors text-2xl leading-none w-8 h-8 flex items-center justify-center"
                >
                  ×
                </button>
              </div>
              <div className="p-6 overflow-y-auto">
                <p className="text-[15px] text-ink-800 leading-relaxed whitespace-pre-wrap">
                  {selected.content}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
