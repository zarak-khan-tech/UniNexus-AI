function App() {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-800/50 backdrop-blur px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-white">UniNexus AI</h1>
          <p className="text-xs text-slate-400">Autonomous Multi-Agent University Intelligence Platform</p>
        </div>
        <div className="text-sm text-slate-400">Built by ZARAK KHAN</div>
      </header>

      {/* Main Layout */}
      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-64 border-r border-slate-700 bg-slate-800/30 p-4 space-y-2">
          <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2">Navigation</div>
          {['Dashboard', 'AI Command Center', 'Agents', 'Students', 'Courses', 'Knowledge Base', 'Audit Logs'].map((item) => (
            <div key={item} className="px-3 py-2 rounded-md hover:bg-slate-700/50 cursor-pointer text-sm transition-colors">
              {item}
            </div>
          ))}
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 p-8">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-2xl font-semibold mb-4">Welcome to the Command Center</h2>
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
              <p className="text-slate-400 mb-4">
                The multi-agent system is online. Use the AI Command Center to issue natural-language tasks to the orchestrator.
              </p>
              <div className="h-64 flex items-center justify-center border-2 border-dashed border-slate-700 rounded-lg">
                <span className="text-slate-500">Agent workflow visualization will appear here</span>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default App
