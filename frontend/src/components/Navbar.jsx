import React from 'react';

const TABS = [
  { id: 'dashboard', label: 'Dashboard', step: '1' },
  { id: 'district-analysis', label: 'District Analysis', step: '2' },
  { id: 'skill-gap', label: 'Skill Gap Intelligence', step: '3' },
  { id: 'course-alignment', label: 'Course Alignment', step: '4' },
  { id: 'training-plan', label: 'District Training Plan', step: '5' }
];

export function Navbar({ activeTab, onSelectTab }) {
  return (
    <header>
      <div className="gov-top-banner">
        <div>Government of Maharashtra &bull; Maharashtra State Skill Development Society (MSSDS)</div>
        <div>SIH 2026 &bull; Problem Statement #26134 &bull; Prototype Edition</div>
      </div>
      <nav className="gov-navbar">
        <div className="navbar-inner">
          <div className="brand-section">
            <div className="gov-emblem">MH</div>
            <div>
              <div className="brand-title">Maharashtra Skill Intelligence Platform</div>
              <div className="brand-subtitle">Industry Demand, Skill Gap &amp; Curriculum Alignment Engine</div>
            </div>
          </div>

          <div className="nav-tabs">
            {TABS.map(tab => (
              <button
                key={tab.id}
                className={`nav-tab-btn ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => onSelectTab(tab.id)}
              >
                <span className="step-indicator">{tab.step}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>
    </header>
  );
}

export default Navbar;

