import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ScatterChart,
  Scatter,
  ZAxis
} from 'recharts';
import { Award, Target, Shield, Zap } from 'lucide-react';

export default function PerformanceAnalysis({ onSelectPlayer }) {
  const [activeSegment, setActiveSegment] = useState('batting');
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      setLoading(true);
      const res = await api.getPlayers({ limit: 120, sort_by: 'runs', order: 'desc' });
      if (res.status === 'success') {
        setPlayers(res.players);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="spinner-container">
        <div className="spinner"></div>
        <p>Loading Cricket Performance Analytics...</p>
      </div>
    );
  }

  // Segment data
  const battersList = [...players]
    .filter((p) => p.runs >= 100)
    .sort((a, b) => b.runs - a.runs)
    .slice(0, 10);

  const bowlersList = [...players]
    .filter((p) => p.wickets >= 10)
    .sort((a, b) => b.wickets - a.wickets)
    .slice(0, 10);

  const fieldersList = [...players]
    .map((p) => ({ ...p, total_dismissals: p.catches + p.stumpings }))
    .sort((a, b) => b.total_dismissals - a.total_dismissals)
    .slice(0, 10);

  return (
    <div>
      {/* Segment Selector Tabs */}
      <div style={{ display: 'flex', gap: '12px', marginBottom: '24px' }}>
        <button
          className={`btn ${activeSegment === 'batting' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveSegment('batting')}
        >
          <Award size={16} />
          <span>Batting Performance</span>
        </button>
        <button
          className={`btn ${activeSegment === 'bowling' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveSegment('bowling')}
        >
          <Target size={16} />
          <span>Bowling Performance</span>
        </button>
        <button
          className={`btn ${activeSegment === 'fielding' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveSegment('fielding')}
        >
          <Shield size={16} />
          <span>Fielding & Dismissals</span>
        </button>
      </div>

      {/* BATTING SEGMENT */}
      {activeSegment === 'batting' && (
        <div>
          <div className="card">
            <div className="card-header">
              <div>
                <h3 className="card-title">Top 10 Run Scorers (Runs vs Batting Average)</h3>
                <p className="card-description">Scoring volume compared with average consistency</p>
              </div>
            </div>
            <div style={{ width: '100%', height: 320 }}>
              <ResponsiveContainer>
                <BarChart data={battersList} margin={{ top: 10, right: 30, left: 20, bottom: 30 }}>
                  <XAxis dataKey="name" angle={-25} textAnchor="end" interval={0} height={60} tick={{ fontSize: 12 }} />
                  <YAxis yAxisId="left" orientation="left" stroke="#0d6e38" />
                  <YAxis yAxisId="right" orientation="right" stroke="#f59e0b" />
                  <Tooltip />
                  <Legend />
                  <Bar yAxisId="left" dataKey="runs" name="Career Runs" fill="#16a34a" radius={[4, 4, 0, 0]} />
                  <Bar yAxisId="right" dataKey="batting_avg" name="Batting Avg" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card">
            <h3 className="card-title" style={{ marginBottom: '16px' }}>Batting Leaderboard Summary</h3>
            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Player</th>
                    <th>Country</th>
                    <th>Runs</th>
                    <th>Avg</th>
                    <th>Strike Rate</th>
                    <th>100s / 50s</th>
                    <th>Highest Score</th>
                  </tr>
                </thead>
                <tbody>
                  {battersList.map((p, idx) => (
                    <tr key={p.player_id} onClick={() => onSelectPlayer && onSelectPlayer(p.player_id)} style={{ cursor: 'pointer' }}>
                      <td style={{ fontWeight: '700', color: '#16a34a' }}>#{idx + 1}</td>
                      <td style={{ fontWeight: '600' }}>{p.name}</td>
                      <td>{p.country}</td>
                      <td style={{ fontWeight: '700' }}>{p.runs?.toLocaleString()}</td>
                      <td>{p.batting_avg}</td>
                      <td style={{ color: p.strike_rate >= 120 ? '#16a34a' : 'inherit' }}>{p.strike_rate}</td>
                      <td>{p.centuries} / {p.fifties}</td>
                      <td>{p.highest_score}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* BOWLING SEGMENT */}
      {activeSegment === 'bowling' && (
        <div>
          <div className="card">
            <div className="card-header">
              <div>
                <h3 className="card-title">Top 10 Wicket Takers (Wickets vs Economy Rate)</h3>
                <p className="card-description">Dismissal volume compared with runs conceded per over</p>
              </div>
            </div>
            <div style={{ width: '100%', height: 320 }}>
              <ResponsiveContainer>
                <BarChart data={bowlersList} margin={{ top: 10, right: 30, left: 20, bottom: 30 }}>
                  <XAxis dataKey="name" angle={-25} textAnchor="end" interval={0} height={60} tick={{ fontSize: 12 }} />
                  <YAxis yAxisId="left" orientation="left" stroke="#0284c7" />
                  <YAxis yAxisId="right" orientation="right" stroke="#dc2626" />
                  <Tooltip />
                  <Legend />
                  <Bar yAxisId="left" dataKey="wickets" name="Wickets" fill="#0284c7" radius={[4, 4, 0, 0]} />
                  <Bar yAxisId="right" dataKey="economy_rate" name="Economy Rate" fill="#dc2626" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card">
            <h3 className="card-title" style={{ marginBottom: '16px' }}>Bowling Leaderboard Summary</h3>
            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Player</th>
                    <th>Country</th>
                    <th>Wickets</th>
                    <th>Economy Rate</th>
                    <th>Bowling Avg</th>
                    <th>Bowling SR</th>
                    <th>Best Bowling</th>
                  </tr>
                </thead>
                <tbody>
                  {bowlersList.map((p, idx) => (
                    <tr key={p.player_id} onClick={() => onSelectPlayer && onSelectPlayer(p.player_id)} style={{ cursor: 'pointer' }}>
                      <td style={{ fontWeight: '700', color: '#0284c7' }}>#{idx + 1}</td>
                      <td style={{ fontWeight: '600' }}>{p.name}</td>
                      <td>{p.country}</td>
                      <td style={{ fontWeight: '700' }}>{p.wickets}</td>
                      <td>{p.economy_rate}</td>
                      <td>{p.bowling_avg}</td>
                      <td>{p.bowling_sr}</td>
                      <td>{p.best_bowling}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* FIELDING SEGMENT */}
      {activeSegment === 'fielding' && (
        <div>
          <div className="card">
            <div className="card-header">
              <div>
                <h3 className="card-title">Top 10 Dismissals Breakdown (Catches + Stumpings)</h3>
                <p className="card-description">Fielding impact and wicketkeeper contribution</p>
              </div>
            </div>
            <div style={{ width: '100%', height: 320 }}>
              <ResponsiveContainer>
                <BarChart data={fieldersList} margin={{ top: 10, right: 30, left: 20, bottom: 30 }}>
                  <XAxis dataKey="name" angle={-25} textAnchor="end" interval={0} height={60} tick={{ fontSize: 12 }} />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="catches" stackId="a" name="Catches" fill="#16a34a" />
                  <Bar dataKey="stumpings" stackId="a" name="Stumpings" fill="#7e22ce" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card">
            <h3 className="card-title" style={{ marginBottom: '16px' }}>Fielding Leaderboard Summary</h3>
            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Player</th>
                    <th>Role</th>
                    <th>Country</th>
                    <th>Catches</th>
                    <th>Stumpings</th>
                    <th>Total Dismissals</th>
                  </tr>
                </thead>
                <tbody>
                  {fieldersList.map((p, idx) => (
                    <tr key={p.player_id} onClick={() => onSelectPlayer && onSelectPlayer(p.player_id)} style={{ cursor: 'pointer' }}>
                      <td style={{ fontWeight: '700', color: '#16a34a' }}>#{idx + 1}</td>
                      <td style={{ fontWeight: '600' }}>{p.name}</td>
                      <td>
                        <span className={`badge badge-${p.role?.toLowerCase()?.replace('-', '')}`}>
                          {p.role}
                        </span>
                      </td>
                      <td>{p.country}</td>
                      <td>{p.catches}</td>
                      <td>{p.stumpings}</td>
                      <td style={{ fontWeight: '700' }}>{p.total_dismissals}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
