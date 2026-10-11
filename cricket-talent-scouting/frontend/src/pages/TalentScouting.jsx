import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Sliders, RefreshCw, Award, Info, BookmarkPlus } from 'lucide-react';

export default function TalentScouting({ onSelectPlayer, onComparePlayer }) {
  const [role, setRole] = useState('Batter');
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState(null);

  // Dynamic Weights Configuration
  const [weights, setWeights] = useState({
    batter: { avg: 0.35, sr: 0.30, runs: 0.20, milestones: 0.15 },
    bowler: { avg: 0.30, econ: 0.30, wkts: 0.25, sr: 0.15 },
    allrounder: { bat: 0.50, bowl: 0.50 },
    wicketkeeper: { bat: 0.65, field: 0.35 },
  });

  useEffect(() => {
    fetchRankings();
  }, [role]);

  async function fetchRankings(customWeights = weights) {
    try {
      setLoading(true);
      const res = await api.getRankings(role, customWeights, 40);
      if (res.status === 'success') {
        setRankings(res.rankings);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  // Preset Configurations
  function applyPreset(presetName) {
    let newWeights = { ...weights };
    if (presetName === 't20') {
      newWeights = {
        batter: { avg: 0.20, sr: 0.50, runs: 0.15, milestones: 0.15 },
        bowler: { avg: 0.20, econ: 0.45, wkts: 0.20, sr: 0.15 },
        allrounder: { bat: 0.50, bowl: 0.50 },
        wicketkeeper: { bat: 0.60, field: 0.40 },
      };
    } else if (presetName === 'odi') {
      newWeights = {
        batter: { avg: 0.35, sr: 0.30, runs: 0.20, milestones: 0.15 },
        bowler: { avg: 0.30, econ: 0.30, wkts: 0.25, sr: 0.15 },
        allrounder: { bat: 0.50, bowl: 0.50 },
        wicketkeeper: { bat: 0.65, field: 0.35 },
      };
    } else if (presetName === 'test') {
      newWeights = {
        batter: { avg: 0.50, sr: 0.10, runs: 0.25, milestones: 0.15 },
        bowler: { avg: 0.35, econ: 0.15, wkts: 0.35, sr: 0.15 },
        allrounder: { bat: 0.50, bowl: 0.50 },
        wicketkeeper: { bat: 0.70, field: 0.30 },
      };
    }
    setWeights(newWeights);
    fetchRankings(newWeights);
  }

  async function handleShortlist(playerId, playerName) {
    try {
      await api.addToShortlist({
        player_id: playerId,
        target_role: role,
        priority_tier: 'High',
        scout_notes: `Scouted via Talent Engine (Score: ${rankings.find(r => r.Player_ID === playerId)?.Talent_Score || 'N/A'})`
      });
      setFeedback(`Shortlisted ${playerName}!`);
      setTimeout(() => setFeedback(null), 3000);
    } catch (err) {
      alert(`Shortlist failed: ${err.message}`);
    }
  }

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: '700' }}>Transparent Cricket Talent Scouting Engine</h3>
        <p style={{ color: '#64748b', fontSize: '0.86rem' }}>
          Configurable multi-metric mathematical normalization. Tune weights according to tournament format and scout objectives.
        </p>
      </div>

      {feedback && <div className="alert alert-success">{feedback}</div>}

      {/* Role Selection & Presets Bar */}
      <div className="filter-bar">
        <div className="filter-group">
          <span style={{ fontSize: '0.85rem', fontWeight: '600' }}>Scout Role:</span>
          {['Batter', 'Bowler', 'All-rounder', 'Wicketkeeper', 'all'].map((r) => (
            <button
              key={r}
              className={`btn btn-sm ${role === r ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setRole(r)}
            >
              {r === 'all' ? 'All Roles' : r}
            </button>
          ))}
        </div>

        <div className="filter-group">
          <span style={{ fontSize: '0.85rem', fontWeight: '600', color: '#64748b' }}>Format Presets:</span>
          <button className="btn btn-secondary btn-sm" onClick={() => applyPreset('t20')}>
            ⚡ T20 Franchise
          </button>
          <button className="btn btn-secondary btn-sm" onClick={() => applyPreset('odi')}>
            🏆 ODI Balanced
          </button>
          <button className="btn btn-secondary btn-sm" onClick={() => applyPreset('test')}>
            🛡️ Red-Ball Test
          </button>
        </div>
      </div>

      {/* Weight Customization Controls */}
      <div className="card">
        <div className="card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Sliders size={18} color="#0d6e38" />
            <h4 className="card-title">Adjust Scoring Coefficients ({role === 'all' ? 'Universal' : role})</h4>
          </div>
          <button className="btn btn-primary btn-sm" onClick={() => fetchRankings(weights)}>
            <RefreshCw size={14} />
            <span>Recalculate Scores</span>
          </button>
        </div>

        {role === 'Batter' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px' }}>
            <div className="slider-group">
              <div className="slider-label">
                <span>Batting Average (Consistency):</span>
                <span>{(weights.batter.avg * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.05"
                max="0.70"
                step="0.05"
                className="range-slider"
                value={weights.batter.avg}
                onChange={(e) => setWeights({
                  ...weights,
                  batter: { ...weights.batter, avg: parseFloat(e.target.value) }
                })}
              />
            </div>

            <div className="slider-group">
              <div className="slider-label">
                <span>Strike Rate (Tempo):</span>
                <span>{(weights.batter.sr * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.05"
                max="0.70"
                step="0.05"
                className="range-slider"
                value={weights.batter.sr}
                onChange={(e) => setWeights({
                  ...weights,
                  batter: { ...weights.batter, sr: parseFloat(e.target.value) }
                })}
              />
            </div>

            <div className="slider-group">
              <div className="slider-label">
                <span>Runs Volume (Log Scaled):</span>
                <span>{(weights.batter.runs * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.05"
                max="0.50"
                step="0.05"
                className="range-slider"
                value={weights.batter.runs}
                onChange={(e) => setWeights({
                  ...weights,
                  batter: { ...weights.batter, runs: parseFloat(e.target.value) }
                })}
              />
            </div>

            <div className="slider-group">
              <div className="slider-label">
                <span>Milestones (100s & 50s):</span>
                <span>{(weights.batter.milestones * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.05"
                max="0.40"
                step="0.05"
                className="range-slider"
                value={weights.batter.milestones}
                onChange={(e) => setWeights({
                  ...weights,
                  batter: { ...weights.batter, milestones: parseFloat(e.target.value) }
                })}
              />
            </div>
          </div>
        )}

        {role === 'Bowler' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px' }}>
            <div className="slider-group">
              <div className="slider-label">
                <span>Bowling Average (Runs/Wkt):</span>
                <span>{(weights.bowler.avg * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.05"
                max="0.60"
                step="0.05"
                className="range-slider"
                value={weights.bowler.avg}
                onChange={(e) => setWeights({
                  ...weights,
                  bowler: { ...weights.bowler, avg: parseFloat(e.target.value) }
                })}
              />
            </div>

            <div className="slider-group">
              <div className="slider-label">
                <span>Economy Rate (Control):</span>
                <span>{(weights.bowler.econ * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.05"
                max="0.60"
                step="0.05"
                className="range-slider"
                value={weights.bowler.econ}
                onChange={(e) => setWeights({
                  ...weights,
                  bowler: { ...weights.bowler, econ: parseFloat(e.target.value) }
                })}
              />
            </div>

            <div className="slider-group">
              <div className="slider-label">
                <span>Wickets Volume (Log Scaled):</span>
                <span>{(weights.bowler.wkts * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.05"
                max="0.50"
                step="0.05"
                className="range-slider"
                value={weights.bowler.wkts}
                onChange={(e) => setWeights({
                  ...weights,
                  bowler: { ...weights.bowler, wkts: parseFloat(e.target.value) }
                })}
              />
            </div>

            <div className="slider-group">
              <div className="slider-label">
                <span>Bowling Strike Rate (Balls/Wkt):</span>
                <span>{(weights.bowler.sr * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.05"
                max="0.40"
                step="0.05"
                className="range-slider"
                value={weights.bowler.sr}
                onChange={(e) => setWeights({
                  ...weights,
                  bowler: { ...weights.bowler, sr: parseFloat(e.target.value) }
                })}
              />
            </div>
          </div>
        )}

        {(role === 'All-rounder' || role === 'Wicketkeeper') && (
          <div style={{ padding: '10px 0', fontSize: '0.88rem', color: '#475569' }}>
            {role === 'All-rounder'
              ? 'All-Rounder Talent Score dynamically fuses 50% normalized Batting index with 50% normalized Bowling threat index.'
              : 'Wicketkeeper Talent Score fuses 65% Batting firepower with 35% fielding dismissals per match volume.'}
          </div>
        )}
      </div>

      {/* Leaderboard */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Talent Scouting Leaderboard ({role})</h3>
            <p className="card-description">Sorted by normalized multi-factor talent score (0-100 scale)</p>
          </div>
        </div>

        {loading ? (
          <div className="spinner-container">
            <div className="spinner"></div>
            <p>Computing talent scores...</p>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Player</th>
                  <th>Role</th>
                  <th>Country</th>
                  <th>Talent Score</th>
                  <th>Scout Tier</th>
                  <th>Key Statistics</th>
                  <th style={{ textAlign: 'center' }}>Scout Actions</th>
                </tr>
              </thead>
              <tbody>
                {rankings.map((r, idx) => {
                  let tierClass = 'tier4';
                  if (r.Talent_Score >= 75) tierClass = 'tier1';
                  else if (r.Talent_Score >= 55) tierClass = 'tier2';
                  else if (r.Talent_Score >= 40) tierClass = 'tier3';

                  return (
                    <tr key={r.Player_ID}>
                      <td style={{ fontWeight: '800', color: idx < 3 ? '#16a34a' : '#64748b' }}>
                        #{idx + 1}
                      </td>
                      <td style={{ fontWeight: '600' }}>
                        <span
                          style={{ cursor: 'pointer', color: '#0d6e38' }}
                          onClick={() => onSelectPlayer && onSelectPlayer(r.Player_ID)}
                        >
                          {r.Player}
                        </span>
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Age: {r.Age}</div>
                      </td>
                      <td>
                        <span className={`badge badge-${r.Role?.toLowerCase()?.replace('-', '')}`}>
                          {r.Role}
                        </span>
                      </td>
                      <td>{r.Country}</td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <span style={{ fontWeight: '800', fontSize: '1.05rem', color: '#0f172a' }}>
                            {r.Talent_Score}
                          </span>
                          <div style={{ width: '60px', height: '6px', background: '#e2e8f0', borderRadius: '4px', overflow: 'hidden' }}>
                            <div
                              style={{
                                width: `${r.Talent_Score}%`,
                                height: '100%',
                                background: r.Talent_Score >= 75 ? '#16a34a' : r.Talent_Score >= 55 ? '#0284c7' : '#f59e0b',
                              }}
                            />
                          </div>
                        </div>
                      </td>
                      <td>
                        <span className={`badge badge-${tierClass}`}>{r.Talent_Tier}</span>
                      </td>
                      <td style={{ fontSize: '0.82rem', color: '#475569' }}>
                        {r.Role === 'Batter' && (
                          <span>Avg: <strong>{r.Batting_Average}</strong> | SR: <strong>{r.Strike_Rate}</strong> | Runs: <strong>{r.Runs?.toLocaleString()}</strong></span>
                        )}
                        {r.Role === 'Bowler' && (
                          <span>Wkts: <strong>{r.Wickets}</strong> | Econ: <strong>{r.Economy_Rate}</strong> | Avg: <strong>{r.Bowling_Average}</strong></span>
                        )}
                        {r.Role === 'All-rounder' && (
                          <span>Runs: <strong>{r.Runs}</strong> | Wkts: <strong>{r.Wickets}</strong> | Econ: <strong>{r.Economy_Rate}</strong></span>
                        )}
                        {r.Role === 'Wicketkeeper' && (
                          <span>Runs: <strong>{r.Runs}</strong> | Catches: <strong>{r.Catches}</strong> | Stumpings: <strong>{r.Stumpings}</strong></span>
                        )}
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: '6px', justifyContent: 'center' }}>
                          <button
                            className="btn btn-secondary btn-sm"
                            title="Shortlist"
                            onClick={() => handleShortlist(r.Player_ID, r.Player)}
                          >
                            <BookmarkPlus size={14} color="#0284c7" />
                          </button>
                          <button
                            className="btn btn-secondary btn-sm"
                            title="Compare"
                            onClick={() => onComparePlayer && onComparePlayer(r.Player_ID)}
                          >
                            Compare
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
