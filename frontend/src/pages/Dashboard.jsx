import Layout from '../components/Layout';

export default function Dashboard() {
  return (
    <Layout>
      <div className="p-8 max-w-5xl mx-auto">
        <h2 className="text-2xl font-semibold mb-4 text-white">Welcome to the Command Center</h2>
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
          <p className="text-slate-400 mb-4">
            The multi-agent system is online. Use the AI Command Center to issue natural-language tasks to the orchestrator.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
            <div className="bg-slate-900 border border-slate-700 rounded-lg p-4">
              <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">Active Agents</div>
              <div className="text-3xl font-bold text-white">4</div>
            </div>
            <div className="bg-slate-900 border border-slate-700 rounded-lg p-4">
              <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">Registered Students</div>
              <div className="text-3xl font-bold text-white">2</div>
            </div>
            <div className="bg-slate-900 border border-slate-700 rounded-lg p-4">
              <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">Knowledge Docs</div>
              <div className="text-3xl font-bold text-white">2</div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
