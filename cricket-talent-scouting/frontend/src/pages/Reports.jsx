import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Download, FileSpreadsheet, Trash2, BookmarkCheck, CheckCircle } from 'lucide-react';

export default function Reports() {
  const [shortlist, setShortlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState(null);

  useEffect(() => {
    loadShortlist();
  }, []);

  async function loadShortlist() {
    try {
      setLoading(true);
      const res = await api.getShortlist();
      if (res.status === 'success') {
        setShortlist(res.shortlist);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleRemove(id) {
    try {
      await api.removeFromShortlist(id);
      setFeedback('Removed player from scouting shortlist.');
      loadShortlist();
      setTimeout(() => setFeedback(null), 3000);
    } catch (err) {
      alert(`Removal failed: ${err.message}`);
    }
  }

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: '700' }}>Scouting Reports & Export Center</h3>
        <p style={{ color: '#64748b', fontSize: '0.86rem' }}>
          Manage your scouted shortlist candidates and export complete data intelligence in standard CSV format.
        </p>
      </div>

      {feedback && <div className="alert alert-success">{feedback}</div>}

      {/* Export Action Card */}
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px', background: 'linear-gradient(90deg, #f0fdf4 0%, #ffffff 100%)', border: '1px solid #bbf7d0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ background: '#dcfce7', padding: '14px', borderRadius: '12px', color: '#16a34a' }}>
            <FileSpreadsheet size={28} />
          </div>
          <div>
            <h4 style={{ fontSize: '1.1rem', fontWeight: '700', color: '#14532d' }}>
              Export Master Talent Scouting CSV Report
            </h4>
            <p style={{ fontSize: '0.85rem', color: '#166534' }}>
              Includes all cleaned player metrics, normalized Batter and Bowler talent indices, and assigned tiers.
            </p>
          </div>
        </div>

        <a
          href={api.getExportCsvUrl()}
          download="cricket_talent_scouting_report.csv"
          className="btn btn-primary"
          style={{ textDecoration: 'none' }}
        >
          <Download size={16} />
          <span>Download Master CSV Report</span>
        </a>
      </div>

      {/* Scouting Shortlist Management Table */}
      <div className="card">
        <div className="card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <BookmarkCheck size={20} color="#0d6e38" />
            <h3 className="card-title">Scouting Shortlist & Priority Targets</h3>
          </div>
          <span className="badge badge-tier1">{shortlist.length} Shortlisted Targets</span>
        </div>

        {loading ? (
          <div className="spinner-container">
            <div className="spinner"></div>
            <p>Loading shortlist...</p>
          </div>
        ) : shortlist.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px 20px', color: '#64748b' }}>
            <p style={{ fontSize: '0.95rem' }}>Your scouting shortlist is currently empty.</p>
            <p style={{ fontSize: '0.82rem', color: '#94a3b8', marginTop: '4px' }}>
              Browse Player Management or Talent Scouting to add priority prospects to your shortlist.
            </p>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Player</th>
                  <th>Country</th>
                  <th>Role</th>
                  <th>Target Role</th>
                  <th>Priority</th>
                  <th>Runs</th>
                  <th>Wickets</th>
                  <th>Scout Notes</th>
                  <th>Added On</th>
                  <th style={{ textAlign: 'center' }}>Remove</th>
                </tr>
              </thead>
              <tbody>
                {shortlist.map((item) => (
                  <tr key={item.id}>
                    <td style={{ fontWeight: '700', color: '#0d6e38' }}>{item.name}</td>
                    <td>{item.country}</td>
                    <td>
                      <span className={`badge badge-${item.role?.toLowerCase()?.replace('-', '')}`}>
                        {item.role}
                      </span>
                    </td>
                    <td style={{ fontWeight: '600' }}>{item.target_role}</td>
                    <td>
                      <span className="badge badge-tier1">{item.priority_tier}</span>
                    </td>
                    <td>{item.runs?.toLocaleString()}</td>
                    <td>{item.wickets}</td>
                    <td style={{ fontSize: '0.82rem', color: '#475569', maxWidth: '240px' }}>
                      {item.scout_notes || 'No notes added'}
                    </td>
                    <td style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                      {item.created_at?.slice(0, 10)}
                    </td>
                    <td style={{ textAlign: 'center' }}>
                      <button
                        className="btn btn-secondary btn-sm"
                        style={{ color: '#ef4444' }}
                        onClick={() => handleRemove(item.id)}
                      >
                        <Trash2 size={14} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
