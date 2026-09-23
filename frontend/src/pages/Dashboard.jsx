import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import api from '../api/client';

// -----------------------------------------------------------------------------
// English: Small inline SVG icons for KPI cards — no external dependency.
// Roman Urdu: Chhote SVG icons KPI cards ke liye — kisi aur library ki zaroorat nahi.
// -----------------------------------------------------------------------------
const icons = {
  agents: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="8" r="3.5" />
      <path d="M5 20c0-3.5 3.1-6 7-6s7 2.5 7 6" />
      <path d="M17.5 4.5a3.5 3.5 0 013.2 2.1" />
    </svg>
  ),
  students: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 3L2 9l10 6 10-6-10-6z" />
      <path d="M6 13v5c0 1 2.5 3 6 3s6-2 6-3v-5" />
    </svg>
  ),
  courses: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 5a2 2 0 012-2h13v18H6a2 2 0 01-2-2V5z" />
      <path d="M8 3v18" />
    </svg>
  ),
  documents: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8l-5-5z" />
      <path d="M14 3v5h5" />
      <path d="M9 13h6M9 17h6" />
    </svg>
  ),
  executions: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="5 3 19 12 5 21 5 3" fill="currentColor" stroke="none" />
    </svg>
  ),
};

// -----------------------------------------------------------------------------
// English: Premium KPI card with icon badge, layered shadow, and hover lift.
// Roman Urdu: Premium KPI card — icon badge, layered shadow, aur hover pe halka uthta hai.
// -----------------------------------------------------------------------------
function StatCard({ label, value, hint, iconKey, accent = 'ink' }) {
  // Accent tint map — keeps color usage coherent across cards.
  const tints = {
    ink: {
      bg: 'from-ink-100 to-ink-50',
      fg: 'text-ink-800',
      ring: 'ring-ink-200/60',
    },
    gold: {
      bg: 'from-gold-100 to-gold-50',
      fg: 'text-gold-700',
      ring: 'ring-gold-200/60',
    },
    emerald: {
      bg: 'from-emerald-100 to-emerald-50',
      fg: 'text-emerald-700',
      ring: 'ring-emerald-200/60',
    },
  };
  const t = tints[accent] || tints.ink;

  return (
    <div className="group bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift hover-press card-highlight overflow-hidden">
      <div className="flex items-start justify-between mb-3">
        <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${t.bg} ring-1 ${t.ring} flex items-center justify-center ${t.fg} transition-transform duration-300 group-hover:scale-105`}>
          <div className="w-5 h-5">{icons[iconKey]}</div>
        </div>
      </div>
      <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">
        {label}
      </div>
      <div className="text-3xl font-display font-bold text-ink-900 tracking-tight">
        {value}
      </div>
      {hint && <div className="text-xs text-ink-400 mt-2">{hint}</div>}
    </div>
  );
}

// -----------------------------------------------------------------------------
// English: Quick action button used in the "Quick actions" row.
// Roman Urdu: Quick action button jo "Quick actions" row mein dikhaya jata hai.
// -----------------------------------------------------------------------------
function QuickAction({ to, title, description, icon }) {
  return (
    <Link
      to={to}
      className="group flex items-center gap-4 bg-white border border-ink-200 rounded-xl p-4 shadow-card hover-lift hover-press transition-all"
    >
      <div className="w-11 h-11 rounded-lg bg-ink-50 ring-1 ring-ink-200/60 flex items-center justify-center text-ink-700 transition-colors group-hover:bg-ink-900 group-hover:text-gold-300 group-hover:ring-ink-900">
        <div className="w-5 h-5">{icon}</div>
      </div>
      <div className="min-w-0 flex-1">
        <div className="text-sm font-semibold text-ink-900">{title}</div>
        <div className="text-xs text-ink-500 truncate">{description}</div>
      </div>
      <svg className="w-4 h-4 text-ink-300 group-hover:text-ink-700 group-hover:translate-x-0.5 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
      </svg>
    </Link>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  // English: Fetch live KPI counts from the backend when the page loads.
  // Roman Urdu: Page load hone par backend se live numbers fetch karte hain.
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/stats/overview');
        setStats(response.data);
      } catch (err) {
        console.error('Failed to load stats', err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  return (
    <Layout>
      <div className="p-8 max-w-6xl mx-auto animate-fade-in">
        {/* ==================== Greeting ==================== */}
        <div className="mb-8">
          <div className="inline-flex items-center gap-2 text-xs text-ink-500 mb-3">
            <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="uppercase tracking-wider font-medium">All systems operational</span>
          </div>
          <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">
            Welcome to UniNexus
          </h1>
          <p className="text-ink-500 max-w-2xl text-[15px] leading-relaxed">
            Your multi-agent intelligence platform is online. Here's a live snapshot of your institution.
          </p>
        </div>

        {/* ==================== KPI Grid ==================== */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          <StatCard
            label="Active Agents"
            value={loading ? '—' : stats?.agents}
            iconKey="agents"
            accent="ink"
          />
          <StatCard
            label="Registered Students"
            value={loading ? '—' : stats?.students}
            iconKey="students"
            accent="ink"
          />
          <StatCard
            label="Courses"
            value={loading ? '—' : stats?.courses}
            iconKey="courses"
            accent="ink"
          />
          <StatCard
            label="Knowledge Documents"
            value={loading ? '—' : stats?.documents}
            iconKey="documents"
            accent="gold"
          />
          <StatCard
            label="Agent Executions"
            value={loading ? '—' : stats?.executions}
            hint="All-time audit records"
            iconKey="executions"
            accent="emerald"
          />
        </div>

        {/* ==================== Quick Actions ==================== */}
        <div className="mb-6">
          <h2 className="text-sm font-semibold text-ink-700 uppercase tracking-wider mb-3">
            Quick actions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <QuickAction
              to="/command-center"
              title="Issue a task"
              description="Natural language → multi-agent workflow"
              icon={
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 2v4M12 18v4M4.9 4.9l2.8 2.8M16.3 16.3l2.8 2.8M2 12h4M18 12h4M4.9 19.1l2.8-2.8M16.3 7.7l2.8-2.8" />
                </svg>
              }
            />
            <QuickAction
              to="/students"
              title="Review students"
              description="Live attendance and academic data"
              icon={
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="9" cy="7" r="3" />
                  <path d="M2 21v-2a5 5 0 015-5h4a5 5 0 015 5v2" />
                  <path d="M17 4a3 3 0 010 6M22 21v-2a5 5 0 00-3-4.6" />
                </svg>
              }
            />
            <QuickAction
              to="/analytics"
              title="View analytics"
              description="Institutional insights and charts"
              icon={
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M3 3v18h18" />
                  <path d="M7 15l3-3 4 3 5-6" />
                </svg>
              }
            />
          </div>
        </div>

        {/* ==================== Primary CTA Panel ==================== */}
        <div className="relative bg-ink-950 text-white rounded-2xl p-8 md:p-10 overflow-hidden shadow-float">
          {/* Soft gold glow */}
          <div className="absolute -top-32 -right-24 w-96 h-96 rounded-full bg-gold-500/15 blur-3xl" />
          {/* Subtle academic grid */}
          <div className="absolute inset-0 ink-grid-pattern opacity-60" />
          {/* Top gradient light */}
          <div className="absolute inset-x-0 top-0 h-24 bg-gradient-to-b from-white/5 to-transparent" />

          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-8">
            <div className="max-w-xl">
              <div className="inline-flex items-center gap-2 text-xs text-gold-300 mb-3">
                <span className="w-1.5 h-1.5 rounded-full bg-gold-400"></span>
                <span className="uppercase tracking-widest font-medium">AI Command Center</span>
              </div>
              <h2 className="font-display text-3xl font-bold mb-3 tracking-tight text-white">
                Ready to issue a task?
              </h2>
              <p className="text-ink-200 leading-relaxed">
                Orchestrate multi-agent workflows with natural language. Every plan, action,
                and result is executed end-to-end and logged to your audit trail.
              </p>
            </div>

            <Link
              to="/command-center"
              className="group inline-flex items-center gap-2 gradient-gold text-ink-950 font-semibold px-6 py-3.5 rounded-xl transition-all shadow-[0_8px_24px_-8px_rgba(209,158,11,0.6)] hover:shadow-[0_12px_32px_-8px_rgba(209,158,11,0.8)] hover:-translate-y-0.5 whitespace-nowrap self-start md:self-auto"
            >
              Open Command Center
              <svg className="w-4 h-4 transition-transform group-hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
}
