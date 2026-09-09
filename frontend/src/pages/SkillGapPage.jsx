import React, { useState, useEffect } from 'react';
import DistrictSelector from '../components/DistrictSelector';
import Panel from '../components/Panel';
import SkillGapTable from '../components/SkillGapTable';
import PriorityBadge from '../components/PriorityBadge';
import apiService from '../services/apiService';

export function SkillGapPage() {
  const [selectedDistrict, setSelectedDistrict] = useState('ALL');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    apiService.getSkillGap(null, selectedDistrict)
      .then(res => {
        if (isMounted) {
          setData(res);
          setLoading(false);
        }
      })
      .catch(err => {
        if (isMounted) {
          setError(err.message);
          setLoading(false);
        }
      });
    return () => { isMounted = false; };
  }, [selectedDistrict]);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Skill Gap Intelligence</h1>
          <p className="page-description">
            Quantitative delta between real-time industry skill demand and state vocational course completers.
          </p>
        </div>
      </div>

      {/* Formula & Methodology Card */}
      <div style={{
        background: '#ffffff',
        border: '1px solid #cbd5e1',
        borderRadius: '8px',
        padding: '16px 20px',
        marginBottom: '20px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '16px'
      }}>
        <div>
          <div style={{ fontSize: '0.78rem', textTransform: 'uppercase', color: '#64748b', fontWeight: '700' }}>
            Primary Mathematical Formula
          </div>
          <div style={{ fontSize: '1.2rem', fontWeight: '800', color: '#0f2b48', marginTop: '2px' }}>
            Skill Gap = Industry Demand &minus; Training Coverage
          </div>
        </div>

        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', alignItems: 'center' }}>
          <span style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: '600' }}>Thresholds:</span>
          <PriorityBadge priority="CRITICAL" /> <span style={{ fontSize: '0.75rem', color: '#64748b' }}>&ge; 50</span>
          <PriorityBadge priority="HIGH" /> <span style={{ fontSize: '0.75rem', color: '#64748b' }}>30&ndash;49</span>
          <PriorityBadge priority="MEDIUM" /> <span style={{ fontSize: '0.75rem', color: '#64748b' }}>15&ndash;29</span>
          <PriorityBadge priority="LOW" /> <span style={{ fontSize: '0.75rem', color: '#64748b' }}>&lt; 15</span>
        </div>
      </div>

      {/* District Filter */}
      <DistrictSelector
        selectedDistrict={selectedDistrict}
        onSelectDistrict={setSelectedDistrict}
        includeAll={true}
      />

      {loading ? (
        <div className="state-container">
          <div className="spinner" />
          <div>Computing skill gap intelligence matrix...</div>
        </div>
      ) : error ? (
        <div className="state-container" style={{ borderColor: '#fca5a5' }}>
          <div style={{ color: '#dc2626', fontWeight: '700' }}>Failed to load skill gap data</div>
          <div style={{ color: '#64748b' }}>{error}</div>
        </div>
      ) : (
        <Panel
          title="Granular Skill Gap Register"
          subtitle={`Showing data for: ${selectedDistrict === 'ALL' ? 'Statewide (All Districts)' : selectedDistrict}`}
        >
          <SkillGapTable records={data.records} />
        </Panel>
      )}
    </div>
  );
}

export default SkillGapPage;

