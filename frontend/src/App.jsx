import React, { useState } from 'react';
import Navbar from './components/Navbar';
import DashboardPage from './pages/DashboardPage';
import DistrictAnalysisPage from './pages/DistrictAnalysisPage';
import SkillGapPage from './pages/SkillGapPage';
import CourseAlignmentPage from './pages/CourseAlignmentPage';
import TrainingPlanPage from './pages/TrainingPlanPage';

export function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [drilldownDistrict, setDrilldownDistrict] = useState('Pune');

  const handleDistrictSelectFromDash = (districtName) => {
    setDrilldownDistrict(districtName);
    setActiveTab('district-analysis');
  };

  return (
    <div className="app-container">
      <Navbar activeTab={activeTab} onSelectTab={setActiveTab} />

      <main className="main-content">
        {activeTab === 'dashboard' && (
          <DashboardPage onSelectDistrict={handleDistrictSelectFromDash} />
        )}
        {activeTab === 'district-analysis' && (
          <DistrictAnalysisPage initialDistrict={drilldownDistrict} />
        )}
        {activeTab === 'skill-gap' && (
          <SkillGapPage />
        )}
        {activeTab === 'course-alignment' && (
          <CourseAlignmentPage />
        )}
        {activeTab === 'training-plan' && (
          <TrainingPlanPage initialDistrict={drilldownDistrict} />
        )}
      </main>

      <footer style={{
        background: '#0b1e33',
        color: '#94a3b8',
        padding: '24px',
        fontSize: '0.82rem',
        borderTop: '1px solid rgba(255,255,255,0.1)',
        marginTop: 'auto'
      }}>
        <div style={{
          maxWidth: '1400px',
          margin: '0 auto',
          display: 'flex',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '12px'
        }}>
          <div>
            <strong>Government of Maharashtra</strong> &bull; Skill Development, Employment and Entrepreneurship Department
          </div>
          <div>
            Smart India Hackathon 2026 Prototype &bull; Problem Statement #26134
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;

