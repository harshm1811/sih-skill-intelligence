import React from 'react';

const DISTRICTS = [
  'Pune',
  'Mumbai',
  'Nagpur',
  'Nashik',
  'Chhatrapati Sambhajinagar'
];

export function DistrictSelector({ selectedDistrict, onSelectDistrict, includeAll = false }) {
  const options = includeAll ? ['ALL', ...DISTRICTS] : DISTRICTS;

  return (
    <div className="district-selector">
      {options.map(dist => (
        <button
          key={dist}
          className={`district-btn ${selectedDistrict === dist ? 'active' : ''}`}
          onClick={() => onSelectDistrict(dist)}
        >
          {dist === 'ALL' ? 'Statewide (All Districts)' : dist}
        </button>
      ))}
    </div>
  );
}

export default DistrictSelector;

