import { useEffect, useState, useRef } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

// English: Category color identity — matches the visual language used across 
// the platform.
// Roman Urdu: Category ka rang — pooray platform ke visual language se match 
// karta hai.
const CATEGORY_COLORS = {
  Policy: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200', dot: 'bg-blue-500' },
  Handbook: { bg: 'bg-violet-50', text: 'text-violet-700', border: 'border-violet-200', dot: 'bg-violet-500' },
  Regulation: { bg: 'bg-amber-50', text: 'text-amber-800', border: 'border-amber-200', dot: 'bg-amber-500' },
};
function categoryStyle(cat) {
  return CATEGORY_COLORS[cat] || { bg: 'bg-ink-50', text: 'text-ink-700', border: 'border-ink-200', dot: 'bg-ink-500' };
}

export default function Knowledge() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState(null);
  const [userRole, setUserRole] = useState('');

  // Upload modal state
  const [showUpload, setShowUpload] = useState(false);
  const [uploadTitle, setUploadTitle] = useState('');
  const [uploadCategory, setUploadCategory] = useState('Policy');
  const [uploadFile, setUploadFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadMsg, setUploadMsg] = useState(null);
  const fileInputRef = useRef(null);

  const fetchDocs = async () => {
    setLoading(true);
    try {
      const response = await api.get('/academic/documents');
      setDocuments(response.data.documents);
    } catch (err) {
      console.error('Failed to fetch documents', err);
    } finally {
      setLoading(false);
    }
  };

  // English: Fetch current user's role so we can show admin-only actions.
  // Roman Urdu: Current user ka role laao taake admin-only actions dikhayein.
  useEffect(() => {
    fetchDocs();
    (async () => {
      try {
        const res = await api.get('/auth/me');
        setUserRole((res.data.role || '').toLowerCase());
      } catch (err) { /* ignore */ }
    })();
  }, []);

  const isAdmin = userRole === 'admin' || userRole === 'super_admin';

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!uploadFile || !uploadTitle.trim()) {
      setUploadMsg({ type: 'error', text: 'Title and file are required.' });
      return;
    }
    setUploading(true);
    setUploadMsg(null);
    try {
      const formData = new FormData();
      formData.append('file', uploadFile);
      formData.append('title', uploadTitle.trim());
      formData.append('category', uploadCategory);
      const res = await api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setUploadMsg({
        type: 'success',
        text: `Uploaded "${res.data.title}" — ${res.data.embedded_chunks} chunk(s) embedded.`,
      });
      setUploadTitle('');
      setUploadFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      await fetchDocs();
    } catch (err) {
      setUploadMsg({
        type: 'error',
        text: err.response?.data?.detail || 'Upload failed.',
      });
    } finally {
      setUploading(false);
    }
  };

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
        {/* Header */}
        <div className="mb-8 flex flex-wrap items-start justify-between gap-4">
          <div>
            <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">
              Knowledge Base
            </h1>
            <p className="text-ink-500 text-[15px] leading-relaxed">
              University policies, handbooks, and regulations that the KnowledgeAgent retrieves from.
            </p>
          </div>
          {isAdmin && (
            <button
              onClick={() => { setShowUpload(true); setUploadMsg(null); }}
              className="inline-flex items-center gap-2 gradient-gold text-ink-950 font-bold px-5 py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover hover:-translate-y-0.5"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Upload Document
            </button>
          )}
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">Total Documents</div>
            <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">
              {loading ? '—' : totalDocs}
            </div>
          </div>
          <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
            <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">Categories</div>
            <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">
              {loading ? '—' : categories}
            </div>
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
              placeholder="Search documents by title, category, or content…"
              className="w-full bg-ink-50/50 border border-ink-200 rounded-lg pl-10 pr-4 py-2.5 text-ink-900 placeholder-ink-400 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100 transition-all"
            />
          </div>
        </div>

        {/* Loading */}
        {loading && (
          <div className="bg-white border border-ink-200 rounded-xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading documents…</div>
          </div>
        )}

        {/* Empty */}
        {!loading && filtered.length === 0 && (
          <div className="bg-white border-2 border-dashed border-ink-200 rounded-xl p-16 text-center">
            <div className="text-ink-500">
              {search ? 'No documents match your search.' : 'No documents in the knowledge base yet.'}
            </div>
          </div>
        )}

        {/* Cards */}
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

        {/* Full content modal */}
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

        {/* Upload modal (admin only) */}
        {showUpload && isAdmin && (
          <div
            className="fixed inset-0 bg-ink-950/70 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in"
            onClick={() => setShowUpload(false)}
          >
            <div
              className="bg-white border border-ink-200 rounded-2xl max-w-lg w-full shadow-float"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="px-6 py-4 border-b border-ink-200 flex items-center justify-between">
                <div>
                  <h2 className="font-display text-xl font-bold text-ink-900">Upload Document</h2>
                  <p className="text-xs text-ink-500 mt-0.5">Accepts .txt, .md, or .pdf (max 2 MB)</p>
                </div>
                <button
                  onClick={() => setShowUpload(false)}
                  className="text-ink-400 hover:text-ink-900 text-2xl leading-none w-8 h-8 flex items-center justify-center"
                >
                  ×
                </button>
              </div>
              <form onSubmit={handleUpload} className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-ink-700 mb-1.5">Title</label>
                  <input
                    type="text"
                    value={uploadTitle}
                    onChange={(e) => setUploadTitle(e.target.value)}
                    placeholder="e.g. Scholarship Renewal Policy 2026"
                    className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-ink-700 mb-1.5">Category</label>
                  <select
                    value={uploadCategory}
                    onChange={(e) => setUploadCategory(e.target.value)}
                    className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100"
                  >
                    <option value="Policy">Policy</option>
                    <option value="Handbook">Handbook</option>
                    <option value="Regulation">Regulation</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-ink-700 mb-1.5">File</label>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".txt,.md,.pdf"
                    onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                    className="block w-full text-sm text-ink-700 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:font-semibold file:bg-ink-900 file:text-white hover:file:bg-ink-800 file:cursor-pointer cursor-pointer border border-ink-200 rounded-lg bg-white"
                    required
                  />
                  {uploadFile && (
                    <div className="text-xs text-ink-500 mt-1.5">
                      Selected: <span className="font-mono text-ink-700">{uploadFile.name}</span> ({(uploadFile.size / 1024).toFixed(1)} KB)
                    </div>
                  )}
                </div>

                {uploadMsg && (
                  <div className={`rounded-lg p-3 text-sm font-medium ${uploadMsg.type === 'success' ? 'bg-emerald-50 border border-emerald-200 text-emerald-700' : 'bg-red-50 border border-red-200 text-red-700'}`}>
                    {uploadMsg.text}
                  </div>
                )}

                <div className="flex items-center gap-3 pt-2">
                  <button
                    type="submit"
                    disabled={uploading}
                    className="inline-flex items-center gap-2 gradient-gold text-ink-950 font-bold px-5 py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover hover:-translate-y-0.5 disabled:opacity-60 disabled:hover:translate-y-0"
                  >
                    {uploading ? (
                      <>
                        <span className="inline-block w-4 h-4 border-2 border-ink-950/30 border-t-ink-950 rounded-full animate-spin"></span>
                        Uploading…
                      </>
                    ) : 'Upload'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowUpload(false)}
                    className="text-sm text-ink-600 hover:text-ink-900 font-semibold px-4 py-2.5"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
