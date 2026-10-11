import React from 'react';
import { Activity, ShieldCheck } from 'lucide-react';

export default function Navbar({ activePageTitle, subtitle }) {
  return (
    <header className="top-navbar">
      <div className="navbar-left">
        <div>
          <h2 className="page-title">{activePageTitle}</h2>
          {subtitle && <p className="page-subtitle">{subtitle}</p>}
        </div>
      </div>
      <div className="navbar-right">
        <div className="system-badge">
          <span className="badge-dot"></span>
          <span>Analytics Engine Active</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#475569', fontSize: '0.82rem' }}>
          <ShieldCheck size={18} color="#16a34a" />
          <span>Scout System v1.0</span>
        </div>
      </div>
    </header>
  );
}
