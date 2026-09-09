import React, { useState } from 'react';
import PriorityBadge from './PriorityBadge';

export function SkillGapTable({ records = [] }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('ALL');

  const filteredRecords = records.filter(r => {
    const matchesSearch = r.skill.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          r.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          r.district.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesPriority = priorityFilter === 'ALL' || r.priority === priorityFilter;
    return matchesSearch && matchesPriority;
  });

  return (
    <div>
      <div style={{ display: 'flex', gap: '12px', marginBottom: '16px', flexWrap: 'wrap' }}>
        <input
          type="text"
          placeholder="Filter by skill, category, or district..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            flex: '1',
            minWidth: '240px',
            padding: '8px 14px',
            borderRadius: '6px',
            border: '1px solid #cbd5e1',
            fontSize: '0.88rem'
          }}
        />
        <select
          value={priorityFilter}
          onChange={(e) => setPriorityFilter(e.target.value)}
          style={{
            padding: '8px 14px',
            borderRadius: '6px',
            border: '1px solid #cbd5e1',
            fontSize: '0.88rem',
            background: '#ffffff',
            cursor: 'pointer'
          }}
        >
          <option value="ALL">All Priorities</option>
          <option value="CRITICAL">Critical (Gap &ge; 50)</option>
          <option value="HIGH">High (Gap 30-49)</option>
          <option value="MEDIUM">Medium (Gap 15-29)</option>
          <option value="LOW">Low (Gap &lt; 15)</option>
        </select>
      </div>

      <div className="data-table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>District</th>
              <th>Skill</th>
              <th>Category</th>
              <th style={{ textAlign: 'right' }}>Industry Demand</th>
              <th style={{ textAlign: 'right' }}>Training Coverage</th>
              <th style={{ textAlign: 'right' }}>Skill Gap</th>
              <th style={{ textAlign: 'center' }}>Priority</th>
            </tr>
          </thead>
          <tbody>
            {filteredRecords.length === 0 ? (
              <tr>
                <td colSpan="7" style={{ textAlign: 'center', padding: '32px', color: '#64748b' }}>
                  No matching skill gap records found.
                </td>
              </tr>
            ) : (
              filteredRecords.map((r, i) => (
                <tr key={`${r.district}-${r.skill}-${i}`}>
                  <td style={{ fontWeight: '600' }}>{r.district}</td>
                  <td style={{ fontWeight: '600', color: '#0f2b48' }}>{r.skill}</td>
                  <td style={{ color: '#475569' }}>{r.category}</td>
                  <td style={{ textAlign: 'right', fontWeight: '600' }}>{r.industry_demand}</td>
                  <td style={{ textAlign: 'right', color: '#2563eb' }}>{r.training_coverage}</td>
                  <td style={{ textAlign: 'right', fontWeight: '700', color: r.skill_gap >= 50 ? '#dc2626' : '#0f172a' }}>
                    {r.skill_gap}
                  </td>
                  <td style={{ textAlign: 'center' }}>
                    <PriorityBadge priority={r.priority} />
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      <div style={{ marginTop: '12px', fontSize: '0.8rem', color: '#64748b', textAlign: 'right' }}>
        Showing {filteredRecords.length} of {records.length} total skill gap calculations
      </div>
    </div>
  );
}

export default SkillGapTable;

