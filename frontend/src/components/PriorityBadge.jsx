import React from 'react';

export function PriorityBadge({ priority = 'LOW' }) {
  const normalized = (priority || 'LOW').toUpperCase();
  let className = 'badge-low';

  if (normalized === 'CRITICAL') className = 'badge-critical';
  else if (normalized === 'HIGH') className = 'badge-high';
  else if (normalized === 'MEDIUM') className = 'badge-medium';

  return (
    <span className={`badge ${className}`}>
      <span style={{ fontSize: '0.65rem' }}>&#9679;</span>
      {normalized}
    </span>
  );
}

export default PriorityBadge;

