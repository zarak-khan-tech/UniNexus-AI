import { NavLink, useNavigate, Link } from 'react-router-dom';
import { useEffect, useState, useRef } from 'react';
import api from '../api/client';

const NAV_GROUPS = [
  {
    label: 'Overview',
    items: [
      { name: 'Dashboard', path: '/' },
      { name: 'AI Command Center', path: '/command-center' },
      { name: 'Analytics', path: '/analytics' },
    ],
  },
  {
    label: 'Intelligence',
    items: [
      { name: 'Agents', path: '/agents' },
      { name: 'Tools', path: '/tools' },
      { name: 'Approvals', path: '/approvals' },
      { name: 'Workflows', path: '/workflows', badge: 'soon' },
    ],
  },
  {
    label: 'Academics',
    items: [
      { name: 'Students', path: '/students' },
      { name: 'Courses', path: '/courses' },
      { name: 'Knowledge Base', path: '/knowledge' },
    ],
  },
  {
    label: 'Operations',
    items: [
      { name: 'Notifications', path: '/notifications' },
      { name: 'Audit Logs', path: '/audit' },
    ],
  },
];

function getInitials(email) {
  if (!email) return '··';
  const name = email.split('@')[0];
  const parts = name.split(/[.\-_]/).filter(Boolean);
  if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
  return name.slice(0, 2).toUpperCase();
}

