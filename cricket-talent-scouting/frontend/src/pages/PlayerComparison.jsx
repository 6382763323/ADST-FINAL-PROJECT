import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import RadarChartComp from '../components/RadarChartComp';
import { GitCompare, Trophy, CheckCircle2 } from 'lucide-react';

export default function PlayerComparison({ initialP1, initialP2 }) {
  const [playerList, setPlayerList] = useState([]);
  const [p1Id, setP1Id] = useState(initialP1 || 'CRIC_001'); // Default Virat Kohli
  const [p2Id, setP2Id] = useState(initialP2 || 'CRIC_004'); // Default Steve Smith
  const [compData, setCompData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadPlayers();
  }, []);

  useEffect(() => {
    if (p1Id && p2Id) {
      runComparison(p1Id, p2Id);
    }
  }, [p1Id, p2Id]);

  async function loadPlayers() {
    try {
      const res = await api.getPlayers({ limit: 120, sort_by: 'runs' });
      if (res.status === 'success') {
        setPlayerList(res.players);
      }
    } catch (err) {
      console.error(err);
    }
  }

  async function runComparison(id1, id2) {
    if (id1 === id2) {
      setError('Please select two distinct players for head-to-head comparison.');
      setCompData(null);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const res = await api.comparePlayers(id1, id2);
      if (res.status === 'success') {
        setCompData(res.comparison);
      }
    } catch (err) {
      setError(err.message || 'Comparison failed.');
    } finally {
      setLoading(false);
    }
  }

  function handleQuickCompare(id1, id2) {
    setP1Id(id1);
    setP2Id(id2);
  }

  const p1 = compData?.player1;
  const p2 = compData?.player2;

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: '700' }}>Head-to-Head Player Comparison</h3>
        <p style={{ color: '#64748b', fontSize: '0.86rem' }}>
          Evaluate two players across standard performance metrics and 5-pillar radar scouting dimensions.
        </p>
      </div>

      {/* Preset Quick Matchups */}
      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '20px' }}>
        <span style={{ fontSize: '0.85rem', fontWeight: '600', color: '#64748b', alignSelf: 'center' }}>
          Classic Scouting Matchups:
        </span>
        <button
          className="btn btn-secondary btn-sm"
          onClick={() => handleQuickCompare('CRIC_001', 'CRIC_004')}
        >
          Virat Kohli vs Steve Smith
        </button>
        <button
          className="btn btn-secondary btn-sm"
          onClick={() => handleQuickCompare('CRIC_061', 'CRIC_062')}
        >
          Jasprit Bumrah vs Pat Cummins
        </button>
        <button
          className="btn btn-secondary btn-sm"
          onClick={() => handleQuickCompare('CRIC_041', 'CRIC_042')}
        >
          Ben Stokes vs Ravindra Jadeja
        </button>
        <button
          className="btn btn-secondary btn-sm"
          onClick={() => handleQuickCompare('CRIC_026', 'CRIC_027')}
        >
          MS Dhoni vs Jos Buttler
        </button>
      </div>

      {/* Selectors Bar */}
      <div className="filter-bar" style={{ display: 'grid', gridTemplateColumns: '1fr 60px 1fr', gap: '16px', alignItems: 'center' }}>
        <div>
          <label style={{ fontSize: '0.78rem', fontWeight: '700', color: '#16a34a', textTransform: 'uppercase' }}>
            Select Player A
          </label>
          <select
            className="select-control"
            style={{ width: '100%', marginTop: '4px' }}
            value={p1Id}
            onChange={(e) => setP1Id(e.target.value)}
          >
            {playerList.map((p) => (
              <option key={p.player_id} value={p.player_id}>
                {p.name} ({p.role} - {p.country})
              </option>
            ))}
          </select>
        </div>

        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <div style={{ background: '#f1f5f9', padding: '8px', borderRadius: '50%', color: '#64748b' }}>
            <GitCompare size={20} />
          </div>
        </div>

        <div>
          <label style={{ fontSize: '0.78rem', fontWeight: '700', color: '#0284c7', textTransform: 'uppercase' }}>
            Select Player B
          </label>
          <select
            className="select-control"
            style={{ width: '100%', marginTop: '4px' }}
            value={p2Id}
            onChange={(e) => setP2Id(e.target.value)}
          >
            {playerList.map((p) => (
              <option key={p.player_id} value={p.player_id}>
                {p.name} ({p.role} - {p.country})
              </option>
            ))}
          </select>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {loading ? (
        <div className="spinner-container">
          <div className="spinner"></div>
          <p>Analyzing head-to-head metrics...</p>
        </div>
      ) : compData && p1 && p2 ? (
        <div>
          {/* Side-by-Side Profiles */}
          <div className="compare-container">
            {/* Player 1 Card */}
            <div className="compare-card" style={{ borderColor: '#16a34a' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <span className="badge badge-tier1">Player A</span>
                  <h3 style={{ fontSize: '1.4rem', marginTop: '8px', color: '#0f172a' }}>{p1.Player}</h3>
                  <p style={{ color: '#64748b', fontSize: '0.85rem' }}>{p1.Country} • {p1.Role}</p>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', textTransform: 'uppercase' }}>Talent Score</div>
                  <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#16a34a' }}>{p1.Talent_Score}</div>
                  <span className="badge badge-tier1">{p1.Talent_Tier}</span>
                </div>
              </div>
            </div>

            {/* Player 2 Card */}
            <div className="compare-card" style={{ borderColor: '#0284c7' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <span className="badge badge-tier2">Player B</span>
                  <h3 style={{ fontSize: '1.4rem', marginTop: '8px', color: '#0f172a' }}>{p2.Player}</h3>
                  <p style={{ color: '#64748b', fontSize: '0.85rem' }}>{p2.Country} • {p2.Role}</p>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', textTransform: 'uppercase' }}>Talent Score</div>
                  <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#0284c7' }}>{p2.Talent_Score}</div>
                  <span className="badge badge-tier2">{p2.Talent_Tier}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Radar Chart Component */}
          <div className="card" style={{ marginTop: '24px' }}>
            <div className="card-header">
              <div>
                <h3 className="card-title">5-Pillar Scouting Radar Matrix</h3>
                <p className="card-description">
                  Dimensions: Batting Power (SR), Consistency (Avg), Bowling Threat (Bowl SR), Economy Control, Fielding Impact
                </p>
              </div>
            </div>
            <RadarChartComp
              p1Name={p1.Player}
              p1Radar={compData.p1_radar}
              p2Name={p2.Player}
              p2Radar={compData.p2_radar}
            />
          </div>

          {/* Metric Comparison Table */}
          <div className="card">
            <h3 className="card-title" style={{ marginBottom: '16px' }}>Detailed Head-to-Head Statistics</h3>
            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Performance Metric</th>
                    <th style={{ color: '#16a34a', fontWeight: '700' }}>{p1.Player}</th>
                    <th style={{ color: '#0284c7', fontWeight: '700' }}>{p2.Player}</th>
                    <th>Scout Advantage</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    { label: 'Matches Played', key: 'Matches', higherBetter: true },
                    { label: 'Total Runs', key: 'Runs', higherBetter: true },
                    { label: 'Batting Average', key: 'Batting_Average', higherBetter: true },
                    { label: 'Strike Rate', key: 'Strike_Rate', higherBetter: true },
                    { label: 'Centuries', key: 'Centuries', higherBetter: true },
                    { label: 'Fifties', key: 'Fifties', higherBetter: true },
                    { label: 'Highest Score', key: 'Highest_Score', higherBetter: true },
                    { label: 'Total Wickets', key: 'Wickets', higherBetter: true },
                    { label: 'Economy Rate', key: 'Economy_Rate', higherBetter: false },
                    { label: 'Bowling Average', key: 'Bowling_Average', higherBetter: false },
                    { label: 'Catches / Stumpings', key: 'Catches', higherBetter: true },
                  ].map((item) => {
                    const v1 = p1[item.key] ?? 0;
                    const v2 = p2[item.key] ?? 0;
                    let winner = 'Equal';
                    if (v1 !== v2) {
                      if (item.higherBetter) {
                        winner = v1 > v2 ? p1.Player : p2.Player;
                      } else {
                        // For economy or bowling average, lower is better (if > 0)
                        if (v1 > 0 && v2 > 0) {
                          winner = v1 < v2 ? p1.Player : p2.Player;
                        } else if (v1 > 0) {
                          winner = p1.Player;
                        } else if (v2 > 0) {
                          winner = p2.Player;
                        }
                      }
                    }

                    return (
                      <tr key={item.key}>
                        <td style={{ fontWeight: '600', color: '#475569' }}>{item.label}</td>
                        <td style={{ fontWeight: winner === p1.Player ? '700' : 'normal', color: winner === p1.Player ? '#16a34a' : 'inherit' }}>
                          {typeof v1 === 'number' ? v1.toLocaleString() : v1}
                        </td>
                        <td style={{ fontWeight: winner === p2.Player ? '700' : 'normal', color: winner === p2.Player ? '#0284c7' : 'inherit' }}>
                          {typeof v2 === 'number' ? v2.toLocaleString() : v2}
                        </td>
                        <td>
                          {winner !== 'Equal' ? (
                            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', color: winner === p1.Player ? '#16a34a' : '#0284c7', fontWeight: '600' }}>
                              <CheckCircle2 size={14} /> {winner}
                            </span>
                          ) : (
                            <span style={{ color: '#94a3b8' }}>Tied</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
