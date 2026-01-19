import React, { useState } from 'react';

/**
 * ArtifactsPanel Component - WITH SCROLLING
 * Displays course materials, resources, and generated artifacts
 * Supports both compact (with scrolling) and expanded (full-screen) modes
 */
export const ArtifactsPanel = ({ isExpanded = false }) => {
  const [artifacts] = useState([
    {
      id: 1,
      type: 'document',
      title: 'Course Syllabus',
      description: 'Complete course outline and schedule',
      date: '2024-01-15',
      icon: '📄',
    },
    {
      id: 2,
      type: 'video',
      title: 'Lecture Recording - Week 1',
      description: 'Introduction to Course Concepts',
      date: '2024-01-18',
      icon: '🎥',
    },
    {
      id: 3,
      type: 'presentation',
      title: 'Slides: Chapter 1',
      description: 'Overview of key concepts',
      date: '2024-01-16',
      icon: '📊',
    },
    {
      id: 4,
      type: 'code',
      title: 'Code Examples',
      description: 'Sample implementations',
      date: '2024-01-17',
      icon: '💻',
    },
    {
      id: 5,
      type: 'document',
      title: 'Assignment Guidelines',
      description: 'Project requirements and rubric',
      date: '2024-01-14',
      icon: '📄',
    },
    {
      id: 6,
      type: 'presentation',
      title: 'Slides: Chapter 2',
      description: 'Advanced topics',
      date: '2024-01-19',
      icon: '📊',
    },
  ]);

  const [activeTab, setActiveTab] = useState('all');

  const filterArtifacts = () => {
    if (activeTab === 'all') return artifacts;
    return artifacts.filter(a => a.type === activeTab);
  };

  const tabs = [
    { id: 'all', label: 'All', icon: '📁' },
    { id: 'document', label: 'Documents', icon: '📄' },
    { id: 'video', label: 'Videos', icon: '🎥' },
    { id: 'presentation', label: 'Slides', icon: '📊' },
    { id: 'code', label: 'Code', icon: '💻' },
  ];

  return (
    <div style={{ 
      height: '100%', 
      display: 'flex', 
      flexDirection: 'column',
      background: isExpanded ? '#F9FAFB' : '#FFFFFF'
    }}>
      {/* Header */}
      <div style={{ 
        padding: isExpanded ? '20px 24px' : '16px', 
        borderBottom: '1px solid #E5E7EB',
        background: '#FFFFFF'
      }}>
        <h3 style={{ 
          fontSize: isExpanded ? '20px' : '18px', 
          fontWeight: '600', 
          marginBottom: '4px',
          color: '#111827'
        }}>
          Artifacts
        </h3>
        <p style={{ 
          fontSize: '13px', 
          color: '#6B7280' 
        }}>
          Course materials and resources
        </p>
      </div>

      {/* Tabs */}
      <div style={{
        display: 'flex',
        gap: '8px',
        padding: isExpanded ? '16px 24px' : '12px 16px',
        borderBottom: '1px solid #E5E7EB',
        overflowX: 'auto',
        background: '#FFFFFF',
        flexShrink: 0,
      }}>
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              padding: '6px 12px',
              borderRadius: '8px',
              border: 'none',
              background: activeTab === tab.id 
                ? 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)' 
                : '#F3F4F6',
              color: activeTab === tab.id ? '#FFFFFF' : '#4B5563',
              fontSize: '13px',
              fontWeight: '500',
              cursor: 'pointer',
              transition: 'all 0.2s',
              whiteSpace: 'nowrap',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
            }}
          >
            <span>{tab.icon}</span>
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Artifacts List - WITH SCROLLING */}
      <div style={{ 
        flex: 1, 
        overflowY: 'auto',  // ← SCROLLING ENABLED
        overflowX: 'hidden',
        padding: isExpanded ? '24px' : '16px',
        background: isExpanded ? '#F9FAFB' : '#FFFFFF',
      }}>
        {filterArtifacts().length === 0 ? (
          <div style={{
            textAlign: 'center',
            padding: '32px 16px',
            color: '#9CA3AF',
          }}>
            <p style={{ fontSize: '14px' }}>No artifacts found</p>
          </div>
        ) : (
          <div style={{ 
            display: isExpanded ? 'grid' : 'flex',
            gridTemplateColumns: isExpanded ? 'repeat(auto-fill, minmax(300px, 1fr))' : 'none',
            flexDirection: isExpanded ? 'row' : 'column',
            gap: isExpanded ? '16px' : '12px'
          }}>
            {filterArtifacts().map(artifact => (
              <div
                key={artifact.id}
                style={{
                  padding: isExpanded ? '20px' : '16px',
                  background: '#FFFFFF',
                  border: '1px solid #E5E7EB',
                  borderRadius: '12px',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = '#8629FF';
                  e.currentTarget.style.boxShadow = '0 2px 8px rgba(134, 41, 255, 0.15)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = '#E5E7EB';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                {/* Icon and Title */}
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'flex-start',
                  gap: '12px',
                  marginBottom: '8px'
                }}>
                  <div style={{ 
                    fontSize: '24px',
                    lineHeight: 1
                  }}>
                    {artifact.icon}
                  </div>
                  <div style={{ flex: 1 }}>
                    <h4 style={{ 
                      fontSize: '14px', 
                      fontWeight: '600',
                      color: '#111827',
                      marginBottom: '4px'
                    }}>
                      {artifact.title}
                    </h4>
                    <p style={{ 
                      fontSize: '13px', 
                      color: '#6B7280',
                      lineHeight: '1.4'
                    }}>
                      {artifact.description}
                    </p>
                  </div>
                </div>

                {/* Footer */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginTop: '12px',
                  paddingTop: '12px',
                  borderTop: '1px solid #F3F4F6'
                }}>
                  <span style={{ 
                    fontSize: '12px', 
                    color: '#9CA3AF'
                  }}>
                    {new Date(artifact.date).toLocaleDateString()}
                  </span>
                  <button style={{
                    padding: '4px 12px',
                    borderRadius: '6px',
                    border: 'none',
                    background: '#EEEBFF',
                    color: '#8629FF',
                    fontSize: '12px',
                    fontWeight: '500',
                    cursor: 'pointer',
                  }}>
                    Open
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Upload Button */}
      <div style={{
        padding: isExpanded ? '20px 24px' : '16px',
        borderTop: '1px solid #E5E7EB',
        background: '#FFFFFF',
        flexShrink: 0,
      }}>
        <button style={{
          width: '100%',
          padding: '12px',
          borderRadius: '10px',
          border: '2px dashed #D1D5DB',
          background: '#F9FAFB',
          color: '#6B7280',
          fontSize: '14px',
          fontWeight: '500',
          cursor: 'pointer',
          transition: 'all 0.2s',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.borderColor = '#8629FF';
          e.currentTarget.style.color = '#8629FF';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.borderColor = '#D1D5DB';
          e.currentTarget.style.color = '#6B7280';
        }}
        >
          + Upload New Artifact
        </button>
      </div>

      {/* Custom Scrollbar Styling */}
      <style>{`
        /* Webkit browsers (Chrome, Safari, Edge) */
        div::-webkit-scrollbar {
          width: 6px;
          height: 6px;
        }

        div::-webkit-scrollbar-track {
          background: #F3F4F6;
          border-radius: 3px;
        }

        div::-webkit-scrollbar-thumb {
          background: #D1D5DB;
          border-radius: 3px;
        }

        div::-webkit-scrollbar-thumb:hover {
          background: #9CA3AF;
        }
      `}</style>
    </div>
  );
};

export default ArtifactsPanel;