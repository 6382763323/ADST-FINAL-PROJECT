import React from 'react';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';

export default function MainLayout({ activeTab, onSelectTab, pageTitle, subtitle, children }) {
  return (
    <div className="app-container">
      <Sidebar activeTab={activeTab} onSelectTab={onSelectTab} />
      <div className="main-wrapper">
        <Navbar activePageTitle={pageTitle} subtitle={subtitle} />
        <main className="content-area">
          {children}
        </main>
      </div>
    </div>
  );
}
