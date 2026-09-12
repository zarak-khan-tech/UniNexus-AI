import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import api from '../api/client';

function StatCard({ label, value, accent }) {
  return (
    <div className="bg-slate-900 border border-slate-700 rounded-lg p-4">
      <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">{label}</div>
      <div className={`text-3xl font-bold ${accent || 'text-white'}`}>{value}</div>
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/stats/overview');
        setStats(response.data);
      } catch (err) {
        console.error('Failed to load stats', err);
      }
    };
    fetchStats();
  }, []);

  return (
    <Layout>
      <div className="p-8 max-w-5xl mx-auto">
        <h2 className="text-2xl font-semibold mb-4 text-white">Welcome to the Command Center</h2>
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
          <p className="text-slate-400 mb-4">
            The multi-agent system is online. Use the AI Command Center to issue natural-language tasks to the orchestrator.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
            <StatCard label="Active Agents" value={stats ? stats.agents : '—'} />
            <StatCard label="Registered Students" value={stats ? stats.students : '—'} />
            <StatCard label="Courses" value={stats ? stats.courses : '—'} />
            <StatCard label="Knowledge Docs" value={stats ? stats.documents : '—'} />
            <StatCard label="Agent Executions" value={stats ? stats.executions : '—'} accent="text-blue-300" />
          </div>
        </div>
      </div>
    </Layout>
  );
}
