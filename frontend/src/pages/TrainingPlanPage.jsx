import React, { useState, useEffect } from 'react';
import DistrictSelector from '../components/DistrictSelector';
import Panel from '../components/Panel';
import RecommendationCard from '../components/RecommendationCard';
import PriorityBadge from '../components/PriorityBadge';
import apiService from '../services/apiService';

export function TrainingPlanPage({ initialDistrict = 'Pune' }) {
  const [selectedDistrict, setSelectedDistrict] = useState(initialDistrict);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    apiService.getTrainingPlan(selectedDistrict)
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
          <h1 className="page-title">District Training Action Plan</h1>
          <p className="page-description">
            Actionable policy and capacity intervention roadmap to bridge critical skill gaps across Maharashtra districts.
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
          <div>Synthesizing district training roadmap...</div>
        </div>
      ) : error ? (
        <div className="state-container" style={{ borderColor: '#fca5a5' }}>
          <div style={{ color: '#dc2626', fontWeight: '700' }}>Failed to load training plan</div>
          <div style={{ color: '#64748b' }}>{error}</div>
        </div>
      ) : (
        <div>
          {/* Target Seats Banner */}
          <div style={{
            background: 'linear-gradient(135deg, #0f2b48 0%, #1e40af 100%)',
            color: '#ffffff',
            borderRadius: '10px',
            padding: '24px',
            marginBottom: '24px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '16px'
          }}>
            <div>
              <div style={{ fontSize: '0.8rem', color: '#93c5fd', textTransform: 'uppercase', fontWeight: '700' }}>
                Strategic Target Intervention &bull; {selectedDistrict}
              </div>
              <h2 style={{ fontSize: '1.6rem', fontWeight: '800', marginTop: '4px' }}>
                +{data.plan.action_plan.targeted_additional_seats} Additional Training Seats Needed
              </h2>
              <div style={{ color: '#e2e8f0', fontSize: '0.88rem', marginTop: '4px' }}>
                Statewide target: +{data.state_summary.total_state_additional_seats_needed} seats across 5 districts
              </div>
            </div>

            <div style={{
              background: 'rgba(255,255,255,0.12)',
              border: '1px solid rgba(255,255,255,0.25)',
              padding: '12px 20px',
              borderRadius: '8px',
              textAlign: 'right'
            }}>
              <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>Current District Capacity</div>
              <div style={{ fontSize: '1.4rem', fontWeight: '800' }}>
                {data.plan.current_status.total_current_capacity} Seats
              </div>
              <div style={{ fontSize: '0.75rem', color: '#93c5fd' }}>
                {data.plan.current_status.annual_placements} Annual Placements
              </div>
            </div>
          </div>

          <div className="grid-2-col">
            {/* Critical Skills Targeted */}
            <Panel
              title={`Top Critical Gaps to Neutralize (${selectedDistrict})`}
              subtitle="Prioritized skills requiring immediate seat additions or curriculum injection"
            >
              <div className="data-table-wrapper">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Skill</th>
                      <th>Category</th>
                      <th style={{ textAlign: 'right' }}>Demand</th>
                      <th style={{ textAlign: 'right' }}>Coverage</th>
                      <th style={{ textAlign: 'right' }}>Net Deficit</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.plan.top_priority_gaps.map((g, i) => (
                      <tr key={i}>
                        <td style={{ fontWeight: '600', color: '#0f2b48' }}>{g.skill}</td>
                        <td style={{ color: '#475569', fontSize: '0.8rem' }}>{g.category}</td>
                        <td style={{ textAlign: 'right' }}>{g.demand}</td>
                        <td style={{ textAlign: 'right', color: '#2563eb' }}>{g.coverage}</td>
                        <td style={{ textAlign: 'right', fontWeight: '700', color: '#dc2626' }}>
                          +{g.gap}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Panel>

            {/* Proposed New Courses */}
            <Panel
              title="Proposed New Specialized Programs"
              subtitle="Zero-coverage critical domains requiring new course launches"
            >
              {data.plan.action_plan.new_courses_to_introduce.length === 0 ? (
                <div style={{ padding: '16px', color: '#64748b' }}>
                  No new courses required; existing capacity expansion is sufficient.
                </div>
              ) : (
                data.plan.action_plan.new_courses_to_introduce.map((nc, i) => (
                  <RecommendationCard
                    key={i}
                    type="new-course"
                    title={nc.proposed_course}
                    subtitle={`Target Roles: ${nc.target_roles.join(', ')}`}
                    seats={nc.proposed_capacity}
                    skills={nc.target_skills}
                    justification={nc.justification}
                  />
                ))
              )}
            </Panel>
          </div>

          {/* Course Expansions & Modernizations */}
          <div className="grid-2-col" style={{ marginTop: '24px' }}>
            <Panel
              title="Existing Course Capacity Expansions"
              subtitle="Scaling high-performing courses that teach high-gap skills"
            >
              {data.plan.action_plan.course_expansions.length === 0 ? (
                <div style={{ padding: '16px', color: '#64748b' }}>
                  No expansions planned for current courses in this district.
                </div>
              ) : (
                data.plan.action_plan.course_expansions.map((exp, i) => (
                  <RecommendationCard
                    key={i}
                    type="expansion"
                    title={exp.course_name}
                    subtitle={`Current Capacity: ${exp.current_capacity} seats (Effectiveness: ${Math.round(exp.effectiveness_score * 100)}%)`}
                    seats={exp.proposed_capacity_increase}
                    skills={exp.target_skills_supported}
                    justification={`Expand intake by +${exp.proposed_capacity_increase} seats to support local manufacturing/IT demand.`}
                  />
                ))
              )}
            </Panel>

            <Panel
              title="Curriculum Modernization Directives"
              subtitle="Injecting missing critical industry skills into active syllabi"
            >
              {data.plan.action_plan.curriculum_modernizations.length === 0 ? (
                <div style={{ padding: '16px', color: '#64748b' }}>
                  All existing curricula are fully aligned.
                </div>
              ) : (
                data.plan.action_plan.curriculum_modernizations.map((mod, i) => (
                  <RecommendationCard
                    key={i}
                    type="modernization"
                    title={mod.course_name}
                    subtitle={`Course ID: ${mod.course_id}`}
                    skills={mod.recommended_modules_to_add}
                    justification={mod.objective}
                  />
                ))
              )}
            </Panel>
          </div>
        </div>
      )}
    </div>
  );
}

export default TrainingPlanPage;

