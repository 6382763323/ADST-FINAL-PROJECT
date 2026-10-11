import React from 'react';
import {
  LayoutDashboard,
  Users,
  LineChart,
  Award,
  GitCompare,
  UserCheck,
  TrendingUp,
  UploadCloud,
  FileSpreadsheet,
  BookOpen
} from 'lucide-react';

export default function Sidebar({ activeTab, onSelectTab }) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'players', label: 'Player Management', icon: Users },
    { id: 'performance', label: 'Performance Analysis', icon: LineChart },
    { id: 'scouting', label: 'Talent Scouting', icon: Award },
    { id: 'compare', label: 'Player Comparison', icon: GitCompare },
    { id: 'profile', label: 'Player Profile', icon: UserCheck },
    { id: 'analytics', label: 'Batting & Bowling EDA', icon: TrendingUp },
    { id: 'upload', label: 'Dataset Upload', icon: UploadCloud },
    { id: 'reports', label: 'Reports & Export', icon: FileSpreadsheet },
    { id: 'about', label: 'About & Methodology', icon: BookOpen },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="brand-icon">🏏</div>
        <div className="brand-info">
          <h1>CricScout AI</h1>
          <p>MCA Capstone Project</p>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              className={`nav-item ${isActive ? 'active' : ''}`}
              onClick={() => onSelectTab(item.id)}
            >
              <Icon className="icon" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <span>SQLite + Flask + React</span>
        <span>2026</span>
      </div>
    </aside>
  );
}
