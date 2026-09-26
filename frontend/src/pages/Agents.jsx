import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import api from '../api/client';

// English: Per-agent visual identity — matches the Command Center colors.
// Roman Urdu: Har agent ka rang — Command Center ke saath consistent.
const AGENT_META = {
  AttendanceAgent: {
    label: 'Attendance',
    description: 'Finds students with low attendance',
    color: 'bg-blue-500',
    lightBg: 'bg-blue-50',
    text: 'text-blue-700',
    border: 'border-blue-200',
    iconBg: 'bg-blue-100',
  },
  PolicyAgent: {
    label: 'Policy',
    description: 'Returns institutional policy rules and thresholds',
    color: 'bg-amber-500',
    lightBg: 'bg-amber-50',
    text: 'text-amber-700',
    border: 'border-amber-200',
    iconBg: 'bg-amber-100',
  },
  RiskAgent: {
    label: 'Risk',
    description: 'Analyzes academic risk from attendance and grades',
    color: 'bg-red-500',
    lightBg: 'bg-red-50',
    text: 'text-red-700',
    border: 'border-red-200',
    iconBg: 'bg-red-100',
  },
  KnowledgeAgent: {
    label: 'Knowledge',
    description: 'Searches university policies, handbooks, and regulations',
    color: 'bg-violet-500',
    lightBg: 'bg-violet-50',
    text: 'text-violet-700',
    border: 'border-violet-200',
    iconBg: 'bg-violet-100',
  },
};

// English: SVG icons per agent type — consistent visual language.
// Roman Urdu: Har agent type ke liye SVG icons — consistent visual language.
const AGENT_ICONS = {
  AttendanceAgent: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 11l3 3L22 4" />
      <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" />
    </svg>
  ),
  PolicyAgent: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
      <path d="M14 2v6h6M9 13h6M9 17h6" />
    </svg>
  ),
  RiskAgent: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
      <path d="M12 9v4M12 17h.01" />
    </svg>
  ),
  KnowledgeAgent: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 19.5A2.5 2.5 0 016.5 17H20" />
      <path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z" />
    </svg>
  ),
};

function fallbackMeta(name) {
  return {
    label: name,
    description: 'Specialized agent registered with the orchestrator',
    color: 'bg-ink-500',
    lightBg: 'bg-ink-50',
    text: 'text-ink-700',
    border: 'border-ink-200',
    iconBg: 'bg-ink-100',
  };
}

export default function Agents() {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const response = await api.get('/agents/list');
        setAgents(response.data.agents);
      } catch (err) {
        console.error('Failed to load agents', err);
      } finally {
        setLoading(false);
      }
    };
    fetchAgents();
  }, []);

  return (
    <Layout>
      <div className="p-8 max-w-6xl mx-auto animate-fade-in">
        {/* ==================== Header ==================== */}
        <div className="mb-8">
          <div className="inline-flex items-center gap-2 text-[11px] text-gold-700 font-bold uppercase tracking-widest mb-3">
            <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
            Registry
          </div>
          <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">
            AI Agent Registry
          </h1>
          <p className="text-ink-500 text-[15px] leading-relaxed">
            Every specialized agent registered in the orchestrator's execution pool.
          </p>
        </div>

        {/* ==================== Summary ==================== */}
        <div className="bg-white border border-ink-200 rounded-xl p-5 mb-6 shadow-card">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">
                Active Agents
              </div>
              <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">
                {loading ? '—' : agents.length}
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-xs text-emerald-700 font-semibold">All operational</span>
            </div>
          </div>
        </div>

        {/* ==================== Loading ==================== */}
        {loading && (
          <div className="bg-white border border-ink-200 rounded-xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading agents…</div>
          </div>
        )}

        {/* ==================== Agent Grid ==================== */}
        {!loading && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {agents.map((agent) => {
              const meta = AGENT_META[agent.name] || fallbackMeta(agent.name);
              const icon = AGENT_ICONS[agent.name] || AGENT_ICONS.KnowledgeAgent;

              return (
                <div
                  key={agent.name}
                  className={`relative bg-white border-2 ${meta.border} rounded-2xl p-6 shadow-card hover-lift transition-all overflow-hidden`}
                >
                  {/* Top accent strip */}
                  <div className={`absolute top-0 left-0 right-0 h-1 ${meta.color}`} />

                  {/* Header */}
                  <div className="flex items-start gap-4 mb-4">
                    <div className={`w-12 h-12 rounded-xl ${meta.iconBg} border ${meta.border} flex items-center justify-center ${meta.text} flex-shrink-0`}>
                      <div className="w-6 h-6">{icon}</div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-display font-bold text-ink-900 text-lg leading-tight">
                          {meta.label}Agent
                        </h3>
                        <span className="inline-flex items-center gap-1 text-[10px] uppercase tracking-wider font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                          <span className="w-1 h-1 rounded-full bg-emerald-500"></span>
                          Active
                        </span>
                      </div>
                      <div className="text-xs text-ink-500 font-mono">
                        {agent.name}
                      </div>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-sm text-ink-600 leading-relaxed mb-5">
                    {meta.description}
                  </p>

                  {/* Footer with CTA */}
                  <div className="pt-4 border-t border-ink-100 flex items-center justify-between">
                    <div className="flex items-center gap-1.5">
                      <div className={`w-1.5 h-1.5 rounded-full ${meta.color}`} />
                      <span className={`text-[10px] uppercase tracking-widest font-bold ${meta.text}`}>
                        Registered
                      </span>
                    </div>
                    <Link
                      to="/command-center"
                      className="inline-flex items-center gap-1.5 text-xs font-semibold text-ink-900 hover:text-gold-700 transition-colors"
                    >
                      Try in Command Center
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </Link>
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
