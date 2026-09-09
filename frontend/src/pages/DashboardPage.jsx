import React, { useState, useEffect } from 'react';
import StatCard from '../components/StatCard';
import Panel from '../components/Panel';
import DemandBar from '../components/DemandBar';
import apiService from '../services/apiService';

export function DashboardPage({ onSelectDistrict }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    apiService.getDashboard()
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
  }, []);

  if (loading) {
    return (
      <div className="state-container">
        <div className="spinner" />
        <div>Loading Maharashtra Skill Intelligence Data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="state-container" style={{ borderColor: '#fca5a5' }}>
        <div style={{ color: '#dc2626', fontWeight: '700' }}>Error Loading Dashboard</div>
        <div style={{ color: '#64748b', marginTop: '6px' }}>{error}</div>
      </div>
    );
  }

  const { kpis, top_statewide_demanded_roles, top_statewide_critical_skills, district_summaries } = data;

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Executive Dashboard</h1>
          <p className="page-description">
            Macro analysis of industry labor demand against state vocational training throughput across Maharashtra.
          </p>
        </div>
      </div>

      <div className="disclaimer-banner">
        <span>&#9432;</span>
        <span>
          <strong>Prototype Notice:</strong> This platform utilizes representative/sample data prepared for SIH 2026 Problem Statement 26134 evaluation.
        </span>
      </div>

      {/* KPI Cards Grid */}
      <div className="stat-cards-grid">
        <StatCard
          label="Total Job Demand"
          value={kpis.total_job_postings.toLocaleString()}
          subtext="Analyzed across 10 core sectors"
          variant="default"
        />
        <StatCard
          label="Training Programs"
          value={kpis.total_training_courses}
          subtext="Across 5 target districts"
          variant="default"
        />
        <StatCard
          label="Enrolled Capacity"
          value={kpis.total_enrolled_capacity.toLocaleString()}
          subtext={`${kpis.total_annual_completers} annual completers`}
          variant="default"
        />
        <StatCard
          label="Placed Trainees"
          value={kpis.total_annual_placements.toLocaleString()}
          subtext={`${Math.round(kpis.overall_placement_rate * 100)}% state placement rate`}
          variant="success"
        />
        <StatCard
          label="Critical Skill Gaps"
          value={kpis.critical_skill_gaps}
          subtext="Net deficit >= 50 candidates"
          variant="critical"
        />
      </div>

      <div className="grid-2-col">
        {/* Top Demanded Roles */}
        <Panel
          title="Top Industry Job Roles"
          subtitle="Highest employment volume across Maharashtra industrial hubs"
        >
          <div className="data-table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Job Role</th>
                  <th style={{ textAlign: 'right' }}>Total Postings</th>
                  <th style={{ textAlign: 'right' }}>Avg Salary (CTC)</th>
                </tr>
              </thead>
              <tbody>
                {top_statewide_demanded_roles.map((r, i) => (
                  <tr key={i}>
                    <td style={{ fontWeight: '600', color: '#0f2b48' }}>{r.role}</td>
                    <td style={{ textAlign: 'right', fontWeight: '600' }}>{r.total_demand}</td>
                    <td style={{ textAlign: 'right', color: '#16a34a', fontWeight: '600' }}>
                      &#8377;{(r.average_salary / 100000).toFixed(1)} LPA
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Panel>

        {/* Top Critical Skills */}
        <Panel
          title="Top Statewide Skill Gaps"
          subtitle="Critical deficits where industry demand substantially outpaces course completers"
        >
          {top_statewide_critical_skills.slice(0, 6).map((s, i) => (
            <DemandBar
              key={i}
              skill={s.skill}
              category={s.category}
              demand={s.statewide_demand}
              coverage={s.statewide_coverage}
              gap={s.statewide_gap}
              priority={s.priority}
            />
          ))}
        </Panel>
      </div>

      {/* District Quick Cards */}
      <Panel
        title="Regional District Summaries"
        subtitle="Click any district to inspect granular employment demand and training infrastructure"
      >
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px' }}>
          {district_summaries.map((d, i) => (
            <div
              key={i}
              onClick={() => onSelectDistrict && onSelectDistrict(d.district)}
              style={{
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                padding: '16px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                backgroundColor: '#ffffff'
              }}
              onMouseEnter={(e) => e.currentTarget.style.borderColor = '#1d4ed8'}
              onMouseLeave={(e) => e.currentTarget.style.borderColor = '#e2e8f0'}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3 style={{ fontSize: '1.05rem', fontWeight: '700', color: '#0f2b48' }}>{d.district}</h3>
                <span style={{ fontSize: '0.75rem', fontWeight: '700', color: '#dc2626', background: '#fef2f2', padding: '2px 8px', borderRadius: '12px' }}>
                  {d.critical_gaps} Critical
                </span>
              </div>
              <div style={{ marginTop: '10px', fontSize: '0.84rem', color: '#475569' }}>
                <div>Industry Demand: <strong>{d.jobs_count} jobs</strong></div>
                <div>Training Courses: <strong>{d.courses_count} courses ({d.training_capacity} seats)</strong></div>
              </div>
              <div style={{ marginTop: '12px', fontSize: '0.78rem', color: '#1d4ed8', fontWeight: '600' }}>
                View District Analysis &rarr;
              </div>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}

export default DashboardPage;

