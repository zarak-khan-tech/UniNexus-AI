import { NavLink, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import api from '../api/client';

const NAV_ITEMS = [
  { name: 'Dashboard', path: '/' },
  { name: 'AI Command Center', path: '/command-center' },
  { name: 'Agents', path: '/agents' },
  { name: 'Students', path: '/students' },
  { name: 'Courses', path: '/courses' },
  { name: 'Knowledge Base', path: '/knowledge' },
  { name: 'Audit Logs', path: '/audit' },
];

export default function Layout({ children }) {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get('/auth/me');
        setUser(response.data);
      } catch (err) {
        localStorage.removeItem('token');
        navigate('/login');
      }
    };
    fetchUser();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      <header className="border-b border-slate-700 bg-slate-800/50 backdrop-blur px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-white">UniNexus AI</h1>
          <p className="text-xs text-slate-400">Autonomous Multi-Agent University Intelligence Platform</p>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm text-slate-400">{user ? user.email : 'Loading...'}</span>
          <button
            onClick={handleLogout}
            className="text-sm bg-slate-700 hover:bg-slate-600 px-3 py-1 rounded transition-colors"
          >
            Logout
          </button>
        </div>
      </header>

      <div className="flex flex-1">
        <aside className="w-64 border-r border-slate-700 bg-slate-800/30 p-4 space-y-1">
          <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2 px-3">Navigation</div>
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                `block px-3 py-2 rounded-md text-sm transition-colors ${
                  isActive
                    ? 'bg-blue-600/20 text-blue-300 border-l-2 border-blue-500'
                    : 'hover:bg-slate-700/50 text-slate-300'
                }`
              }
            >
              {item.name}
            </NavLink>
          ))}
        </aside>

        <main className="flex-1 overflow-auto">{children}</main>
      </div>
    </div>
  );
}
