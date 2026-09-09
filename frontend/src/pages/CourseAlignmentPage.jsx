import React, { useState, useEffect } from 'react';
import Panel from '../components/Panel';
import apiService from '../services/apiService';

export function CourseAlignmentPage() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [districtFilter, setDistrictFilter] = useState('ALL');

  useEffect(() => {
    let isMounted = true;
    apiService.getCourse()
      .then(res => {
        if (isMounted) {
          setCourses(res);
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

  const filteredCourses = courses.filter(c => 
    districtFilter === 'ALL' || c.district.toLowerCase() === districtFilter.toLowerCase()
  );

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Course Alignment &amp; Effectiveness</h1>
          <p className="page-description">
            Audit of state vocational curricula against local industry skill needs, completion ratios, and employment placement outcomes.
          </p>
        </div>
      </div>

      <div style={{ marginBottom: '16px', display: 'flex', gap: '8px', alignItems: 'center' }}>
        <span style={{ fontSize: '0.85rem', fontWeight: '600', color: '#475569' }}>Filter District:</span>
        <select
          value={districtFilter}
          onChange={(e) => setDistrictFilter(e.target.value)}
          style={{
            padding: '6px 12px',
            borderRadius: '6px',
            border: '1px solid #cbd5e1',
            fontSize: '0.85rem',
            background: '#ffffff'
          }}
        >
          <option value="ALL">All Districts</option>
          <option value="Pune">Pune</option>
          <option value="Mumbai">Mumbai</option>
          <option value="Nagpur">Nagpur</option>
          <option value="Nashik">Nashik</option>
          <option value="Chhatrapati Sambhajinagar">Chhatrapati Sambhajinagar</option>
        </select>
      </div>

      {loading ? (
        <div className="state-container">
          <div className="spinner" />
          <div>Evaluating course alignments and throughput metrics...</div>
        </div>
      ) : error ? (
        <div className="state-container" style={{ borderColor: '#fca5a5' }}>
          <div style={{ color: '#dc2626', fontWeight: '700' }}>Failed to load course alignments</div>
          <div style={{ color: '#64748b' }}>{error}</div>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '16px' }}>
          {filteredCourses.map(c => {
            const isHighEff = c.effectiveness_score >= 0.65;
            return (
              <div
                key={c.course_id}
                style={{
                  background: '#ffffff',
                  border: '1px solid #e2e8f0',
                  borderRadius: '10px',
                  padding: '20px',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <span style={{
                        background: '#e0e7ff',
                        color: '#3730a3',
                        fontWeight: '700',
                        fontSize: '0.75rem',
                        padding: '2px 8px',
                        borderRadius: '4px'
                      }}>
                        {c.course_id}
                      </span>
                      <h3 style={{ fontSize: '1.15rem', fontWeight: '700', color: '#0f2b48' }}>
                        {c.course_name}
                      </h3>
                    </div>
                    <div style={{ color: '#64748b', fontSize: '0.82rem', marginTop: '4px' }}>
                      Training Location: <strong>{c.district}</strong>
                    </div>
                  </div>

                  <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '0.75rem', color: '#64748b', textTransform: 'uppercase' }}>Alignment Score</div>
                      <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#1d4ed8' }}>
                        {c.alignment_score}%
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '0.75rem', color: '#64748b', textTransform: 'uppercase' }}>Effectiveness</div>
                      <div style={{
                        fontSize: '1.25rem',
                        fontWeight: '800',
                        color: isHighEff ? '#16a34a' : '#d97706'
                      }}>
                        {Math.round(c.effectiveness_score * 100)}%
                      </div>
                    </div>
                  </div>
                </div>

                {/* Metrics Bar */}
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
                  gap: '12px',
                  margin: '16px 0',
                  padding: '12px 16px',
                  background: '#f8fafc',
                  borderRadius: '6px'
                }}>
                  <div>
                    <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Capacity:</span>{' '}
                    <strong>{c.capacity} seats</strong>
                  </div>
                  <div>
                    <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Completion Rate:</span>{' '}
                    <strong>{Math.round(c.completion_rate * 100)}%</strong> ({c.completed_trainees})
                  </div>
                  <div>
                    <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Placement Rate:</span>{' '}
                    <strong style={{ color: '#16a34a' }}>{Math.round(c.placement_rate * 100)}%</strong> ({c.placed_trainees})
                  </div>
                </div>

                {/* Skills Taught */}
                <div style={{ marginBottom: '12px' }}>
                  <div style={{ fontSize: '0.8rem', fontWeight: '600', color: '#334155', marginBottom: '6px' }}>
                    Skills Taught in Curriculum:
                  </div>
                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    {c.skills_taught.map((s, idx) => (
                      <span
                        key={idx}
                        style={{
                          background: '#eff6ff',
                          color: '#1e40af',
                          fontSize: '0.75rem',
                          fontWeight: '600',
                          padding: '3px 10px',
                          borderRadius: '4px',
                          border: '1px solid #bfdbfe'
                        }}
                      >
                        {s.skill} &bull; <small style={{ color: '#3b82f6' }}>{s.proficiency_taught}</small> (Demand: {s.district_demand})
                      </span>
                    ))}
                  </div>
                </div>

                {/* Actionable Recommendations */}
                {c.action_recommendations && c.action_recommendations.length > 0 && (
                  <div style={{
                    marginTop: '12px',
                    padding: '10px 14px',
                    background: '#fffbeb',
                    borderLeft: '4px solid #f59e0b',
                    borderRadius: '0 6px 6px 0',
                    fontSize: '0.84rem',
                    color: '#92400e'
                  }}>
                    <strong>Curriculum Intervention:</strong>{' '}
                    {c.action_recommendations.join(' ')}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default CourseAlignmentPage;

