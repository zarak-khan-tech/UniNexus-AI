import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import api from '../api/client';

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
      <div className="p-8 max-w-6xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-white mb-2">AI Agent Registry</h1>
          <p className="text-slate-400">
            Every specialized agent registered in the orchestrator's execution pool.
          </p>
        </div>

        {loading && (
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-16 text-center">
            <div className="text-slate-500">Loading agents...</div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {agents.map((agent) => (
            <div
              key={agent.name}
              className="bg-slate-800 border border-slate-700 rounded-xl p-6 hover:border-blue-500/40 transition-colors"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-2.5 h-2.5 rounded-full bg-green-400 shadow-[0_0_8px_rgba(74,222,128,0.6)]"></div>
                  <h3 className="font-semibold text-white">{agent.name}</h3>
                </div>
                <span className="text-xs px-2 py-0.5 rounded bg-green-500/15 text-green-300 border border-green-500/30">
                  Active
                </span>
              </div>
              <p className="text-sm text-slate-400 leading-relaxed mb-4">{agent.description}</p>
              <Link
                to="/command-center"
                className="inline-block text-xs text-blue-400 hover:text-blue-300 font-medium"
              >
                Try in Command Center →
              </Link>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
}
