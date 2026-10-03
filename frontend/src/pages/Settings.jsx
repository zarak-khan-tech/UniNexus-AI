import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

// English: Settings page — lets admins change tenant-wide thresholds without code.
// Roman Urdu: Settings page — admin bina code ke tenant-wide thresholds change kar sakta hai.
export default function Settings() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // English: Local form state — mirrors the settings JSON from the backend.
  // Roman Urdu: Local form state — backend ke settings JSON ki copy.
  const [form, setForm] = useState({
    university_name: 'Demo University',
    attendance_threshold: 75,
    risk_high_threshold: 60,
    risk_medium_threshold: 75,
  });

  const fetchSettings = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get('/tenant/settings');
      const s = res.data.settings || {};
      setForm({
        university_name: s.university_name ?? 'Demo University',
        attendance_threshold: s.attendance_threshold ?? 75,
        risk_high_threshold: s.risk_high_threshold ?? 60,
        risk_medium_threshold: s.risk_medium_threshold ?? 75,
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load settings.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchSettings(); }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    const isNumeric = ['attendance_threshold', 'risk_high_threshold', 'risk_medium_threshold'].includes(name);
    setForm((prev) => ({ ...prev, [name]: isNumeric ? Number(value) : value }));
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setSuccess(null);
    try {
      await api.put('/tenant/settings', { settings: form });
      setSuccess('Settings saved successfully.');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save settings.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <Layout>
      <div className="p-8 max-w-3xl mx-auto animate-fade-in">
        {/* Header */}
        <div className="mb-8">
          <div className="inline-flex items-center gap-2 text-[11px] text-gold-700 font-bold uppercase tracking-widest mb-3">
            <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
            Configuration
          </div>
          <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">Settings</h1>
          <p className="text-ink-500 text-[15px] leading-relaxed">
            University-wide thresholds and defaults. Changes apply to all agents immediately.
          </p>
        </div>

        {loading && (
          <div className="bg-white border border-ink-200 rounded-2xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading settings…</div>
          </div>
        )}

        {!loading && (
          <form onSubmit={handleSave} className="bg-white border border-ink-200 rounded-2xl shadow-card overflow-hidden">
            {/* University Identity */}
            <div className="px-6 py-5 border-b border-ink-100">
              <h2 className="font-display text-lg font-bold text-ink-900 mb-1">University Identity</h2>
              <p className="text-xs text-ink-500">Shown in notifications and reports.</p>
            </div>
            <div className="px-6 py-5 border-b border-ink-100">
              <label className="block text-sm font-medium text-ink-700 mb-1.5">University Name</label>
              <input
                type="text"
                name="university_name"
                value={form.university_name}
                onChange={handleChange}
                className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100"
              />
            </div>

            {/* Thresholds */}
            <div className="px-6 py-5 border-b border-ink-100">
              <h2 className="font-display text-lg font-bold text-ink-900 mb-1">Thresholds</h2>
              <p className="text-xs text-ink-500">Agents use these values when they run.</p>
            </div>
            <div className="px-6 py-5 border-b border-ink-100 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-ink-700 mb-1.5">Attendance Threshold (%)</label>
                <input
                  type="number" min="0" max="100"
                  name="attendance_threshold"
                  value={form.attendance_threshold}
                  onChange={handleChange}
                  className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100"
                />
                <p className="text-[11px] text-ink-500 mt-1">Used by Attendance & Policy agents</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-ink-700 mb-1.5">Risk · High (%)</label>
                <input
                  type="number" min="0" max="100"
                  name="risk_high_threshold"
                  value={form.risk_high_threshold}
                  onChange={handleChange}
                  className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100"
                />
                <p className="text-[11px] text-ink-500 mt-1">Below this → High risk</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-ink-700 mb-1.5">Risk · Medium (%)</label>
                <input
                  type="number" min="0" max="100"
                  name="risk_medium_threshold"
                  value={form.risk_medium_threshold}
                  onChange={handleChange}
                  className="w-full bg-white border border-ink-200 rounded-lg px-3.5 py-2.5 text-ink-900 focus:outline-none focus:border-gold-400 focus:ring-4 focus:ring-gold-100"
                />
                <p className="text-[11px] text-ink-500 mt-1">Below this → Medium risk</p>
              </div>
            </div>

            {/* Feedback + Actions */}
            <div className="px-6 py-5 flex flex-wrap items-center gap-4">
              <button
                type="submit"
                disabled={saving}
                className="inline-flex items-center gap-2 gradient-gold text-ink-950 font-bold px-6 py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover hover:-translate-y-0.5 disabled:opacity-60 disabled:hover:translate-y-0"
              >
                {saving ? 'Saving…' : 'Save settings'}
              </button>
              <button
                type="button"
                onClick={fetchSettings}
                disabled={saving}
                className="text-sm text-ink-600 hover:text-ink-900 font-semibold transition-colors"
              >
                Reset
              </button>
              {success && (
                <span className="text-sm text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-lg px-3 py-1.5 inline-flex items-center gap-1.5">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                  </svg>
                  {success}
                </span>
              )}
              {error && (
                <span className="text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg px-3 py-1.5">
                  {error}
                </span>
              )}
            </div>
          </form>
        )}
      </div>
    </Layout>
  );
}
