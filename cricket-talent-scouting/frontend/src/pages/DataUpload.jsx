import React, { useState } from 'react';
import { api } from '../services/api';
import { UploadCloud, CheckCircle, AlertTriangle, FileText, Download } from 'lucide-react';

export default function DataUpload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  function handleFileChange(e) {
    const selected = e.target.files[0];
    if (selected) {
      if (!selected.name.endsWith('.csv')) {
        setError('Only CSV files are permitted.');
        setFile(null);
        return;
      }
      setError(null);
      setFile(selected);
    }
  }

  async function handleUpload(e) {
    e.preventDefault();
    if (!file) {
      setError('Please choose a valid CSV file before uploading.');
      return;
    }

    try {
      setUploading(true);
      setError(null);
      setResult(null);

      const res = await api.uploadCSV(file);
      if (res.status === 'success') {
        setResult(res.message);
      }
    } catch (err) {
      setError(err.message || 'File upload and cleaning failed.');
    } finally {
      setUploading(false);
    }
  }

  function downloadSampleTemplate() {
    const headers = [
      "Player_ID", "Player", "Country", "Role", "Batting_Style", "Bowling_Style",
      "Age", "Matches", "Innings", "Runs", "Highest_Score", "Batting_Average",
      "Strike_Rate", "Centuries", "Fifties", "Wickets", "Bowling_Average",
      "Economy_Rate", "Bowling_Strike_Rate", "Best_Bowling", "Catches", "Stumpings"
    ];
    const sampleRow = [
      "CRIC_SAMPLE_01", "Sample Player", "India", "Batter", "Right-hand bat", "Right-arm medium",
      "25", "50", "48", "2100", "125*", "45.65", "92.4", "5", "14", "2", "45.0", "6.2", "42.0", "1/15", "25", "0"
    ];

    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(','), sampleRow.join(',')].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "cricket_players_template.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: '700' }}>Dataset Upload & Automated Cleaning Pipeline</h3>
        <p style={{ color: '#64748b', fontSize: '0.86rem' }}>
          Upload new cricket statistics CSV files. The automated Python cleaning engine validates fields, handles missing data, normalizes roles, and re-indexes SQLite.
        </p>
      </div>

      {result && <div className="alert alert-success"><CheckCircle size={18} /><span>{result}</span></div>}
      {error && <div className="alert alert-error"><AlertTriangle size={18} /><span>{error}</span></div>}

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '24px' }}>
        {/* Upload Form Card */}
        <div className="card">
          <h4 className="card-title" style={{ marginBottom: '16px' }}>Upload New CSV File</h4>

          <form onSubmit={handleUpload}>
            <div
              style={{
                border: '2px dashed #cbd5e1',
                borderRadius: '12px',
                padding: '40px 20px',
                textAlign: 'center',
                background: '#fafafa',
                cursor: 'pointer',
                marginBottom: '20px'
              }}
              onClick={() => document.getElementById('csv-file-input').click()}
            >
              <UploadCloud size={44} color="#16a34a" style={{ margin: '0 auto 12px' }} />
              <p style={{ fontWeight: '600', color: '#0f172a' }}>
                {file ? file.name : 'Click to select CSV file from your computer'}
              </p>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '4px' }}>
                Supports standard UTF-8 encoded cricket CSV datasets
              </p>
              <input
                id="csv-file-input"
                type="file"
                accept=".csv"
                style={{ display: 'none' }}
                onChange={handleFileChange}
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <button
                type="button"
                className="btn btn-secondary btn-sm"
                onClick={downloadSampleTemplate}
              >
                <Download size={14} />
                <span>Download Sample CSV Template</span>
              </button>

              <button
                type="submit"
                className="btn btn-primary"
                disabled={!file || uploading}
              >
                {uploading ? 'Processing & Cleaning...' : 'Upload & Clean Data'}
              </button>
            </div>
          </form>
        </div>

        {/* Pipeline Specifications Card */}
        <div className="card" style={{ background: '#f8fafc' }}>
          <h4 className="card-title" style={{ marginBottom: '14px' }}>Automated Cleaning Rules Applied:</h4>
          <ul style={{ paddingLeft: '20px', fontSize: '0.87rem', color: '#475569', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <li>
              <strong>Duplicate Identification:</strong> Exact and Player_ID duplicates are automatically purged.
            </li>
            <li>
              <strong>Role Normalization:</strong> Variants like "BATTER", "all rounder", or "WK" normalize into standard categories.
            </li>
            <li>
              <strong>Score Parsing:</strong> Unbeaten asterisks like <code>183*</code> are parsed into integer 183 while preserving not-out flags.
            </li>
            <li>
              <strong>Domain Sentinels:</strong> Pure batters with 0 bowling overs receive neutral indicators rather than corrupted statistics.
            </li>
            <li>
              <strong>Outlier Preservation:</strong> Exceptional scores (e.g. 264 runs or 800+ wickets) are retained as elite sports achievements.
            </li>
            <li>
              <strong>Database Reseeding:</strong> SQLite tables are automatically synchronized with the validated dataset.
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
