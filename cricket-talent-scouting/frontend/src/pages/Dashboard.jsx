import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import MetricCard from '../components/MetricCard';
import {
  Users,
  Trophy,
  Zap,
  Target,
  Shield,
  Flame,
  ArrowRight
} from 'lucide-react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend
} from 'recharts';

export default function Dashboard({ onNavigate }) {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      setLoading(true);
      const res = await api.getDashboard();
      if (res.status === 'success') {
        setData(res.data);
      }
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="spinner-container">
        <div className="spinner"></div>
        <p>Loading Cricket Analytics Dashboard...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="alert alert-error">
        <span>Error: {error || 'No data returned from backend.'}</span>
      </div>
    );
  }

  // Formatting chart data
  const roleChartData = Object.entries(data.role_distribution || {}).map(([key, val]) => ({
    name: key,
    value: val,
  }));

  const tierChartData = Object.entries(data.tier_distribution || {}).map(([key, val]) => ({
    name: key.split(' - ')[0],
    count: val,
  }));

  const ROLE_COLORS = ['#0d6e38', '#16a34a', '#0284c7', '#f59e0b'];
  const TIER_COLORS = ['#16a34a', '#0284c7', '#f59e0b', '#94a3b8'];

  return (
    <div>
      {/* KPI Cards */}
      <div className="metric-grid">
        <MetricCard
          title="Scouted Players"
          value={data.total_players}
          subtext="International & league database"
          icon={Users}
          color="#16a34a"
          bg="#dcfce7"
        />
        <MetricCard
          title="Squad Total Runs"
          value={data.total_runs?.toLocaleString()}
          subtext="Cumulative batting tally"
          icon={Trophy}
          color="#0284c7"
          bg="#e0f2fe"
        />
        <MetricCard
          title="Squad Total Wickets"
          value={data.total_wickets?.toLocaleString()}
          subtext="Cumulative bowling dismissals"
          icon={Target}
          color="#dc2626"
          bg="#fee2e2"
        />
        <MetricCard
          title="Mean Batting Average"
          value={data.avg_batting_average}
          subtext="Calculated across all batters"
          icon={Shield}
          color="#f59e0b"
          bg="#fef3c7"
        />
        <MetricCard
          title="Mean Strike Rate"
          value={data.avg_strike_rate}
          subtext="Scoring tempo across formats"
          icon={Zap}
          color="#7e22ce"
          bg="#f3e8ff"
        />
      </div>

      {/* Top Performers Spotlight */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Top Role Performers Spotlight</h3>
            <p className="card-description">Highest impact players categorized by primary cricket role</p>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '20px' }}>
          {/* Top Batter */}
          <div style={{ border: '1px solid #e2e8f0', borderRadius: '12px', padding: '18px', background: '#fafafa' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="badge badge-batter">Lead Batter</span>
              <span style={{ fontSize: '0.8rem', color: '#64748b' }}>{data.top_performers?.batter?.Country}</span>
            </div>
            <h4 style={{ fontSize: '1.15rem', marginTop: '10px', color: '#0f172a' }}>{data.top_performers?.batter?.Player}</h4>
            <div style={{ marginTop: '12px', fontSize: '0.88rem', color: '#475569', display: 'flex', gap: '16px' }}>
              <div><strong>{data.top_performers?.batter?.Runs?.toLocaleString()}</strong> Runs</div>
              <div>Avg: <strong>{data.top_performers?.batter?.Batting_Average}</strong></div>
              <div>SR: <strong>{data.top_performers?.batter?.Strike_Rate}</strong></div>
            </div>
          </div>

          {/* Top Bowler */}
          <div style={{ border: '1px solid #e2e8f0', borderRadius: '12px', padding: '18px', background: '#fafafa' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="badge badge-bowler">Lead Bowler</span>
              <span style={{ fontSize: '0.8rem', color: '#64748b' }}>{data.top_performers?.bowler?.Country}</span>
            </div>
            <h4 style={{ fontSize: '1.15rem', marginTop: '10px', color: '#0f172a' }}>{data.top_performers?.bowler?.Player}</h4>
            <div style={{ marginTop: '12px', fontSize: '0.88rem', color: '#475569', display: 'flex', gap: '16px' }}>
              <div><strong>{data.top_performers?.bowler?.Wickets}</strong> Wkts</div>
              <div>Econ: <strong>{data.top_performers?.bowler?.Economy_Rate}</strong></div>
              <div>Avg: <strong>{data.top_performers?.bowler?.Bowling_Average}</strong></div>
            </div>
          </div>

          {/* Top All-Rounder */}
          <div style={{ border: '1px solid #e2e8f0', borderRadius: '12px', padding: '18px', background: '#fafafa' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="badge badge-allrounder">Lead All-Rounder</span>
              <span style={{ fontSize: '0.8rem', color: '#64748b' }}>{data.top_performers?.allrounder?.Country}</span>
            </div>
            <h4 style={{ fontSize: '1.15rem', marginTop: '10px', color: '#0f172a' }}>{data.top_performers?.allrounder?.Player}</h4>
            <div style={{ marginTop: '12px', fontSize: '0.88rem', color: '#475569', display: 'flex', gap: '16px' }}>
              <div>Score: <strong>{data.top_performers?.allrounder?.Talent_Score}</strong>/100</div>
              <div>Runs: <strong>{data.top_performers?.allrounder?.Runs}</strong></div>
              <div>Wkts: <strong>{data.top_performers?.allrounder?.Wickets}</strong></div>
            </div>
          </div>

          {/* Top Wicketkeeper */}
          <div style={{ border: '1px solid #e2e8f0', borderRadius: '12px', padding: '18px', background: '#fafafa' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="badge badge-wicketkeeper">Lead Wicketkeeper</span>
              <span style={{ fontSize: '0.8rem', color: '#64748b' }}>{data.top_performers?.wicketkeeper?.Country}</span>
            </div>
            <h4 style={{ fontSize: '1.15rem', marginTop: '10px', color: '#0f172a' }}>{data.top_performers?.wicketkeeper?.Player}</h4>
            <div style={{ marginTop: '12px', fontSize: '0.88rem', color: '#475569', display: 'flex', gap: '16px' }}>
              <div>Score: <strong>{data.top_performers?.wicketkeeper?.Talent_Score}</strong>/100</div>
              <div>Runs: <strong>{data.top_performers?.wicketkeeper?.Runs}</strong></div>
              <div>Dismissals: <strong>{(data.top_performers?.wicketkeeper?.Catches || 0) + (data.top_performers?.wicketkeeper?.Stumpings || 0)}</strong></div>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-grid">
        {/* Role Breakdown Pie Chart */}
        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="card-title">Role Distribution in Database</h3>
              <p className="card-description">Ratio of Batters, Bowlers, All-rounders & Keepers</p>
            </div>
          </div>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={roleChartData}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  innerRadius={50}
                  paddingAngle={4}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {roleChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={ROLE_COLORS[index % ROLE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Talent Tier Distribution */}
        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="card-title">Talent Grading Spectrum</h3>
              <p className="card-description">Composite talent score tier distribution</p>
            </div>
          </div>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <BarChart data={tierChartData}>
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" name="Players in Tier" fill="#0d6e38" radius={[6, 6, 0, 0]}>
                  {tierChartData.map((entry, index) => (
                    <Cell key={`tier-${index}`} fill={TIER_COLORS[index % TIER_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Quick Navigation Footer Banner */}
      <div className="card" style={{ background: 'linear-gradient(90deg, #0b192c 0%, #1e293b 100%)', color: 'white', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ fontSize: '1.1rem', fontWeight: '700' }}>Ready for Talent Scouting & Player Ranking?</h3>
          <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginTop: '4px' }}>
            Customize mathematical scoring weights and compare players head-to-head.
          </p>
        </div>
        <button
          className="btn btn-primary"
          onClick={() => onNavigate && onNavigate('scouting')}
        >
          <span>Explore Talent Scouting</span>
          <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
}
