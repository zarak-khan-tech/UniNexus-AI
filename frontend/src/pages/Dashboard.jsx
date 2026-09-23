import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import api from '../api/client';

// English: A single KPI card — light surface, ink text, subtle hover elevation.
// Roman Urdu: Ek single stat card — light background, ink text, aur hover pe halki shadow.
function StatCard({ label, value, accent = 'text-ink-900', hint }) {
  return (
    <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover:shadow-card-hover transition-shadow">
      <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-2">
        {label}
      </div>
      <div className={`text-3xl font-display font-bold ${accent}`}>{value}</div>
      {hint && <div className="text-xs text-ink-400 mt-2">{hint}</div>}
    </div>
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
      <div className="p-8 max-w-6xl mx-auto">
        {/* Greeting */}
        <div className="mb-8">
          <h1 className="font-display text-3xl font-bold text-ink-900 mb-2">
            Welcome to UniNexus
          </h1>
          <p className="text-ink-500 max-w-2xl">
            Your multi-agent intelligence platform is online. Here's a snapshot of your institution.
          </p>
        </div>

        {/* KPI grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          <StatCard label="Active Agents" value={loading ? '—' : stats?.agents} />
          <StatCard label="Registered Students" value={loading ? '—' : stats?.students} />
          <StatCard label="Courses" value={loading ? '—' : stats?.courses} />
          <StatCard label="Knowledge Documents" value={loading ? '—' : stats?.documents} />
          <StatCard
            label="Agent Executions"
            value={loading ? '—' : stats?.executions}
            hint="All-time audit records"
          />
        </div>

        {/* CTA panel — dark navy + gold accent, matching brand */}
        <div className="bg-ink-950 text-white rounded-xl p-8 relative overflow-hidden">
          <div className="absolute -top-20 -right-20 w-64 h-64 rounded-full bg-gold-500/10 blur-3xl" />
          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div>
              <h2 className="font-display text-2xl font-bold mb-2">Ready to issue a task?</h2>
              <p className="text-ink-200 max-w-lg leading-relaxed">
                The AI Command Center lets you orchestrate multi-agent workflows with natural language.
                Every action is planned, executed, and logged.
              </p>
            </div>
            <Link
              to="/command-center"
              className="inline-flex items-center gap-2 bg-gold-400 hover:bg-gold-300 text-ink-950 font-semibold px-6 py-3 rounded-lg transition-colors whitespace-nowrap self-start md:self-auto"
            >
              Open Command Center
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
}
