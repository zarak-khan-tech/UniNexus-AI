import { useEffect, useState } from 'react';
import api from '../api/client';

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get('/auth/me');
        console.log('User fetched successfully:', response.data);
        setUser(response.data);
      } catch (err) {
        console.error('Failed to fetch /auth/me:', err);
        console.error('Error response:', err.response);
        console.error('Error message:', err.message);
        setError(JSON.stringify(err.response?.data || err.message, null, 2));
      }
    };
    fetchUser();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-slate-100 p-8">
        <div className="max-w-2xl w-full bg-red-900/30 border border-red-700 rounded-xl p-6">
          <h2 className="text-xl font-bold mb-4">Error Fetching User</h2>
          <pre className="text-sm bg-slate-950 p-4 rounded overflow-auto">{error}</pre>
          <button onClick={handleLogout} className="mt-4 bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded">
            Back to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      <header className="border-b border-slate-700 bg-slate-800/50 backdrop-blur px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-white">UniNexus AI</h1>
          <p className="text-xs text-slate-400">Autonomous Multi-Agent University Intelligence Platform</p>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm text-slate-400">{user ? user.email : 'Loading...'}</span>
          <button onClick={handleLogout} className="text-sm bg-slate-700 hover:bg-slate-600 px-3 py-1 rounded transition-colors">Logout</button>
        </div>
      </header>

      <div className="flex flex-1">
        <aside className="w-64 border-r border-slate-700 bg-slate-800/30 p-4 space-y-2">
          <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2">Navigation</div>
          {['Dashboard', 'AI Command Center', 'Agents', 'Students', 'Courses', 'Knowledge Base', 'Audit Logs'].map((item) => (
            <div key={item} className="px-3 py-2 rounded-md hover:bg-slate-700/50 cursor-pointer text-sm transition-colors">
              {item}
            </div>
          ))}
        </aside>

        <main className="flex-1 p-8">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-2xl font-semibold mb-4">Welcome to the Command Center</h2>
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
              <p className="text-slate-400 mb-4">
                Logged in as: <span className="text-white font-semibold">{user?.email}</span>
              </p>
              <div className="h-64 flex items-center justify-center border-2 border-dashed border-slate-700 rounded-lg">
                <span className="text-slate-500">Agent workflow visualization will appear here</span>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
