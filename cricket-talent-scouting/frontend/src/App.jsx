import React, { useState } from 'react';
import MainLayout from './layouts/MainLayout';
import Dashboard from './pages/Dashboard';
import PlayerManagement from './pages/PlayerManagement';
import PerformanceAnalysis from './pages/PerformanceAnalysis';
import TalentScouting from './pages/TalentScouting';
import PlayerComparison from './pages/PlayerComparison';
import PlayerProfile from './pages/PlayerProfile';
import Analytics from './pages/Analytics';
import DataUpload from './pages/DataUpload';
import Reports from './pages/Reports';
import AboutMethodology from './pages/AboutMethodology';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedPlayerId, setSelectedPlayerId] = useState('CRIC_001');
  const [compareP1, setCompareP1] = useState('CRIC_001');
  const [compareP2, setCompareP2] = useState('CRIC_004');

  // Page titles and subtitle dictionary
  const pageMeta = {
    dashboard: { title: 'Cricket Analytics Dashboard', subtitle: 'Executive overview of squad metrics, talent distribution, and key milestones.' },
    players: { title: 'Player Management & Directory', subtitle: 'Search, filter, insert, update, and manage player records in SQLite.' },
    performance: { title: 'Player Performance Analysis', subtitle: 'Role-segregated breakdown of batting, bowling, and fielding statistics.' },
    scouting: { title: 'Cricket Talent Scouting & Ranking', subtitle: 'Configurable multi-factor talent scoring engine with format-specific presets.' },
    compare: { title: 'Player Comparison & Radar Matrix', subtitle: 'Head-to-head comparison across 5 core scouting pillars.' },
    profile: { title: 'Individual Player Profile', subtitle: 'Deep dive into career stats, milestones, and Machine Learning talent tier prediction.' },
    analytics: { title: 'Batting & Bowling Exploratory Analytics', subtitle: 'Frontier scatter plots, efficiency clusters, and quadrant analysis.' },
    upload: { title: 'Dataset Upload & Cleaning Pipeline', subtitle: 'Upload new CSV files, validate schema, and trigger automated Python cleaner.' },
    reports: { title: 'Reports & CSV Export Center', subtitle: 'Shortlist candidate management and full talent scouting CSV downloads.' },
    about: { title: 'Methodology & MCA Capstone Viva Guide', subtitle: 'System architecture, mathematical formulations, and viva-voce questions.' },
  };

  function handleSelectPlayer(playerId) {
    setSelectedPlayerId(playerId);
    setActiveTab('profile');
  }

  function handleComparePlayer(playerId) {
    setCompareP1(playerId);
    setActiveTab('compare');
  }

  const currentMeta = pageMeta[activeTab] || { title: 'Cricket Talent Scouting', subtitle: '' };

  return (
    <MainLayout
      activeTab={activeTab}
      onSelectTab={setActiveTab}
      pageTitle={currentMeta.title}
      subtitle={currentMeta.subtitle}
    >
      {activeTab === 'dashboard' && <Dashboard onNavigate={setActiveTab} />}
      {activeTab === 'players' && (
        <PlayerManagement
          onSelectPlayer={handleSelectPlayer}
          onComparePlayer={handleComparePlayer}
        />
      )}
      {activeTab === 'performance' && (
        <PerformanceAnalysis onSelectPlayer={handleSelectPlayer} />
      )}
      {activeTab === 'scouting' && (
        <TalentScouting
          onSelectPlayer={handleSelectPlayer}
          onComparePlayer={handleComparePlayer}
        />
      )}
      {activeTab === 'compare' && (
        <PlayerComparison
          initialP1={compareP1}
          initialP2={compareP2}
        />
      )}
      {activeTab === 'profile' && (
        <PlayerProfile
          playerId={selectedPlayerId}
          onComparePlayer={handleComparePlayer}
        />
      )}
      {activeTab === 'analytics' && (
        <Analytics onSelectPlayer={handleSelectPlayer} />
      )}
      {activeTab === 'upload' && <DataUpload />}
      {activeTab === 'reports' && <Reports />}
      {activeTab === 'about' && <AboutMethodology />}
    </MainLayout>
  );
}
