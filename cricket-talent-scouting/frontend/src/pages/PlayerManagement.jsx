import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import PlayerFilter from '../components/PlayerFilter';
import { Plus, Edit2, Trash2, BookmarkPlus, Eye, X } from 'lucide-react';

export default function PlayerManagement({ onSelectPlayer, onComparePlayer }) {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [feedback, setFeedback] = useState(null);

  // Filters
  const [search, setSearch] = useState('');
  const [role, setRole] = useState('all');
  const [country, setCountry] = useState('all');
  const [sortBy, setSortBy] = useState('runs');
  const [order, setOrder] = useState('desc');

  // Modal State for Add/Edit
  const [showModal, setShowModal] = useState(false);
  const [editingPlayer, setEditingPlayer] = useState(null);
  const [formData, setFormData] = useState({
    player_id: '',
    name: '',
    country: 'India',
    role: 'Batter',
    batting_style: 'Right-hand bat',
    bowling_style: 'Right-arm medium',
    age: 24,
    matches: 10,
    innings: 10,
    runs: 350,
    highest_score: 85,
    batting_avg: 38.5,
    strike_rate: 135.0,
    centuries: 0,
    fifties: 2,
    wickets: 0,
    bowling_avg: 0.0,
    economy_rate: 0.0,
    bowling_sr: 0.0,
    best_bowling: '-',
    catches: 5,
    stumpings: 0,
  });

  useEffect(() => {
    loadPlayers();
  }, [search, role, country, sortBy, order]);

  async function loadPlayers() {
    try {
      setLoading(true);
      const res = await api.getPlayers({
        search,
        role,
        country,
        sort_by: sortBy,
        order,
      });
      if (res.status === 'success') {
        setPlayers(res.players);
      }
    } catch (err) {
      setError(err.message || 'Failed to fetch players.');
    } finally {
      setLoading(false);
    }
  }

  function handleOpenCreate() {
    setEditingPlayer(null);
    setFormData({
      player_id: `CRIC_${Date.now().toString().slice(-4)}`,
      name: '',
      country: 'India',
      role: 'Batter',
      batting_style: 'Right-hand bat',
      bowling_style: '-',
      age: 23,
      matches: 15,
      innings: 14,
      runs: 480,
      highest_score: 92,
      batting_avg: 40.0,
      strike_rate: 138.5,
      centuries: 0,
      fifties: 3,
      wickets: 0,
      bowling_avg: 0.0,
      economy_rate: 0.0,
      bowling_sr: 0.0,
      best_bowling: '-',
      catches: 6,
      stumpings: 0,
    });
    setShowModal(true);
  }

  function handleOpenEdit(player) {
    setEditingPlayer(player.player_id);
    setFormData({ ...player });
    setShowModal(true);
  }

  async function handleSubmitForm(e) {
    e.preventDefault();
    if (!formData.name.trim()) {
      alert('Player name cannot be empty.');
      return;
    }

    try {
      if (editingPlayer) {
        await api.updatePlayer(editingPlayer, formData);
        setFeedback(`Player ${formData.name} updated successfully.`);
      } else {
        await api.createPlayer(formData);
        setFeedback(`Player ${formData.name} added successfully.`);
      }
      setShowModal(false);
      loadPlayers();
      setTimeout(() => setFeedback(null), 4000);
    } catch (err) {
      alert(`Save failed: ${err.message}`);
    }
  }

  async function handleDelete(playerId, playerName) {
    if (window.confirm(`Are you sure you want to delete ${playerName} (${playerId})?`)) {
      try {
        await api.deletePlayer(playerId);
        setFeedback(`Player ${playerName} deleted.`);
        loadPlayers();
        setTimeout(() => setFeedback(null), 4000);
      } catch (err) {
        alert(`Delete failed: ${err.message}`);
      }
    }
  }

  async function handleShortlist(playerId, playerName) {
    try {
      await api.addToShortlist({
        player_id: playerId,
        target_role: 'Priority Scout',
        priority_tier: 'High',
        scout_notes: 'Shortlisted from Player Management view'
      });
      setFeedback(`Added ${playerName} to Scouting Shortlist.`);
      setTimeout(() => setFeedback(null), 3000);
    } catch (err) {
      alert(`Shortlist action failed: ${err.message}`);
    }
  }

  return (
    <div>
      {/* Top action header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div>
          <h3 style={{ fontSize: '1.2rem', fontWeight: '700' }}>Player Records Directory</h3>
          <p style={{ color: '#64748b', fontSize: '0.85rem' }}>
            Manage, inspect, search, and edit cricket player profiles and performance metrics.
          </p>
        </div>
        <button className="btn btn-primary" onClick={handleOpenCreate}>
          <Plus size={16} />
          <span>Add New Player</span>
        </button>
      </div>

      {feedback && <div className="alert alert-success">{feedback}</div>}
      {error && <div className="alert alert-error">{error}</div>}

      {/* Filter Component */}
      <PlayerFilter
        search={search}
        setSearch={setSearch}
        role={role}
        setRole={setRole}
        country={country}
        setCountry={setCountry}
        sortBy={sortBy}
        setSortBy={setSortBy}
        order={order}
        setOrder={setOrder}
        onReset={() => {
          setSearch('');
          setRole('all');
          setCountry('all');
          setSortBy('runs');
          setOrder('desc');
        }}
      />

      {/* Table */}
      <div className="card">
        {loading ? (
          <div className="spinner-container">
            <div className="spinner"></div>
            <p>Loading player records...</p>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Player ID</th>
                  <th>Player</th>
                  <th>Country</th>
                  <th>Role</th>
                  <th>Matches</th>
                  <th>Runs</th>
                  <th>Bat Avg</th>
                  <th>SR</th>
                  <th>Wickets</th>
                  <th>Bowl Econ</th>
                  <th>Catches</th>
                  <th style={{ textAlign: 'center' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {players.length === 0 ? (
                  <tr>
                    <td colSpan="12" style={{ textAlign: 'center', padding: '30px', color: '#64748b' }}>
                      No players matching current criteria.
                    </td>
                  </tr>
                ) : (
                  players.map((p) => (
                    <tr key={p.player_id}>
                      <td style={{ fontFamily: 'monospace', fontSize: '0.8rem', color: '#64748b' }}>
                        {p.player_id}
                      </td>
                      <td style={{ fontWeight: '600' }}>
                        <span
                          style={{ cursor: 'pointer', color: '#0d6e38' }}
                          onClick={() => onSelectPlayer && onSelectPlayer(p.player_id)}
                        >
                          {p.name}
                        </span>
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Age: {p.age}</div>
                      </td>
                      <td>{p.country}</td>
                      <td>
                        <span className={`badge badge-${p.role?.toLowerCase()?.replace('-', '')}`}>
                          {p.role}
                        </span>
                      </td>
                      <td>{p.matches}</td>
                      <td style={{ fontWeight: '600' }}>{p.runs?.toLocaleString()}</td>
                      <td>{p.batting_avg}</td>
                      <td>{p.strike_rate}</td>
                      <td style={{ fontWeight: '600', color: p.wickets > 0 ? '#15803d' : '#94a3b8' }}>
                        {p.wickets}
                      </td>
                      <td>{p.economy_rate > 0 ? p.economy_rate : '-'}</td>
                      <td>{p.catches}</td>
                      <td>
                        <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                          <button
                            title="View Full Profile"
                            className="btn btn-secondary btn-sm"
                            onClick={() => onSelectPlayer && onSelectPlayer(p.player_id)}
                          >
                            <Eye size={14} />
                          </button>
                          <button
                            title="Add to Shortlist"
                            className="btn btn-secondary btn-sm"
                            onClick={() => handleShortlist(p.player_id, p.name)}
                          >
                            <BookmarkPlus size={14} color="#0284c7" />
                          </button>
                          <button
                            title="Edit Record"
                            className="btn btn-secondary btn-sm"
                            onClick={() => handleOpenEdit(p)}
                          >
                            <Edit2 size={14} />
                          </button>
                          <button
                            title="Delete Record"
                            className="btn btn-secondary btn-sm"
                            style={{ color: '#ef4444' }}
                            onClick={() => handleDelete(p.player_id, p.name)}
                          >
                            <Trash2 size={14} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Add / Edit Modal */}
      {showModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h3 style={{ fontSize: '1.2rem', fontWeight: '700' }}>
                {editingPlayer ? 'Edit Player Record' : 'Register New Player'}
              </h3>
              <button
                style={{ background: 'none', border: 'none', cursor: 'pointer' }}
                onClick={() => setShowModal(false)}
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleSubmitForm}>
              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">Player ID</label>
                  <input
                    type="text"
                    className="form-input"
                    value={formData.player_id}
                    disabled={!!editingPlayer}
                    onChange={(e) => setFormData({ ...formData, player_id: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Full Name *</label>
                  <input
                    type="text"
                    required
                    className="form-input"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Country / Team *</label>
                  <input
                    type="text"
                    required
                    className="form-input"
                    value={formData.country}
                    onChange={(e) => setFormData({ ...formData, country: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Role *</label>
                  <select
                    className="form-input"
                    value={formData.role}
                    onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                  >
                    <option value="Batter">Batter</option>
                    <option value="Bowler">Bowler</option>
                    <option value="All-rounder">All-rounder</option>
                    <option value="Wicketkeeper">Wicketkeeper</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Age</label>
                  <input
                    type="number"
                    className="form-input"
                    value={formData.age}
                    onChange={(e) => setFormData({ ...formData, age: Number(e.target.value) })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Matches</label>
                  <input
                    type="number"
                    className="form-input"
                    value={formData.matches}
                    onChange={(e) => setFormData({ ...formData, matches: Number(e.target.value) })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Total Runs</label>
                  <input
                    type="number"
                    className="form-input"
                    value={formData.runs}
                    onChange={(e) => setFormData({ ...formData, runs: Number(e.target.value) })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Batting Average</label>
                  <input
                    type="number"
                    step="0.01"
                    className="form-input"
                    value={formData.batting_avg}
                    onChange={(e) => setFormData({ ...formData, batting_avg: Number(e.target.value) })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Strike Rate</label>
                  <input
                    type="number"
                    step="0.01"
                    className="form-input"
                    value={formData.strike_rate}
                    onChange={(e) => setFormData({ ...formData, strike_rate: Number(e.target.value) })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Centuries / 50s</label>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <input
                      type="number"
                      placeholder="100s"
                      className="form-input"
                      value={formData.centuries}
                      onChange={(e) => setFormData({ ...formData, centuries: Number(e.target.value) })}
                    />
                    <input
                      type="number"
                      placeholder="50s"
                      className="form-input"
                      value={formData.fifties}
                      onChange={(e) => setFormData({ ...formData, fifties: Number(e.target.value) })}
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Wickets</label>
                  <input
                    type="number"
                    className="form-input"
                    value={formData.wickets}
                    onChange={(e) => setFormData({ ...formData, wickets: Number(e.target.value) })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Economy Rate</label>
                  <input
                    type="number"
                    step="0.01"
                    className="form-input"
                    value={formData.economy_rate}
                    onChange={(e) => setFormData({ ...formData, economy_rate: Number(e.target.value) })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Catches / Stumpings</label>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <input
                      type="number"
                      placeholder="Catches"
                      className="form-input"
                      value={formData.catches}
                      onChange={(e) => setFormData({ ...formData, catches: Number(e.target.value) })}
                    />
                    <input
                      type="number"
                      placeholder="Stumpings"
                      className="form-input"
                      value={formData.stumpings}
                      onChange={(e) => setFormData({ ...formData, stumpings: Number(e.target.value) })}
                    />
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '24px' }}>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingPlayer ? 'Save Changes' : 'Create Player'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
