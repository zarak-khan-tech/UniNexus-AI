import { useState, useRef } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

// English: Description of each import type — header fields + sample CSV.
// Roman Urdu: Har import type ki description — header fields + sample CSV.
const TABS = [
  {
    id: 'students',
    label: 'Students',
    endpoint: '/import/students',
    csvHeader: 'student_number,first_name,last_name,email,enrollment_year',
    sample: 'S201,Ali,Khan,ali.khan@demo.edu,2024',
  },
  {
    id: 'courses',
    label: 'Courses',
    endpoint: '/import/courses',
    csvHeader: 'course_code,title,credit_hours,department',
    sample: 'CS401,Advanced Algorithms,4,Computer Science',
  },
  {
    id: 'enrollments',
    label: 'Enrollments',
    endpoint: '/import/enrollments',
    csvHeader: 'student_number,course_code,grade,attendance_percentage',
    sample: 'S101,CS401,A,85',
  },
];

function ResultCard({ result, onDismiss }) {
  if (!result) return null;
  const hasErrors = (result.errors || []).length > 0;
  return (
    <div className={`border-2 rounded-2xl p-5 mt-4 shadow-card ${hasErrors ? 'bg-amber-50/60 border-amber-200' : 'bg-emerald-50/60 border-emerald-200'}`}>
      <div className="flex items-start justify-between gap-4 mb-3">
        <div className="flex items-start gap-3">
          <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${hasErrors ? 'bg-amber-100' : 'bg-emerald-100'}`}>
            {hasErrors ? (
              <svg className="w-5 h-5 text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01M5.07 19h13.86a2 2 0 001.71-3.01l-6.93-12a2 2 0 00-3.42 0l-6.93 12A2 2 0 005.07 19z" />
              </svg>
            ) : (
              <svg className="w-5 h-5 text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
              </svg>
            )}
          </div>
          <div>
            <div className="text-sm font-bold text-ink-900">Import complete</div>
            <div className="text-xs text-ink-600 mt-0.5">{result.summary}</div>
          </div>
        </div>
        <button onClick={onDismiss} className="text-xs text-ink-500 hover:text-ink-900 font-semibold">Dismiss</button>
      </div>

      <div className="grid grid-cols-3 gap-3 mb-3">
        <div className="bg-white border border-ink-200 rounded-lg p-3">
          <div className="text-[10px] uppercase tracking-wider text-ink-500 font-bold mb-0.5">Added</div>
          <div className="text-2xl font-display font-bold text-emerald-700">{result.added}</div>
        </div>
        <div className="bg-white border border-ink-200 rounded-lg p-3">
          <div className="text-[10px] uppercase tracking-wider text-ink-500 font-bold mb-0.5">Skipped</div>
          <div className="text-2xl font-display font-bold text-amber-700">{result.skipped}</div>
        </div>
        <div className="bg-white border border-ink-200 rounded-lg p-3">
          <div className="text-[10px] uppercase tracking-wider text-ink-500 font-bold mb-0.5">Errors</div>
          <div className="text-2xl font-display font-bold text-red-700">{(result.errors || []).length}</div>
        </div>
      </div>

      {hasErrors && (
        <div>
          <div className="text-[10px] uppercase tracking-wider text-ink-600 font-bold mb-1.5">Row issues</div>
          <ul className="text-xs text-ink-700 bg-white border border-ink-200 rounded-lg p-3 space-y-1 max-h-40 overflow-auto font-mono">
            {result.errors.map((e, i) => <li key={i}>• {e}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}

export default function Import() {
  const [activeTab, setActiveTab] = useState('students');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const tab = TABS.find((t) => t.id === activeTab);

  const handleFileChange = (e) => {
    const f = e.target.files?.[0];
    setFile(f || null);
    setError(null);
    setResult(null);
  };

  const handleUpload = async () => {
    if (!file || !tab) return;
    setUploading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await api.post(tab.endpoint, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
    } catch (err) {
      setError(err.response?.data?.detail || 'Import failed.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <Layout>
      <div className="p-8 max-w-4xl mx-auto animate-fade-in">
        {/* Header */}
        <div className="mb-8">
          <div className="inline-flex items-center gap-2 text-[11px] text-gold-700 font-bold uppercase tracking-widest mb-3">
            <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
            Data Onboarding
          </div>
          <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">Import</h1>
          <p className="text-ink-500 text-[15px] leading-relaxed max-w-2xl">
            Bulk-upload students, courses, and enrollments from CSV files. Duplicates are skipped; invalid rows are reported.
          </p>
        </div>

        {/* Tabs */}
        <div className="inline-flex items-center gap-1 p-1 bg-ink-100 border border-ink-200 rounded-xl mb-6 shadow-inset-soft">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => { setActiveTab(t.id); setFile(null); setResult(null); setError(null); if (fileInputRef.current) fileInputRef.current.value = ''; }}
              className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
                activeTab === t.id
                  ? 'bg-ink-900 text-white shadow-card'
                  : 'text-ink-600 hover:text-ink-900 hover:bg-white'
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {/* Upload Card */}
        <div className="bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden">
          <div className="px-6 py-5 border-b border-ink-100">
            <h2 className="font-display text-lg font-bold text-ink-900 mb-1">Upload {tab?.label} CSV</h2>
            <p className="text-xs text-ink-500">First row must be the header. Duplicates (by ID/email) are skipped automatically.</p>
          </div>

          <div className="p-6 space-y-4">
            {/* Expected header */}
            <div className="bg-ink-50/60 border border-ink-100 rounded-lg p-3">
              <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1.5">Expected header</div>
              <code className="text-xs text-ink-800 font-mono break-all">{tab?.csvHeader}</code>
              <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mt-3 mb-1.5">Sample row</div>
              <code className="text-xs text-ink-600 font-mono break-all">{tab?.sample}</code>
            </div>

            {/* File picker */}
            <div>
              <label className="block text-sm font-medium text-ink-700 mb-1.5">CSV file</label>
              <input
                ref={fileInputRef}
                type="file"
                accept=".csv,text/csv"
                onChange={handleFileChange}
                className="block w-full text-sm text-ink-700 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:font-semibold file:bg-ink-900 file:text-white hover:file:bg-ink-800 file:cursor-pointer cursor-pointer border border-ink-200 rounded-lg bg-white"
              />
              {file && (
                <div className="text-xs text-ink-500 mt-1.5">
                  Selected: <span className="font-mono text-ink-700">{file.name}</span> ({(file.size / 1024).toFixed(1)} KB)
                </div>
              )}
            </div>

            {/* Upload button */}
            <button
              onClick={handleUpload}
              disabled={!file || uploading}
              className="inline-flex items-center gap-2 gradient-gold text-ink-950 font-bold px-6 py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover hover:-translate-y-0.5 disabled:opacity-60 disabled:hover:translate-y-0"
            >
              {uploading ? (
                <><span className="inline-block w-4 h-4 border-2 border-ink-950/30 border-t-ink-950 rounded-full animate-spin"></span>Uploading…</>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M12 4v12m0 0l-4-4m4 4l4-4" />
                  </svg>
                  Upload &amp; Import
                </>
              )}
            </button>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm font-medium">{error}</div>
            )}

            <ResultCard result={result} onDismiss={() => setResult(null)} />
          </div>
        </div>
      </div>
    </Layout>
  );
}
