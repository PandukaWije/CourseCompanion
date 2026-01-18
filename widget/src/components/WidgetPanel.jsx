import React from 'react';
import { X } from 'lucide-react';
import { useWidgetStore } from '../store/widgetStore';

/**
 * WidgetPanel Component
 * The full panel that displays different views (Discovery, Search, Chat)
 */
export const WidgetPanel = ({ children }) => {
  const { isPanelOpen, currentView, closePanel } = useWidgetStore();

  if (!isPanelOpen || !currentView) return null;

  const getTitleForView = (view) => {
    switch (view) {
      case 'discovery':
        return 'Course Discovery';
      case 'search':
        return 'Search Courses';
      case 'chat':
        return 'Course Companion';
      default:
        return 'Course Companion';
    }
  };

  return (
    <div 
      className="cc-panel"
      style={{ pointerEvents: 'auto' }} // Enable clicks
    >
      {/* Header */}
      {/* <div className="cc-panel-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <img 
            src="/svg/Logo Icon.svg" 
            alt="CourseCompanion" 
            style={{ width: '32px', height: '32px' }}
          />
          <h3>{getTitleForView(currentView)}</h3>
        </div>
        <button
          className="cc-panel-close"
          onClick={closePanel}
          aria-label="Close panel"
        >
          <X size={24} />
        </button>
      </div> */}

      {/* Content */}
      <div className="cc-panel-content">
        {children}
      </div>
    </div>
  );
};

export default WidgetPanel;