function timeAgo(iso) {
  const now = new Date();
  const then = new Date(iso);
  const diff = Math.floor((now - then) / 1000);
  if (diff < 60) return 'just now';
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`;
  return then.toLocaleDateString();
}

const KIND_COLORS = {
  approval: { bg: 'bg-violet-100', text: 'text-violet-700', dot: 'bg-violet-500' },
  execution: { bg: 'bg-blue-100', text: 'text-blue-700', dot: 'bg-blue-500' },
  system: { bg: 'bg-ink-100', text: 'text-ink-700', dot: 'bg-ink-500' },
};

function NotificationBell() {
  const [open, setOpen] = useState(false);
  const [data, setData] = useState({ notifications: [], unread_count: 0 });
  const [loading, setLoading] = useState(false);
  const ref = useRef(null);
  const navigate = useNavigate();

  const fetchNotifications = async () => {
    try {
      const res = await api.get('/notifications?status=all&limit=8');
      setData(res.data);
    } catch (err) {
      console.error('Failed to load notifications', err);
    }
  };

  // English: Poll every 30s for new notifications.
  // Roman Urdu: Har 30 second pe nayi notifications ke liye check karo.
  useEffect(() => {
    fetchNotifications();
    const iv = setInterval(fetchNotifications, 30000);
    return () => clearInterval(iv);
  }, []);

  useEffect(() => {
    const handler = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const toggle = async () => {
    const next = !open;
    setOpen(next);
    if (next) {
      setLoading(true);
      await fetchNotifications();
      setLoading(false);
    }
  };

  const handleClick = async (n) => {
    if (!n.is_read) {
      try { await api.post(`/notifications/${n.id}/read`); } catch (e) {}
    }
    setOpen(false);
    if (n.action_url) navigate(n.action_url);
  };

  const unread = data.unread_count || 0;

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={toggle}
        className="relative p-2 rounded-lg hover:bg-ink-50 transition-colors"
        title="Notifications"
      >
        <svg className="w-5 h-5 text-ink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M15 17h5l-1.4-1.4A2 2 0 0118 14.2V11a6 6 0 10-12 0v3.2c0 .5-.2 1-.6 1.4L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        {unread > 0 && (
          <span className="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] px-1 rounded-full bg-red-500 text-white text-[10px] font-bold flex items-center justify-center border-2 border-white">
            {unread > 9 ? '9+' : unread}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-96 bg-white border border-ink-200 rounded-xl shadow-float z-30 overflow-hidden animate-slide-up">
          {/* Header */}
          <div className="px-4 py-3 border-b border-ink-100 bg-ink-50/60 flex items-center justify-between">
            <div>
              <div className="text-sm font-bold text-ink-900">Notifications</div>
              <div className="text-[11px] text-ink-500">
                {unread > 0 ? `${unread} unread` : 'All caught up'}
              </div>
            </div>
            {unread > 0 && (
              <button
                onClick={async () => {
                  try { await api.post('/notifications/read-all'); await fetchNotifications(); } catch (e) {}
                }}
                className="text-[11px] font-semibold text-ink-600 hover:text-ink-900 transition-colors"
              >
                Mark all read
              </button>
            )}
          </div>

          {/* List */}
          <div className="max-h-96 overflow-y-auto">
            {loading && (
              <div className="p-8 text-center text-xs text-ink-500">Loading…</div>
            )}
            {!loading && data.notifications.length === 0 && (
              <div className="p-8 text-center">
                <div className="text-sm text-ink-500 mb-1">No notifications yet</div>
                <div className="text-xs text-ink-400">You'll see updates here when the AI acts.</div>
              </div>
            )}
            {!loading && data.notifications.map((n) => {
              const k = KIND_COLORS[n.kind] || KIND_COLORS.system;
              return (
                <button
                  key={n.id}
                  onClick={() => handleClick(n)}
                  className={`w-full text-left px-4 py-3 border-b border-ink-100 last:border-b-0 hover:bg-ink-50/60 transition-colors ${!n.is_read ? 'bg-violet-50/40' : ''}`}
                >
                  <div className="flex items-start gap-3">
                    <div className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${n.is_read ? 'bg-ink-200' : k.dot}`}></div>
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2 mb-0.5">
                        <div className={`text-xs font-semibold ${n.is_read ? 'text-ink-700' : 'text-ink-900'}`}>
                          {n.title}
                        </div>
                        <div className="text-[10px] text-ink-400 ml-auto whitespace-nowrap">{timeAgo(n.created_at)}</div>
                      </div>
                      <div className="text-xs text-ink-500 leading-snug line-clamp-2">{n.body}</div>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Footer */}
          <div className="px-4 py-2.5 border-t border-ink-100 bg-ink-50/40">
            <Link
              to="/notifications"
              onClick={() => setOpen(false)}
              className="block text-center text-xs font-semibold text-ink-700 hover:text-ink-900 transition-colors"
            >
              View all notifications →
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}

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
    <div className="min-h-screen bg-slate-50 text-ink-900 flex">
      <aside className="hidden md:flex w-64 flex-col border-r border-ink-100 bg-white">
        <div className="px-5 py-5 border-b border-ink-100">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center font-display font-bold text-ink-950">U</div>
            <div>
              <div className="font-display font-bold text-[15px] tracking-tight text-ink-900 leading-tight">UniNexus AI</div>
              <div className="text-[10px] text-ink-400 tracking-widest uppercase">Academic Intelligence</div>
            </div>
          </div>
        </div>
        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-5">
          {NAV_GROUPS.map((group) => (
            <div key={group.label}>
              <div className="text-[10px] font-semibold uppercase tracking-widest text-ink-400 px-3 mb-2">{group.label}</div>
              <div className="space-y-0.5">
                {group.items.map((item) => (
                  <NavLink
                    key={item.path}
                    to={item.badge === 'soon' ? '#' : item.path}
                    end={item.path === '/'}
                    onClick={(e) => { if (item.badge === 'soon') e.preventDefault(); }}
                    className={({ isActive }) =>
                      `group flex items-center justify-between px-3 py-2 rounded-md text-sm transition-colors ${
                        item.badge === 'soon'
                          ? 'text-ink-400 cursor-not-allowed'
                          : isActive
                          ? 'bg-ink-900 text-white font-medium'
                          : 'text-ink-700 hover:bg-ink-50'
                      }`
                    }
                  >
                    <span>{item.name}</span>
                    {item.badge === 'soon' && (
                      <span className="text-[10px] uppercase tracking-wider text-ink-400 border border-ink-200 rounded px-1.5 py-0.5">soon</span>
                    )}
                  </NavLink>
                ))}
              </div>
            </div>
          ))}
        </nav>
        <div className="border-t border-ink-100 p-3">
          <div className="flex items-center gap-3 px-2 py-2 rounded-lg hover:bg-ink-50 transition-colors">
            <div className="w-9 h-9 rounded-full bg-ink-900 text-gold-300 flex items-center justify-center text-xs font-bold flex-shrink-0">{getInitials(user?.email)}</div>
            <div className="min-w-0 flex-1">
              <div className="text-xs font-medium text-ink-900 truncate">{user ? user.email : 'Loading…'}</div>
              <div className="text-[10px] uppercase tracking-wider text-ink-400">{user ? user.role : '—'}</div>
            </div>
          </div>
          <button onClick={handleLogout} className="w-full mt-1 text-xs text-ink-500 hover:text-ink-900 px-3 py-2 rounded-md hover:bg-ink-50 transition-colors text-left">
            Sign out
          </button>
        </div>
      </aside>
      <div className="flex-1 flex flex-col min-w-0">
        <header className="border-b border-ink-100 bg-white/80 backdrop-blur sticky top-0 z-20">
          <div className="px-6 lg:px-8 py-3 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="md:hidden flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center font-display font-bold text-ink-950 text-sm">U</div>
                <span className="font-display font-bold text-ink-900">UniNexus AI</span>
              </div>
              <div className="hidden md:flex items-center gap-2 text-xs">
                <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                <span className="text-ink-500">Connected</span>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <NotificationBell />
              <button onClick={handleLogout} className="text-sm text-ink-600 hover:text-ink-900 px-3 py-1.5 rounded-lg hover:bg-ink-50 transition-colors">
                Sign out
              </button>
            </div>
          </div>
        </header>
        <main className="flex-1 min-w-0">{children}</main>
      </div>
    </div>
  );
}
