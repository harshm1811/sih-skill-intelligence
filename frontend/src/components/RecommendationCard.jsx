import React from 'react';

export function RecommendationCard({
  type = 'expansion', // 'expansion' | 'modernization' | 'new-course'
  title,
  subtitle,
  seats,
  skills = [],
  justification
}) {
  let badgeText = 'Course Expansion';
  let cardClass = 'rec-card expansion';

  if (type === 'modernization') {
    badgeText = 'Curriculum Modernization';
    cardClass = 'rec-card modernization';
  } else if (type === 'new-course') {
    badgeText = 'New Course Launch';
    cardClass = 'rec-card new-course';
  }

  return (
    <div className={cardClass}>
      <div className="rec-title">
        <span>{title}</span>
        {seats ? (
          <span style={{ fontSize: '0.8rem', fontWeight: '700', color: '#16a34a' }}>
            +{seats} Seats
          </span>
        ) : null}
      </div>
      {subtitle && <div style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '2px' }}>{subtitle}</div>}
      
      {skills.length > 0 && (
        <div style={{ marginTop: '8px', display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
          {skills.map((s, idx) => (
            <span
              key={idx}
              style={{
                fontSize: '0.72rem',
                background: '#f1f5f9',
                padding: '2px 8px',
                borderRadius: '4px',
                color: '#334155',
                fontWeight: '500'
              }}
            >
              {s}
            </span>
          ))}
        </div>
      )}

      {justification && (
        <div className="rec-body">
          <strong>Action Plan:</strong> {justification}
        </div>
      )}
    </div>
  );
}

export default RecommendationCard;

