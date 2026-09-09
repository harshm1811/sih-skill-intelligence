import React, { useState, useEffect } from 'react';
import DistrictSelector from '../components/DistrictSelector';
import StatCard from '../components/StatCard';
import Panel from '../components/Panel';
import DemandBar from '../components/DemandBar';
import PriorityBadge from '../components/PriorityBadge';
import apiService from '../services/apiService';

export function DistrictAnalysisPage({ initialDistrict = 'Pune' }) {
  const [selectedDistrict, setSelectedDistrict] = useState(initialDistrict);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    apiService.getDistrictAnalysis(selectedDistrict)
      .then(res => {
        if (isMounted) {
          setAnalysis(res);
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
          <h1 className="page-title">District Analysis</h1>
          <p className="page-description">
            Localized industrial clusters, employer hiring trends, and skill shortages across Maharashtra.
          </p>
        </div>
      </div>

      <DistrictSelector
        selectedDistrict={selectedDistrict}
        onSelectDistrict={setSelectedDistrict}
      />

      {loading ? (
        <div className="state-container">
          <div className="spinner" />
          <div>Loading district data for {selectedDistrict}...</div>
        </div>
      ) : error ? (
        <div className="state-container" style={{ borderColor: '#fca5a5' }}>
          <div style={{ color: '#dc2626', fontWeight: '700' }}>Failed to load district data</div>
          <div style={{ color: '#64748b' }}>{error}</div>
        </div>
      ) : (
        <div>
          {/* District Profile Banner */}
          <div style={{
            background: 'linear-gradient(135deg, #1e3a8a 0%, #0f2b48 100%)',
            color: '#ffffff',
            padding: '20px 24px',
            borderRadius: '10px',
            marginBottom: '24px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px' }}>
              <div>
                <h2 style={{ fontSize: '1.4rem', fontWeight: '700' }}>{analysis.district_name} District</h2>
                <div style={{ color: '#93c5fd', fontSize: '0.85rem' }}>Region: {analysis.region}</div>
              </div>
              <div style={{
                background: 'rgba(255,255,255,0.15)',
                padding: '6px 14px',
                borderRadius: '6px',
                fontSize: '0.8rem',
                fontWeight: '600'
              }}>
                District ID: {analysis.district_id}
              </div>
            </div>
            <div style={{ marginTop: '12px', fontSize: '0.9rem', color: '#e2e8f0' }}>
              <strong>Key Industrial Focus:</strong> {analysis.industrial_focus}
            </div>
          </div>

          {/* Quick Metrics */}
          <div className="stat-cards-grid">
            <StatCard
              label="Local Job Demand"
              value={analysis.total_job_demand}
              subtext="Active job postings"
            />
            <StatCard
              label="Average CTC"
              value={`₹${(analysis.average_salary / 100000).toFixed(1)}L`}
              subtext="Annual package"
              variant="success"
            />
            <StatCard
              label="Critical Gaps"
              value={analysis.skills_analysis.critical_gaps.length}
              subtext="Skills with deficit >= 50"
              variant="critical"
            />
            <StatCard
              label="High Priority Gaps"
              value={analysis.skills_analysis.high_gaps.length}
              subtext="Skills with deficit 30-49"
              variant="warning"
            />
          </div>

          <div className="grid-2-col">
            {/* Top Demanded Roles */}
            <Panel
              title="Top Demanded Roles in District"
              subtitle="Hiring volume in local manufacturing plants & tech corridors"
            >
              <div className="data-table-wrapper">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Job Role</th>
                      <th style={{ textAlign: 'right' }}>Demand</th>
                      <th style={{ textAlign: 'right' }}>Avg Salary</th>
                    </tr>
                  </thead>
                  <tbody>
                    {analysis.top_roles.map((r, i) => (
                      <tr key={i}>
                        <td style={{ fontWeight: '600', color: '#0f2b48' }}>{r.role}</td>
                        <td style={{ textAlign: 'right', fontWeight: '600' }}>{r.demand}</td>
                        <td style={{ textAlign: 'right', color: '#16a34a', fontWeight: '600' }}>
                          &#8377;{(r.average_salary / 100000).toFixed(1)}L
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Panel>

            {/* Top Hiring Companies */}
            <Panel
              title="Top Hiring Employers"
              subtitle="Major industrial enterprises driving recruitment"
            >
              <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '10px' }}>
                {Object.entries(analysis.top_hiring_companies).map(([comp, count], i) => (
                  <div
                    key={i}
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '10px 14px',
                      background: '#f8fafc',
                      borderRadius: '6px',
                      border: '1px solid #e2e8f0'
                    }}
                  >
                    <span style={{ fontWeight: '600', color: '#0f2b48' }}>{comp}</span>
                    <span style={{
                      background: '#e0e7ff',
                      color: '#3730a3',
                      fontSize: '0.78rem',
                      fontWeight: '700',
                      padding: '2px 8px',
                      borderRadius: '12px'
                    }}>
                      {count} Openings
                    </span>
                  </div>
                ))}
              </div>
            </Panel>
          </div>

          {/* District Critical Gaps */}
          <Panel
            title={`Critical Skill Gaps in ${selectedDistrict}`}
            subtitle="Skills where local industry demand exceeds existing training capacity"
            badge={<PriorityBadge priority="CRITICAL" />}
          >
            {analysis.skills_analysis.critical_gaps.length === 0 ? (
              <div style={{ color: '#16a34a', padding: '12px 0' }}>
                No critical gaps identified for this district.
              </div>
            ) : (
              analysis.skills_analysis.critical_gaps.slice(0, 8).map((g, i) => (
                <DemandBar
                  key={i}
                  skill={g.skill}
                  category={g.category}
                  demand={g.industry_demand}
                  coverage={g.training_coverage}
                  gap={g.skill_gap}
                  priority={g.priority}
                />
              ))
            )}
          </Panel>
        </div>
      )}
    </div>
  );
}

export default DistrictAnalysisPage;

