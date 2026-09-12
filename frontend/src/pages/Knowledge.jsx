import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import api from '../api/client';

const CATEGORY_COLORS = {
  Policy: 'bg-blue-500/15 text-blue-300 border-blue-500/40',
  Handbook: 'bg-purple-500/15 text-purple-300 border-purple-500/40',
  Regulation: 'bg-orange-500/15 text-orange-300 border-orange-500/40',
  Default: 'bg-slate-700 text-slate-300 border-slate-600',
};

function categoryColor(cat) {
  return CATEGORY_COLORS[cat] || CATEGORY_COLORS.Default;
}

export default function Knowledge() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await api.get('/academic/documents');
        setDocuments(response.data.documents);
      } catch (err) {
        console.error('Failed to fetch documents', err);
      } finally {
        setLoading(false);
      }
    };
    fetch();
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

  return (
    <Layout>
      <div className="p-8 max-w-6xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-white mb-2">Knowledge Base</h1>
          <p className="text-slate-400">
            University policies, handbooks, and regulations that the KnowledgeAgent retrieves from.
          </p>
        </div>

        {/* Search */}
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 mb-6">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search documents by title, category, or content..."
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
        </div>

        {loading && (
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-16 text-center">
            <div className="text-slate-500">Loading documents...</div>
          </div>
        )}

        {!loading && filtered.length === 0 && (
          <div className="bg-slate-800/50 border border-dashed border-slate-700 rounded-xl p-16 text-center">
            <div className="text-slate-500">
              {search ? 'No documents match your search.' : 'No documents in the knowledge base yet.'}
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map((doc) => (
            <div
              key={doc.id}
              className="bg-slate-800 border border-slate-700 rounded-xl p-6 hover:border-blue-500/40 transition-colors flex flex-col"
            >
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-semibold text-white text-lg flex-1">{doc.title}</h3>
                {doc.category && (
                  <span className={`text-xs px-2 py-0.5 rounded border ml-2 ${categoryColor(doc.category)}`}>
                    {doc.category}
                  </span>
                )}
              </div>
              <div className="text-sm text-slate-400 leading-relaxed mb-4 line-clamp-4 flex-1">
                {doc.content.length > 220 ? doc.content.slice(0, 220) + '…' : doc.content}
              </div>
              <div className="flex items-center justify-between pt-3 border-t border-slate-700/50">
                <button
                  onClick={() => setSelected(doc)}
                  className="text-xs text-blue-400 hover:text-blue-300 font-medium"
                >
                  View full content
                </button>
                <Link
                  to="/command-center"
                  className="text-xs text-slate-400 hover:text-slate-200"
                >
                  Try in Command Center →
                </Link>
              </div>
            </div>
          ))}
        </div>

        {/* Full content modal */}
        {selected && (
          <div
            className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50"
            onClick={() => setSelected(null)}
          >
            <div
              className="bg-slate-800 border border-slate-700 rounded-xl max-w-2xl w-full max-h-[85vh] overflow-hidden flex flex-col"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="px-6 py-4 border-b border-slate-700 flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-white">{selected.title}</h2>
                  {selected.category && (
                    <span className={`inline-block text-xs px-2 py-0.5 rounded border mt-1 ${categoryColor(selected.category)}`}>
                      {selected.category}
                    </span>
                  )}
                </div>
                <button
                  onClick={() => setSelected(null)}
                  className="text-slate-400 hover:text-white text-2xl leading-none"
                >
                  ×
                </button>
              </div>
              <div className="p-6 overflow-auto">
                <div className="text-sm text-slate-200 leading-relaxed whitespace-pre-wrap">
                  {selected.content}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
