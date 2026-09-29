import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import api from '../api/client';

function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleString('en-US', {
    month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

const KIND_META = {
  approval:  { label: 'Approval',  bg: 'bg-violet-50', text: 'text-violet-700', border: 'border-violet-200', dot: 'bg-violet-500' },
  execution: { label: 'Execution', bg: 'bg-blue-50',   text: 'text-blue-700',   border: 'border-blue-200',   dot: 'bg-blue-500' },
  system:    { label: 'System',    bg: 'bg-ink-50',    text: 'text-ink-700',    border: 'border-ink-200',    dot: 'bg-ink-500' },
};

function kindStyle(k) {
  return KIND_META[k] || KIND_META.system;
}

export default function Notifications() {
  const [items, setItems] = useState([]);
  const [unread, setUnread] = useState(0);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const res = await api.get(`/notifications?status=${filter}&limit=100`);
      setItems(res.data.notifications || []);
      setUnread(res.data.unread_count || 0);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchNotifications(); }, [filter]);

  const markRead = async (id) => {
    try {
      await api.post(`/notifications/${id}/read`);
      await fetchNotifications();
    } catch (err) { console.error(err); }
  };

  const markAllRead = async () => {
    try {
      await api.post('/notifications/read-all');
      await fetchNotifications();
    } catch (err) { console.error(err); }
  };

  return (
    <Layout>
      <div className="p-8 max-w-4xl mx-auto animate-fade-in">
        {/* Header */}
        <div className="mb-8 flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 text-[11px] text-gold-700 font-bold uppercase tracking-widest mb-3">
              <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
              Activity Feed
            </div>
            <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">Notifications</h1>
            <p className="text-ink-500 text-[15px] leading-relaxed max-w-2xl">
              Updates from the platform — approvals requested, actions completed, and system events.
            </p>
          </div>
          {unread > 0 && (
            <button
              onClick={markAllRead}
              className="inline-flex items-center gap-2 text-sm bg-white border border-ink-200 hover:border-ink-400 text-ink-700 hover:text-ink-900 font-semibold px-4 py-2.5 rounded-lg transition-all shadow-card hover:shadow-card-hover"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Mark all as read
            </button>
          )}
        </div>

        {/* Filter tabs */}
        <div className="inline-flex items-center gap-1 p-1 bg-ink-100 border border-ink-200 rounded-xl mb-6 shadow-inset-soft">
          {[
            { id: 'all', label: 'All' },
            { id: 'unread', label: 'Unread' },
            { id: 'read', label: 'Read' },
          ].map((t) => (
            <button
              key={t.id}
              onClick={() => setFilter(t.id)}
              className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
                filter === t.id ? 'bg-ink-900 text-white shadow-card' : 'text-ink-600 hover:text-ink-900 hover:bg-white'
              }`}
            >
              {t.label}
              {t.id === 'unread' && unread > 0 && (
                <span className="ml-2 inline-flex items-center justify-center min-w-[18px] h-[18px] text-[10px] font-bold rounded-full bg-red-500 text-white px-1.5">
                  {unread}
                </span>
              )}
            </button>
          ))}
        </div>

        {loading && (
          <div className="bg-white border border-ink-200 rounded-xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading…</div>
          </div>
        )}

        {!loading && items.length === 0 && (
          <div className="relative bg-gradient-to-br from-white to-ink-50/50 border-2 border-dashed border-ink-200 rounded-2xl p-16 text-center overflow-hidden">
            <div className="relative">
              <div className="w-16 h-16 mx-auto mb-5 rounded-2xl bg-emerald-100 flex items-center justify-center">
                <svg className="w-8 h-8 text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div className="font-display text-xl font-bold text-ink-900 mb-2">
                {filter === 'unread' ? 'No unread notifications' : 'No notifications yet'}
              </div>
              <div className="text-sm text-ink-500 max-w-md mx-auto">
                Updates will appear here when the AI takes actions, requests approvals, or completes tasks.
              </div>
            </div>
          </div>
        )}

        {!loading && items.length > 0 && (
          <div className="space-y-3">
            {items.map((n) => {
              const k = kindStyle(n.kind);
              return (
                <div
                  key={n.id}
                  className={`relative bg-white border rounded-2xl shadow-card overflow-hidden transition-all ${
                    !n.is_read ? 'border-violet-200' : 'border-ink-200'
                  }`}
                >
                  {!n.is_read && <div className={`absolute top-0 left-0 right-0 h-1 ${k.dot}`} />}
                  <div className="p-5 flex items-start gap-4">
                    <div className={`w-10 h-10 rounded-xl ${k.bg} ${k.text} flex items-center justify-center flex-shrink-0 border ${k.border}`}>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M15 17h5l-1.4-1.4A2 2 0 0118 14.2V11a6 6 0 10-12 0v3.2c0 .5-.2 1-.6 1.4L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                      </svg>
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-wrap items-center gap-2 mb-1">
                        <span className={`text-[10px] uppercase tracking-widest font-bold px-2 py-0.5 rounded-full border ${k.bg} ${k.text} ${k.border}`}>
                          {k.label}
                        </span>
                        {!n.is_read && (
                          <span className="text-[10px] uppercase tracking-widest font-bold text-red-600 bg-red-50 border border-red-200 rounded-full px-2 py-0.5">
                            New
                          </span>
                        )}
                        <span className="text-[11px] text-ink-400 ml-auto">{formatDate(n.created_at)}</span>
                      </div>
                      <div className={`font-semibold mb-1 ${!n.is_read ? 'text-ink-900' : 'text-ink-700'}`}>{n.title}</div>
                      <div className="text-sm text-ink-600 leading-relaxed">{n.body}</div>
                      <div className="flex items-center gap-3 mt-3">
                        {n.action_url && (
                          <Link
                            to={n.action_url}
                            onClick={() => { if (!n.is_read) markRead(n.id); }}
                            className="text-xs font-semibold text-ink-900 hover:text-gold-700 inline-flex items-center gap-1 transition-colors"
                          >
                            Open
                            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                          </Link>
                        )}
                        {!n.is_read && (
                          <button
                            onClick={() => markRead(n.id)}
                            className="text-xs font-semibold text-ink-500 hover:text-ink-900 transition-colors"
                          >
                            Mark as read
                          </button>
                        )}
                      </div>
                    </div>
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
