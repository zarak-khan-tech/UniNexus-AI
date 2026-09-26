import { useEffect, useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line
} from 'recharts';
import Layout from '../components/Layout';
import api from '../api/client';

// English: Risk colors — consistent with the rest of the platform.
// Roman Urdu: Risk ke rang — baaki platform ke saath consistent.
const RISK_COLORS = { High: '#ef4444', Medium: '#f59e0b', Low: '#10b981' };

// English: Custom tooltip styling for light theme.
// Roman Urdu: Light theme ke liye custom tooltip styling.
const TOOLTIP_STYLE = {
  backgroundColor: '#ffffff',
  border: '1px solid #e2e8f0',
  borderRadius: '8px',
  boxShadow: '0 4px 12px rgba(15,23,42,0.08)',
  fontSize: '12px',
  color: '#0f172a',
};

function StatCard({ label, value, accent = 'text-ink-900' }) {
  return (
    <div className="bg-white border border-ink-200 rounded-xl p-5 shadow-card hover-lift transition-all">
      <div className="text-xs uppercase tracking-wider text-ink-500 font-medium mb-1.5">
        {label}
      </div>
      <div className={`text-3xl font-display font-bold tracking-tight ${accent}`}>{value}</div>
    </div>
  );
}

export default function Analytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/analytics/overview');
        setData(response.data);
      } catch (err) {
        console.error('Failed to load analytics', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <Layout>
        <div className="p-8 max-w-6xl mx-auto">
          <div className="bg-white border border-ink-200 rounded-xl p-16 text-center shadow-card">
            <div className="inline-block w-6 h-6 border-2 border-ink-300 border-t-ink-900 rounded-full animate-spin mb-3"></div>
            <div className="text-ink-500 text-sm">Loading analytics…</div>
          </div>
        </div>
      </Layout>
    );
  }

  if (!data) return null;

  const riskPieData = Object.entries(data.risk_distribution).map(([name, value]) => ({
    name, value,
  }));

  return (
    <Layout>
      <div className="p-8 max-w-6xl mx-auto animate-fade-in">
        {/* ==================== Header ==================== */}
        <div className="mb-8">
          <h1 className="font-display text-4xl font-bold text-ink-900 mb-2 tracking-tight">
            Analytics
          </h1>
          <p className="text-ink-500 text-[15px] leading-relaxed">
            Real-time insights from your institutional data and agent activity.
          </p>
        </div>

        {/* ==================== Summary Cards ==================== */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
          <StatCard label="Total Executions" value={data.total_executions} />
          <StatCard
            label="High Risk Cases"
            value={data.risk_distribution.High}
            accent="text-red-600"
          />
          <StatCard
            label="Students Tracked"
            value={data.attendance_by_student.length}
          />
        </div>

        {/* ==================== Charts Grid ==================== */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Risk Distribution Pie */}
          <div className="bg-white border border-ink-200 rounded-2xl p-6 shadow-card">
            <h2 className="font-display text-lg font-bold text-ink-900 mb-1">
              Risk Distribution
            </h2>
            <p className="text-xs text-ink-500 mb-4">
              Enrollment-level risk based on attendance and grades
            </p>
            <div style={{ width: '100%', height: 280 }}>
              <ResponsiveContainer>
                <PieChart>
                  <Pie
                    data={riskPieData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => value > 0 ? name + ': ' + value : ''}
                    outerRadius={90}
                    innerRadius={55}
                    dataKey="value"
                    stroke="#ffffff"
                    strokeWidth={2}
                  >
                    {riskPieData.map((entry, idx) => (
                      <Cell key={idx} fill={RISK_COLORS[entry.name] || '#64748b'} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={TOOLTIP_STYLE} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Attendance per Student */}
          <div className="bg-white border border-ink-200 rounded-2xl p-6 shadow-card">
            <h2 className="font-display text-lg font-bold text-ink-900 mb-1">
              Average Attendance per Student
            </h2>
            <p className="text-xs text-ink-500 mb-4">
              Threshold is 75% — below this requires intervention
            </p>
            <div style={{ width: '100%', height: 280 }}>
              <ResponsiveContainer>
                <BarChart data={data.attendance_by_student}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                  <XAxis
                    dataKey="name"
                    stroke="#94a3b8"
                    fontSize={10}
                    angle={-35}
                    textAnchor="end"
                    height={60}
                    interval={0}
                  />
                  <YAxis stroke="#94a3b8" fontSize={11} domain={[0, 100]} />
                  <Tooltip contentStyle={TOOLTIP_STYLE} />
                  <Bar dataKey="attendance" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Agent Usage */}
          <div className="bg-white border border-ink-200 rounded-2xl p-6 shadow-card">
            <h2 className="font-display text-lg font-bold text-ink-900 mb-1">
              Agent Usage
            </h2>
            <p className="text-xs text-ink-500 mb-4">
              How often each specialized agent was invoked
            </p>
            {data.agent_usage.length > 0 ? (
              <div style={{ width: '100%', height: 280 }}>
                <ResponsiveContainer>
                  <BarChart data={data.agent_usage} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" horizontal={false} />
                    <XAxis type="number" stroke="#94a3b8" fontSize={11} allowDecimals={false} />
                    <YAxis
                      type="category"
                      dataKey="agent"
                      stroke="#94a3b8"
                      fontSize={11}
                      width={120}
                    />
                    <Tooltip contentStyle={TOOLTIP_STYLE} />
                    <Bar dataKey="count" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <div className="h-64 flex items-center justify-center text-ink-400 text-sm">
                No agent usage yet. Run some tasks in the Command Center.
              </div>
            )}
          </div>

          {/* Executions over Time */}
          <div className="bg-white border border-ink-200 rounded-2xl p-6 shadow-card">
            <h2 className="font-display text-lg font-bold text-ink-900 mb-1">
              Executions (Last 7 Days)
            </h2>
            <p className="text-xs text-ink-500 mb-4">
              Daily volume of agent workflow executions
            </p>
            <div style={{ width: '100%', height: 280 }}>
              <ResponsiveContainer>
                <LineChart data={data.executions_by_day}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                  <XAxis dataKey="date" stroke="#94a3b8" fontSize={11} />
                  <YAxis stroke="#94a3b8" fontSize={11} allowDecimals={false} />
                  <Tooltip contentStyle={TOOLTIP_STYLE} />
                  <Line
                    type="monotone"
                    dataKey="executions"
                    stroke="#06b6d4"
                    strokeWidth={3}
                    dot={{ r: 5, fill: '#06b6d4', strokeWidth: 0 }}
                    activeDot={{ r: 7 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
