import React from 'react';

export function Panel({ title, subtitle, badge, action, children }) {
  return (
    <div className="panel">
      {(title || subtitle || badge || action) && (
        <div className="panel-header">
          <div>
            {title && <div className="panel-title">{title}</div>}
            {subtitle && <div className="panel-subtitle">{subtitle}</div>}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {badge && <span>{badge}</span>}
            {action && <span>{action}</span>}
          </div>
        </div>
      )}
      <div className="panel-body">
        {children}
      </div>
    </div>
  );
}

export default Panel;

