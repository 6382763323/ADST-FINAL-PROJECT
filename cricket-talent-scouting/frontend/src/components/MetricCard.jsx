import React from 'react';

export default function MetricCard({ title, value, subtext, icon: Icon, color = '#16a34a', bg = '#dcfce7' }) {
  return (
    <div className="metric-card">
      <div className="metric-header">
        <span className="metric-title">{title}</span>
        {Icon && (
          <div className="metric-icon-box" style={{ background: bg, color }}>
            <Icon size={20} />
          </div>
        )}
      </div>
      <div>
        <div className="metric-value">{value}</div>
        {subtext && <div className="metric-subtext">{subtext}</div>}
      </div>
    </div>
  );
}
