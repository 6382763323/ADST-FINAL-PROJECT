import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { UserCheck, Shield, Award, Target, Brain, BookmarkPlus, AlertCircle } from 'lucide-react';

export default function PlayerProfile({ playerId = 'CRIC_001', onComparePlayer }) {
  const [selectedId, setSelectedId] = useState(playerId);
  const [playerList, setPlayerList] = useState([]);
  const [player, setPlayer] = useState(null);
  const [mlPrediction, setMlPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState(null);

  useEffect(() => {
    loadPlayerDirectory();
  }, []);

  useEffect(() => {
    if (selectedId) {
      loadProfile(selectedId);
    }
  }, [selectedId]);

  async function loadPlayerDirectory() {
    try {
      const res = await api.getPlayers({ limit: 120 });
      if (res.status === 'success') {
        setPlayerList(res.players);
      }
    } catch (err) {
      console.error(err);
    }
  }

  async function loadProfile(id) {
    try {
      setLoading(true);
      const res = await api.getPlayerById(id);
      if (res.status === 'success') {
        setPlayer(res.player);
        // Run ML Prediction for this player
        fetchMlPrediction(res.player);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function fetchMlPrediction(pData) {
    try {
      const mlRes = await api.predictTier(pData);
      if (mlRes.status === 'success') {
        setMlPrediction(mlRes.prediction);
      }
    } catch (err) {
      console.error('ML inference note:', err);
    }
  }

  async function handleShortlist() {
    if (!player) return;
    try {
      await api.addToShortlist({
        player_id: player.player_id,
        target_role: player.role,
        priority_tier: 'High Priority',
        scout_notes: `Shortlisted from Individual Profile view`
      });
      setFeedback(`Added ${player.name} to Scouting Shortlist!`);
      setTimeout(() => setFeedback(null), 3000);
    } catch (err) {
      alert(`Shortlist failed: ${err.message}`);
    }
  }

  if (loading && !player) {
    return (
      <div className="spinner-container">
        <div className="spinner"></div>
        <p>Loading Player Profile...</p>
      </div>
    );
  }

  return (
    <div>
      {/* Player Selector Bar */}
      <div className="filter-bar">
        <div className="filter-group">
          <span style={{ fontSize: '0.85rem', fontWeight: '600' }}>Select Player Profile:</span>
          <select
            className="select-control"
            value={selectedId}
            onChange={(e) => setSelectedId(e.target.value)}
          >
            {playerList.map((p) => (
              <option key={p.player_id} value={p.player_id}>
                {p.name} ({p.role} - {p.country})
              </option>
            ))}
          </select>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button className="btn btn-secondary btn-sm" onClick={handleShortlist}>
            <BookmarkPlus size={14} color="#0284c7" />
            <span>Shortlist Player</span>
          </button>
          {onComparePlayer && (
            <button
              className="btn btn-primary btn-sm"
              onClick={() => onComparePlayer(player?.player_id)}
            >
              Compare with Another
            </button>
          )}
        </div>
      </div>

      {feedback && <div className="alert alert-success">{feedback}</div>}

      {player && (
        <div>
          {/* Hero Profile Card */}
          <div className="card" style={{ background: 'linear-gradient(135deg, #0b192c 0%, #1e293b 100%)', color: 'white' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '20px' }}>
              <div>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <span className="badge badge-batter">{player.role}</span>
                  <span style={{ color: '#94a3b8', fontSize: '0.82rem' }}>ID: {player.player_id}</span>
                </div>
                <h2 style={{ fontSize: '2rem', fontWeight: '800', marginTop: '10px' }}>{player.name}</h2>
                <p style={{ color: '#cbd5e1', fontSize: '0.95rem' }}>
                  {player.country} • Age: {player.age} • Batting: {player.batting_style} • Bowling: {player.bowling_style}
                </p>
              </div>

              <div style={{ display: 'flex', gap: '20px', background: 'rgba(255, 255, 255, 0.08)', padding: '16px 24px', borderRadius: '12px' }}>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase' }}>Matches</div>
                  <div style={{ fontSize: '1.4rem', fontWeight: '800' }}>{player.matches}</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase' }}>Innings</div>
                  <div style={{ fontSize: '1.4rem', fontWeight: '800' }}>{player.innings}</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase' }}>Runs</div>
                  <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#4ade80' }}>{player.runs?.toLocaleString()}</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase' }}>Wickets</div>
                  <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#38bdf8' }}>{player.wickets}</div>
                </div>
              </div>
            </div>
          </div>

          {/* Stats Sections Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px', marginBottom: '24px' }}>
            {/* Batting Card */}
            <div className="card">
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
                <Award size={20} color="#16a34a" />
                <h4 className="card-title">Batting Profile</h4>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                <div style={{ padding: '12px', background: '#f8fafc', borderRadius: '8px' }}>
                  <div style={{ fontSize: '0.78rem', color: '#64748b' }}>Batting Average</div>
                  <div style={{ fontSize: '1.3rem', fontWeight: '700', color: '#0f172a' }}>{player.batting_avg}</div>
                </div>
                <div style={{ padding: '12px', background: '#f8fafc', borderRadius: '8px' }}>
                  <div style={{ fontSize: '0.78rem', color: '#64748b' }}>Strike Rate</div>
                  <div style={{ fontSize: '1.3rem', fontWeight: '700', color: '#0f172a' }}>{player.strike_rate}</div>
                </div>
                <div style={{ padding: '12px', background: '#f8fafc', borderRadius: '8px' }}>
                  <div style={{ fontSize: '0.78rem', color: '#64748b' }}>Highest Score</div>
                  <div style={{ fontSize: '1.3rem', fontWeight: '700', color: '#0f172a' }}>{player.highest_score}</div>
                </div>
                <div style={{ padding: '12px', background: '#f8fafc', borderRadius: '8px' }}>
                  <div style={{ fontSize: '0.78rem', color: '#64748b' }}>Centuries / 50s</div>
                  <div style={{ fontSize: '1.3rem', fontWeight: '700', color: '#0f172a' }}>{player.centuries} / {player.fifties}</div>
                </div>
              </div>
            </div>

            {/* Bowling Card */}
            <div className="card">
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
                <Target size={20} color="#0284c7" />
                <h4 className="card-title">Bowling Profile</h4>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                <div style={{ padding: '12px', background: '#f8fafc', borderRadius: '8px' }}>
                  <div style={{ fontSize: '0.78rem', color: '#64748b' }}>Total Wickets</div>
                  <div style={{ fontSize: '1.3rem', fontWeight: '700', color: '#0f172a' }}>{player.wickets}</div>
                </div>
                <div style={{ padding: '12px', background: '#f8fafc', borderRadius: '8px' }}>
                  <div style={{ fontSize: '0.78rem', color: '#64748b' }}>Economy Rate</div>
                  <div style={{ fontSize: '1.3rem', fontWeight: '700', color: '#0f172a' }}>{player.economy_rate > 0 ? player.economy_rate : '-'}</div>
                </div>
                <div style={{ padding: '12px', background: '#f8fafc', borderRadius: '8px' }}>
                  <div style={{ fontSize: '0.78rem', color: '#64748b' }}>Bowling Average</div>
                  <div style={{ fontSize: '1.3rem', fontWeight: '700', color: '#0f172a' }}>{player.bowling_avg > 0 ? player.bowling_avg : '-'}</div>
                </div>
                <div style={{ padding: '12px', background: '#f8fafc', borderRadius: '8px' }}>
                  <div style={{ fontSize: '0.78rem', color: '#64748b' }}>Best Bowling</div>
                  <div style={{ fontSize: '1.3rem', fontWeight: '700', color: '#0f172a' }}>{player.best_bowling}</div>
                </div>
              </div>
            </div>

            {/* Fielding Card */}
            <div className="card">
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
                <Shield size={20} color="#f59e0b" />
                <h4 className="card-title">Fielding & Dismissals</h4>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                <div style={{ padding: '12px', background: '#f8fafc', borderRadius: '8px' }}>
                  <div style={{ fontSize: '0.78rem', color: '#64748b' }}>Catches Taken</div>
                  <div style={{ fontSize: '1.3rem', fontWeight: '700', color: '#0f172a' }}>{player.catches}</div>
                </div>
                <div style={{ padding: '12px', background: '#f8fafc', borderRadius: '8px' }}>
                  <div style={{ fontSize: '0.78rem', color: '#64748b' }}>Stumpings</div>
                  <div style={{ fontSize: '1.3rem', fontWeight: '700', color: '#0f172a' }}>{player.stumpings}</div>
                </div>
              </div>
            </div>
          </div>

          {/* Machine Learning Scout Classification Widget */}
          {mlPrediction && (
            <div className="card" style={{ border: '2px solid #86efac', background: '#f0fdf4' }}>
              <div className="card-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Brain size={22} color="#16a34a" />
                  <div>
                    <h3 className="card-title" style={{ color: '#14532d' }}>
                      Machine Learning Talent Tier Prediction: {mlPrediction.predicted_tier}
                    </h3>
                    <p className="card-description" style={{ color: '#166534' }}>
                      Inference generated via Scikit-learn Random Forest Classifier Pipeline
                    </p>
                  </div>
                </div>
                <span className="badge badge-tier1" style={{ fontSize: '0.85rem' }}>
                  {mlPrediction.predicted_tier}
                </span>
              </div>

              {/* Probabilities Distribution */}
              <div style={{ marginBottom: '16px' }}>
                <div style={{ fontSize: '0.82rem', fontWeight: '600', color: '#166534', marginBottom: '8px' }}>
                  Model Confidence Distribution:
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
                  {Object.entries(mlPrediction.probabilities || {}).map(([cls, prob]) => (
                    <div key={cls} style={{ background: 'white', padding: '10px 14px', borderRadius: '8px', border: '1px solid #bbf7d0' }}>
                      <div style={{ fontSize: '0.75rem', color: '#475569' }}>{cls}</div>
                      <div style={{ fontSize: '1.2rem', fontWeight: '700', color: '#0f172a' }}>{prob}%</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Disclaimer */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#15803d', fontSize: '0.8rem' }}>
                <AlertCircle size={16} />
                <span>{mlPrediction.disclaimer}</span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
