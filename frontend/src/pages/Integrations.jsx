import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

// English: Visual identity for integration statuses. Honest labels — no fake "connected".
// Roman Urdu: Integration statuses ki visual identity. Honest labels — koi fake "connected" nahi.
const STATUS_META = {
  implemented: {
    label: 'Live',
    bg: 'bg-emerald-50',
    text: 'text-emerald-700',
    border: 'border-emerald-200',
    dot: 'bg-emerald-500',
    hint: 'Connected to a real external system.',
  },
  locally_simulated: {
    label: 'Simulated',
    bg: 'bg-blue-50',
    text: 'text-blue-700',
    border: 'border-blue-200',
    dot: 'bg-blue-500',
    hint: 'Locally simulated for demonstration.',
  },
  architecture_ready: {
    label: 'Architecture Ready',
    bg: 'bg-amber-50',
    text: 'text-amber-800',
    border: 'border-amber-200',
    dot: 'bg-amber-500',
    hint: 'Interface ready. Configure credentials to activate.',
  },
  planned: {
    label: 'Planned',
    bg: 'bg-ink-50',
    text: 'text-ink-700',
    border: 'border-ink-200',
    dot: 'bg-ink-400',
    hint: 'Documented, not yet built.',
  },
};

function statusStyle(status) {
  return STATUS_META[status] || STATUS_META.planned;
}

function IntegrationCard({ integration, onTest }) {
  const meta = statusStyle(integration.status);
  const [testing, setTesting] = useState(false);
  const [result, setResult] = useState(null);

  const handleTest = async () => {
    setTesting(true);
    setResult(null);
    try {
      const res = await onTest(integration.name);
      setResult(res);
    } catch (err) {
      setResult({ ok: false, message: err.response?.data?.detail || 'Test failed.' });
    } finally {
      setTesting(false);
    }
  };

  return (
    <div className="relative bg-white border border-ink-200 rounded-2xl p-6 shadow-card hover:lift transition-all overflow-hidden">
      <div className={`absolute top-0 left-0 right-0 h-1 ${meta.dot}`} />

      <div className="flex items-start justify-between gap-4 mb-3">
        <div className="min-w-0">
          <h3 className="font-display font-bold text-ink-900 text-lg leading-tight">
            {integration.display_name}
          </h3>
          <div className="text-xs text-ink-500 font-mono mt-0.5">
            {integration.name}
          </div>
        </div>
        <span className={`inline-flex items-center gap-1.5 text-[10px] uppercase tracking-widest font-bold px-2.5 py-1 rounded-full border whitespace-nowrap ${meta.bg} ${meta.text} ${meta.border}`}>
          <span className={`w-1.5 h-1.5 rounded-full ${meta.dot}`} />
          {meta.label}
        </span>
      </div>

      <p className="text-sm text-ink-600 leading-relaxed mb-4">
        {integration.description}
      </p>

      <div className="text-xs text-ink-500 italic mb-4">{meta.hint}</div>

      {integration.capabilities && integration.capabilities.length > 0 && (
        <div className="mb-4">
          <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-1.5">
            Capabilities
          </div>
          <div className="flex flex-wrap gap-1.5">
            {integration.capabilities.map((c) => (
              <span
                key={c}
                className="text-[11px] font-mono px-2 py-0.5 rounded bg-ink-50 text-ink-600 border border-ink-200"
              >
                {c}
              </span>
            ))}
          </div>
        </div>
      )}

      {integration.requires_credentials && (
        <div className="text-[11px] text-amber-700 mb-4 flex items-center gap-1.5">
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          Credentials required to activate
        </div>
      )}

      <div className="pt-4 border-t border-ink-100">
        <button
          onClick={handleTest}
          disabled={testing}
          className="inline-flex items-center gap-2 text-xs font-semibold text-ink-900 hover:text-gold-700 transition-colors disabled:opacity-50"
        >
          {testing ? (
            <>
              <span className="inline-block w-3 h-3 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin" />
              Testing…
            </>
          ) : (
            <>
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Test Connection
            </>
          )}
        </button>

        {result && (
          <div
            className={`mt-3 rounded-lg p-3 text-xs ${
              result.ok
                ? 'bg-emerald-50 border border-emerald-200 text-emerald-700'
                : 'bg-amber-50 border border-amber-200 text-amber-800'
            }`}
          >
            {result.message}
          </div>
        )}
      </div>
    </div>
  );
}

export default function Integrations() {
  const [integrations, setIntegrations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchIntegrations = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get('/integrations');
      setIntegrations(res.data.integrations || []);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load integrations.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIntegrations();
  }, []);

  const testIntegration = async (name) => {
    const res = await api.post(`/integrations/${name}/test`);
    return res.data;
  };

  return (
    <Layout>
      <div className="p-8 max-w-6xl mx-auto animate-fade-in">
        {/* Header */}
        <div className="mb-8">
          <div className="inline-flex items-center gap-2 text-[11px] text-gold-700 font-bold uppercase tracking-widest mb-3">
            <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
            External Systems
          </div>
          <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">
            Integrations
          </h1>
          <p className="text-ink-500 text-[15px] leading-relaxed max-w-2xl">
            Adapters for external university systems. Each integration reports its
            honest status — we never claim a live connection without real credentials
            and a working backend.
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 mb-6 text-sm font-medium">
            {error}
          </div>
        )}

        {loading && (
          <div className="bg-white border border-ink-200 rounded-2xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3" />
            <div className="text-ink-500 text-sm">Loading integrations…</div>
          </div>
        )}

        {!loading && integrations.length === 0 && (
          <div className="bg-white border-2 border-dashed border-ink-200 rounded-2xl p-16 text-center">
            <div className="text-ink-500">No integrations registered.</div>
          </div>
        )}

        {!loading && integrations.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {integrations.map((i) => (
              <IntegrationCard
                key={i.name}
                integration={i}
                onTest={testIntegration}
              />
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}
