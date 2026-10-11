import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  ZAxis,
  Tooltip,
  Legend,
  CartesianGrid
} from 'recharts';
import { TrendingUp, Info } from 'lucide-react';

export default function Analytics({ onSelectPlayer }) {
  const [scatterData, setScatterData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadScatter();
  }, []);

  async function loadScatter() {
    try {
      setLoading(true);
      const res = await api.getScatterData();
      if (res.status === 'success') {
        setScatterData(res);
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
        <p>Loading Exploratory Analytics Plots...</p>
      </div>
    );
  }

  const battingPoints = scatterData?.batting_scatter || [];
  const bowlingPoints = scatterData?.bowling_scatter || [];

  const CustomBattingTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div style={{ background: 'white', padding: '10px 14px', border: '1px solid #cbd5e1', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
          <p style={{ fontWeight: '700', color: '#0f172a' }}>{data.Player}</p>
          <p style={{ fontSize: '0.8rem', color: '#64748b' }}>Role: {data.Role}</p>
          <p style={{ fontSize: '0.85rem', color: '#16a34a' }}>Batting Avg: <strong>{data.Batting_Average}</strong></p>
          <p style={{ fontSize: '0.85rem', color: '#0284c7' }}>Strike Rate: <strong>{data.Strike_Rate}</strong></p>
          <p style={{ fontSize: '0.85rem', color: '#475569' }}>Career Runs: <strong>{data.Runs?.toLocaleString()}</strong></p>
        </div>
      );
    }
    return null;
  };

  const CustomBowlingTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div style={{ background: 'white', padding: '10px 14px', border: '1px solid #cbd5e1', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
          <p style={{ fontWeight: '700', color: '#0f172a' }}>{data.Player}</p>
          <p style={{ fontSize: '0.8rem', color: '#64748b' }}>Role: {data.Role}</p>
          <p style={{ fontSize: '0.85rem', color: '#dc2626' }}>Economy: <strong>{data.Economy_Rate}</strong></p>
          <p style={{ fontSize: '0.85rem', color: '#0284c7' }}>Bowling Avg: <strong>{data.Bowling_Average}</strong></p>
          <p style={{ fontSize: '0.85rem', color: '#16a34a' }}>Wickets: <strong>{data.Wickets}</strong></p>
        </div>
      );
    }
    return null;
  };

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: '700' }}>Batting & Bowling Exploratory Data Analytics</h3>
        <p style={{ color: '#64748b', fontSize: '0.86rem' }}>
          Inspect bivariate relationships, performance clusters, and player efficiency frontiers.
        </p>
      </div>

      {/* BATTING SCATTER: AVERAGE VS STRIKE RATE */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Batting Frontier: Batting Average vs Strike Rate</h3>
            <p className="card-description">
              Top-Right Quadrant indicates modern elite batters (High Average + High Strike Rate). Bubble size represents career runs.
            </p>
          </div>
        </div>

        <div style={{ width: '100%', height: 380 }}>
          <ResponsiveContainer>
            <ScatterChart margin={{ top: 20, right: 30, bottom: 20, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis
                type="number"
                dataKey="Batting_Average"
                name="Batting Average"
                unit=""
                domain={[15, 60]}
                label={{ value: 'Batting Average (Runs per Dismissal)', position: 'insideBottom', offset: -10, fill: '#475569', fontSize: 12 }}
              />
              <YAxis
                type="number"
                dataKey="Strike_Rate"
                name="Strike Rate"
                unit=""
                domain={[60, 175]}
                label={{ value: 'Strike Rate (Runs per 100 Balls)', angle: -90, position: 'insideLeft', fill: '#475569', fontSize: 12 }}
              />
              <ZAxis type="number" dataKey="Runs" range={[50, 450]} name="Runs" />
              <Tooltip content={<CustomBattingTooltip />} />
              <Scatter name="Players" data={battingPoints} fill="#16a34a" fillOpacity={0.7} />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* BOWLING SCATTER: ECONOMY VS BOWLING AVERAGE */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Bowling Efficiency Frontier: Economy Rate vs Bowling Average</h3>
            <p className="card-description">
              Bottom-Left Quadrant represents world-class bowlers (Low Economy + Low Average). Bubble size represents career wickets.
            </p>
          </div>
        </div>

        <div style={{ width: '100%', height: 380 }}>
          <ResponsiveContainer>
            <ScatterChart margin={{ top: 20, right: 30, bottom: 20, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis
                type="number"
                dataKey="Economy_Rate"
                name="Economy Rate"
                domain={[3.0, 9.0]}
                label={{ value: 'Economy Rate (Runs Conceded per Over)', position: 'insideBottom', offset: -10, fill: '#475569', fontSize: 12 }}
              />
              <YAxis
                type="number"
                dataKey="Bowling_Average"
                name="Bowling Average"
                domain={[15, 55]}
                label={{ value: 'Bowling Average (Runs Conceded per Wicket)', angle: -90, position: 'insideLeft', fill: '#475569', fontSize: 12 }}
              />
              <ZAxis type="number" dataKey="Wickets" range={[60, 500]} name="Wickets" />
              <Tooltip content={<CustomBowlingTooltip />} />
              <Scatter name="Bowlers" data={bowlingPoints} fill="#0284c7" fillOpacity={0.7} />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
