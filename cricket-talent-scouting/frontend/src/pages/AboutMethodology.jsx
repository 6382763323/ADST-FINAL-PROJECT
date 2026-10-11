import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { BookOpen, Award, Brain, Database, CheckCircle, HelpCircle } from 'lucide-react';

export default function AboutMethodology() {
  const [modelInfo, setModelInfo] = useState(null);

  useEffect(() => {
    loadModelMetadata();
  }, []);

  async function loadModelMetadata() {
    try {
      const res = await api.getModelInfo();
      if (res.status === 'success') {
        setModelInfo(res.metadata);
      }
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: '700' }}>Project Methodology & Capstone Report Guide</h3>
        <p style={{ color: '#64748b', fontSize: '0.86rem' }}>
          Comprehensive documentation of mathematical formulation, data engineering pipelines, machine learning architecture, and Viva viva-voce preparation.
        </p>
      </div>

      {/* Overview Card */}
      <div className="card">
        <h4 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <BookOpen size={20} color="#0d6e38" />
          <span>1. Project Background & Objective</span>
        </h4>
        <div style={{ fontSize: '0.9rem', color: '#334155', lineHeight: '1.7', marginTop: '10px' }}>
          <p>
            In modern cricket auctions and franchise squad development, relying purely on raw statistics (like total career runs or wickets) leads to flawed evaluations. A batter who accumulates 8,000 runs over 15 seasons in top-order positions is not necessarily more impactful in modern T20/ODI cricket than a player scoring at a 155 strike rate with a 42 average.
          </p>
          <p style={{ marginTop: '8px' }}>
            This system implements an objective, role-specific Cricket Talent Scouting and Analysis framework that balances consistency (average), scoring tempo (strike rate), defensive containment (economy), and milestone conversions into a transparent 0-100 talent score.
          </p>
        </div>
      </div>

      {/* Mathematical Formulas Card */}
      <div className="card">
        <h4 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Award size={20} color="#16a34a" />
          <span>2. Transparent Mathematical Talent Scoring Formulation</span>
        </h4>
        <div style={{ fontSize: '0.88rem', color: '#334155', lineHeight: '1.7', marginTop: '12px' }}>
          <div style={{ background: '#f8fafc', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0', marginBottom: '14px' }}>
            <h5 style={{ fontWeight: '700', color: '#0f172a' }}>A. Batter Talent Score:</h5>
            <p style={{ fontFamily: 'monospace', color: '#0d6e38', fontWeight: '600', marginTop: '4px' }}>
              Batter_Score = 0.35 * Norm(Batting_Average) + 0.30 * Norm(Strike_Rate) + 0.20 * Norm(log(Runs)) + 0.15 * Norm(Milestones)
            </p>
            <p style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '4px' }}>
              Batting average reflects consistency; Strike rate measures aggression; Log of runs rewards experience while preventing volume domination.
            </p>
          </div>

          <div style={{ background: '#f8fafc', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0', marginBottom: '14px' }}>
            <h5 style={{ fontWeight: '700', color: '#0f172a' }}>B. Bowler Talent Score:</h5>
            <p style={{ fontFamily: 'monospace', color: '#0284c7', fontWeight: '600', marginTop: '4px' }}>
              Bowler_Score = 0.30 * InvNorm(Bowling_Average) + 0.30 * InvNorm(Economy_Rate) + 0.25 * Norm(log(Wickets)) + 0.15 * InvNorm(Bowling_SR)
            </p>
            <p style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '4px' }}>
              InvNorm (Inverse Normalization) ensures that lower economy rates and lower bowling averages receive higher scouting ratings.
            </p>
          </div>

          <div style={{ background: '#f8fafc', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <h5 style={{ fontWeight: '700', color: '#0f172a' }}>C. All-Rounder & Wicketkeeper Composites:</h5>
            <p style={{ fontFamily: 'monospace', color: '#b45309', fontWeight: '600', marginTop: '4px' }}>
              AllRounder_Score = 0.50 * Batter_Score + 0.50 * Bowler_Score
            </p>
            <p style={{ fontFamily: 'monospace', color: '#7e22ce', fontWeight: '600', marginTop: '4px' }}>
              WicketKeeper_Score = 0.65 * Batter_Score + 0.35 * Norm(Dismissals_Per_Match)
            </p>
          </div>
        </div>
      </div>

      {/* Machine Learning Pipeline Card */}
      <div className="card">
        <h4 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Brain size={20} color="#0284c7" />
          <span>3. Machine Learning Architecture & Limitations</span>
        </h4>
        <div style={{ fontSize: '0.88rem', color: '#334155', lineHeight: '1.7', marginTop: '12px' }}>
          <p>
            The system employs a <strong>Random Forest Classifier</strong> within a Scikit-learn Pipeline with Standard Scaler normalization.
          </p>

          {modelInfo && (
            <div style={{ marginTop: '14px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '14px' }}>
              <div style={{ background: '#f0fdf4', padding: '14px', borderRadius: '8px', border: '1px solid #bbf7d0' }}>
                <div style={{ fontSize: '0.78rem', color: '#166534' }}>Cross-Validation Accuracy</div>
                <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#14532d' }}>
                  {(modelInfo.metrics?.cv_accuracy_mean * 100).toFixed(1)}%
                </div>
              </div>

              <div style={{ background: '#f0f9ff', padding: '14px', borderRadius: '8px', border: '1px solid #bae6fd' }}>
                <div style={{ fontSize: '0.78rem', color: '#0369a1' }}>Test Split Accuracy</div>
                <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#0c4a6e' }}>
                  {(modelInfo.metrics?.test_accuracy * 100).toFixed(1)}%
                </div>
              </div>

              <div style={{ background: '#fef3c7', padding: '14px', borderRadius: '8px', border: '1px solid #fde68a' }}>
                <div style={{ fontSize: '0.78rem', color: '#92400e' }}>Model Architecture</div>
                <div style={{ fontSize: '0.95rem', fontWeight: '700', color: '#78350f', marginTop: '4px' }}>
                  RandomForest (100 Trees)
                </div>
              </div>
            </div>
          )}

          <div style={{ marginTop: '16px', background: '#fee2e2', padding: '16px', borderRadius: '8px', border: '1px solid #fca5a5' }}>
            <h5 style={{ fontWeight: '700', color: '#991b1b', marginBottom: '6px' }}>Explicit Academic Limitations:</h5>
            <ul style={{ paddingLeft: '20px', color: '#7f1d1d', fontSize: '0.84rem' }}>
              <li>Career aggregates do not capture contextual pitch conditions (dusty vs green-top) or weather.</li>
              <li>Match-to-match form fluctuations and player fitness injuries cannot be captured by static historical statistics.</li>
              <li>The machine learning classification is an analytical decision-support tool, not an absolute guarantee of match outcomes.</li>
            </ul>
          </div>
        </div>
      </div>

      {/* MCA Viva Voce FAQ Card */}
      <div className="card">
        <h4 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <HelpCircle size={20} color="#7e22ce" />
          <span>4. MCA Capstone Viva-Voce Key Talking Points</span>
        </h4>
        <div style={{ marginTop: '14px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ borderLeft: '4px solid #16a34a', paddingLeft: '14px' }}>
            <h5 style={{ fontWeight: '700', color: '#0f172a' }}>Q: Why did you not delete extreme outliers in batting and bowling?</h5>
            <p style={{ fontSize: '0.86rem', color: '#475569', marginTop: '4px' }}>
              <strong>Answer:</strong> In cricket sports analytics, records such as Rohit Sharma's 264 runs or Muttiah Muralitharan's 1300+ international dismissals represent true world-class mastery rather than data corruption. Automatically trimming them would distort talent benchmarks.
            </p>
          </div>

          <div style={{ borderLeft: '4px solid #0284c7', paddingLeft: '14px' }}>
            <h5 style={{ fontWeight: '700', color: '#0f172a' }}>Q: How are missing values handled for pure batters and pure bowlers?</h5>
            <p style={{ fontSize: '0.86rem', color: '#475569', marginTop: '4px' }}>
              <strong>Answer:</strong> Domain sentinels (0.0 with proper documentation) are imputed because a pure batter does not bowl in professional matches, making NaN bowling averages a domain reality rather than a missing data error.
            </p>
          </div>

          <div style={{ borderLeft: '4px solid #f59e0b', paddingLeft: '14px' }}>
            <h5 style={{ fontWeight: '700', color: '#0f172a' }}>Q: What database and architectural patterns are used?</h5>
            <p style={{ fontSize: '0.86rem', color: '#475569', marginTop: '4px' }}>
              <strong>Answer:</strong> A relational SQLite database structured with 3NF tables (<code>players</code>, <code>player_performance</code>, <code>scouting_shortlist</code>, <code>analysis_history</code>) with foreign keys and cascade rules, connected to a Flask REST API and a decoupled Vite + React frontend.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
