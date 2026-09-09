import React from 'react';

export function DemandBar({ skill, category, demand, coverage, gap, priority }) {
  const coveragePct = demand > 0 ? Math.min(100, Math.round((coverage / demand) * 100)) : 100;
  
  // Choose color based on priority
  let barColor = '#16a34a'; // green
  if (priority === 'CRITICAL') barColor = '#dc2626'; // red
  else if (priority === 'HIGH') barColor = '#ea580c'; // orange
  else if (priority === 'MEDIUM') barColor = '#d97706'; // amber

  return (
    <div className="demand-bar-container">
      <div className="demand-bar-header">
        <div>
          <span style={{ fontWeight: '600', color: '#0f2b48' }}>{skill}</span>
          {category && <span style={{ fontSize: '0.75rem', color: '#64748b', marginLeft: '8px' }}>({category})</span>}
        </div>
        <div className="demand-bar-labels">
          <span style={{ color: '#1e293b' }}>Demand: <strong>{demand}</strong></span>
          <span style={{ color: '#2563eb' }}>Supply: <strong>{coverage}</strong></span>
          <span style={{ color: barColor }}>Gap: <strong>{gap}</strong></span>
        </div>
      </div>
      <div className="demand-progress-track">
        <div
          className="demand-progress-fill"
          style={{
            width: `${coveragePct}%`,
            backgroundColor: barColor
          }}
          title={`Coverage: ${coveragePct}% (${coverage}/${demand})`}
        />
      </div>
    </div>
  );
}

export default DemandBar;

