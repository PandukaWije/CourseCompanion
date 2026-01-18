import React, { useState } from 'react';

/**
 * MindMapPanel Component
 * Visualizes concepts and their relationships
 */
export const MindMapPanel = () => {
  const [mindMaps] = useState([
    {
      id: 1,
      title: 'Course Overview',
      nodes: 12,
      lastModified: new Date('2024-01-18'),
      thumbnail: '🌳',
    },
    {
      id: 2,
      title: 'Chapter 1 Concepts',
      nodes: 8,
      lastModified: new Date('2024-01-17'),
      thumbnail: '🧩',
    },
    {
      id: 3,
      title: 'Study Techniques',
      nodes: 15,
      lastModified: new Date('2024-01-16'),
      thumbnail: '📚',
    },
  ]);

  const [selectedMap, setSelectedMap] = useState(null);
  const [viewMode, setViewMode] = useState('list'); // 'list' or 'canvas'

  // Sample mind map structure
  const sampleMindMap = {
    id: 1,
    title: 'Study Techniques',
    centerNode: {
      id: 'center',
      label: 'Effective Learning',
      x: 50,
      y: 50,
    },
    nodes: [
      {
        id: 'active',
        label: 'Active Recall',
        x: 30,
        y: 30,
        color: '#8629FF',
        children: ['flashcards', 'self-testing'],
      },
      {
        id: 'spaced',
        label: 'Spaced Repetition',
        x: 70,
        y: 30,
        color: '#FF1F38',
        children: ['schedule', 'intervals'],
      },
      {
        id: 'interleaving',
        label: 'Interleaving',
        x: 30,
        y: 70,
        color: '#10B981',
        children: ['mix-topics', 'practice'],
      },
      {
        id: 'elaboration',
        label: 'Elaboration',
        x: 70,
        y: 70,
        color: '#F59E0B',
        children: ['explain', 'connect'],
      },
      // Child nodes
      {
        id: 'flashcards',
        label: 'Flashcards',
        x: 20,
        y: 20,
        parent: 'active',
        isChild: true,
      },
      {
        id: 'self-testing',
        label: 'Self-Testing',
        x: 25,
        y: 35,
        parent: 'active',
        isChild: true,
      },
      {
        id: 'schedule',
        label: 'Schedule',
        x: 75,
        y: 20,
        parent: 'spaced',
        isChild: true,
      },
      {
        id: 'intervals',
        label: 'Intervals',
        x: 80,
        y: 35,
        parent: 'spaced',
        isChild: true,
      },
    ],
  };

  const handleViewMap = (map) => {
    setSelectedMap(sampleMindMap);
    setViewMode('canvas');
  };

  const handleBackToList = () => {
    setSelectedMap(null);
    setViewMode('list');
  };

  const formatDate = (date) => {
    const now = new Date();
    const diff = now - new Date(date);
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    if (days < 7) return `${days} days ago`;
    return new Date(date).toLocaleDateString();
  };

  if (viewMode === 'canvas' && selectedMap) {
    return (
      <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        {/* Canvas Header */}
        <div style={{ padding: '16px', borderBottom: '1px solid #E5E7EB' }}>
          <button
            onClick={handleBackToList}
            style={{
              padding: '6px 12px',
              borderRadius: '8px',
              border: '1px solid #E5E7EB',
              background: '#FFFFFF',
              color: '#6B7280',
              fontSize: '13px',
              fontWeight: '500',
              cursor: 'pointer',
              marginBottom: '12px',
            }}
          >
            ← Back to Mind Maps
          </button>
          <h3 style={{ 
            fontSize: '16px', 
            fontWeight: '600',
            color: '#111827',
          }}>
            {selectedMap.title}
          </h3>
        </div>

        {/* Canvas Area */}
        <div style={{ 
          flex: 1, 
          position: 'relative',
          background: '#F9FAFB',
          overflow: 'hidden',
        }}>
          {/* Grid Background */}
          <div style={{
            position: 'absolute',
            inset: 0,
            backgroundImage: `
              linear-gradient(to right, #E5E7EB 1px, transparent 1px),
              linear-gradient(to bottom, #E5E7EB 1px, transparent 1px)
            `,
            backgroundSize: '20px 20px',
            opacity: 0.5,
          }} />

          {/* Mind Map Visualization */}
          <div style={{
            position: 'relative',
            width: '100%',
            height: '100%',
            padding: '40px',
          }}>
            {/* Center Node */}
            <div style={{
              position: 'absolute',
              left: `${selectedMap.centerNode.x}%`,
              top: `${selectedMap.centerNode.y}%`,
              transform: 'translate(-50%, -50%)',
              padding: '20px 28px',
              background: 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)',
              borderRadius: '50%',
              color: '#FFFFFF',
              fontSize: '15px',
              fontWeight: '600',
              boxShadow: '0 4px 12px rgba(134, 41, 255, 0.3)',
              zIndex: 10,
              minWidth: '140px',
              textAlign: 'center',
            }}>
              {selectedMap.centerNode.label}
            </div>

            {/* Main Branch Nodes */}
            {selectedMap.nodes.filter(node => !node.isChild).map((node) => (
              <div key={node.id}>
                {/* Connection Line */}
                <svg
                  style={{
                    position: 'absolute',
                    inset: 0,
                    pointerEvents: 'none',
                    zIndex: 1,
                  }}
                >
                  <line
                    x1={`${selectedMap.centerNode.x}%`}
                    y1={`${selectedMap.centerNode.y}%`}
                    x2={`${node.x}%`}
                    y2={`${node.y}%`}
                    stroke={node.color}
                    strokeWidth="2"
                    opacity="0.4"
                  />
                </svg>

                {/* Node */}
                <div style={{
                  position: 'absolute',
                  left: `${node.x}%`,
                  top: `${node.y}%`,
                  transform: 'translate(-50%, -50%)',
                  padding: '12px 20px',
                  background: '#FFFFFF',
                  border: `3px solid ${node.color}`,
                  borderRadius: '12px',
                  fontSize: '13px',
                  fontWeight: '600',
                  color: node.color,
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                  zIndex: 5,
                  minWidth: '100px',
                  textAlign: 'center',
                  cursor: 'pointer',
                }}>
                  {node.label}
                </div>

                {/* Child Nodes */}
                {node.children && selectedMap.nodes
                  .filter(child => child.parent === node.id)
                  .map((child) => (
                    <div key={child.id}>
                      {/* Connection Line */}
                      <svg
                        style={{
                          position: 'absolute',
                          inset: 0,
                          pointerEvents: 'none',
                          zIndex: 2,
                        }}
                      >
                        <line
                          x1={`${node.x}%`}
                          y1={`${node.y}%`}
                          x2={`${child.x}%`}
                          y2={`${child.y}%`}
                          stroke={node.color}
                          strokeWidth="1"
                          strokeDasharray="4"
                          opacity="0.3"
                        />
                      </svg>

                      {/* Child Node */}
                      <div style={{
                        position: 'absolute',
                        left: `${child.x}%`,
                        top: `${child.y}%`,
                        transform: 'translate(-50%, -50%)',
                        padding: '8px 14px',
                        background: '#F9FAFB',
                        border: `2px solid ${node.color}`,
                        borderRadius: '8px',
                        fontSize: '11px',
                        fontWeight: '500',
                        color: '#6B7280',
                        boxShadow: '0 1px 4px rgba(0, 0, 0, 0.08)',
                        zIndex: 3,
                        cursor: 'pointer',
                      }}>
                        {child.label}
                      </div>
                    </div>
                  ))}
              </div>
            ))}
          </div>
        </div>

        {/* Canvas Footer */}
        <div style={{
          padding: '12px 16px',
          borderTop: '1px solid #E5E7EB',
          background: '#FFFFFF',
          display: 'flex',
          gap: '8px',
          justifyContent: 'space-between',
        }}>
          <button style={{
            padding: '8px 16px',
            borderRadius: '8px',
            border: '1px solid #E5E7EB',
            background: '#FFFFFF',
            color: '#6B7280',
            fontSize: '13px',
            fontWeight: '500',
            cursor: 'pointer',
          }}>
            Export
          </button>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button style={{
              padding: '8px 16px',
              borderRadius: '8px',
              border: 'none',
              background: '#EEEBFF',
              color: '#8629FF',
              fontSize: '13px',
              fontWeight: '500',
              cursor: 'pointer',
            }}>
              Add Node
            </button>
            <button style={{
              padding: '8px 16px',
              borderRadius: '8px',
              border: 'none',
              background: 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)',
              color: '#FFFFFF',
              fontSize: '13px',
              fontWeight: '500',
              cursor: 'pointer',
            }}>
              Save Changes
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <div style={{ padding: '16px', borderBottom: '1px solid #E5E7EB' }}>
        <h3 style={{ 
          fontSize: '18px', 
          fontWeight: '600',
          color: '#111827',
          marginBottom: '4px',
        }}>
          Mind Map
        </h3>
        <p style={{ 
          fontSize: '13px', 
          color: '#6B7280' 
        }}>
          Visualize concepts and connections
        </p>
      </div>

      {/* Mind Maps List */}
      <div style={{ 
        flex: 1, 
        overflowY: 'auto',
        padding: '16px',
      }}>
        {mindMaps.length === 0 ? (
          <div style={{
            textAlign: 'center',
            padding: '32px 16px',
            color: '#9CA3AF',
          }}>
            <div style={{ fontSize: '48px', marginBottom: '12px' }}>🗺️</div>
            <p style={{ fontSize: '14px', marginBottom: '4px' }}>No mind maps yet</p>
            <p style={{ fontSize: '12px' }}>
              Create your first mind map to visualize concepts
            </p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {mindMaps.map(map => (
              <div
                key={map.id}
                onClick={() => handleViewMap(map)}
                style={{
                  padding: '16px',
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
                {/* Header */}
                <div style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '12px',
                  marginBottom: '12px',
                }}>
                  <div style={{
                    width: '48px',
                    height: '48px',
                    borderRadius: '10px',
                    background: 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '24px',
                    flexShrink: 0,
                  }}>
                    {map.thumbnail}
                  </div>
                  <div style={{ flex: 1 }}>
                    <h4 style={{ 
                      fontSize: '14px', 
                      fontWeight: '600',
                      color: '#111827',
                      marginBottom: '4px',
                    }}>
                      {map.title}
                    </h4>
                    <div style={{
                      fontSize: '12px',
                      color: '#6B7280',
                    }}>
                      {map.nodes} nodes
                    </div>
                  </div>
                </div>

                {/* Mini Preview */}
                <div style={{
                  height: '60px',
                  background: '#F9FAFB',
                  borderRadius: '8px',
                  position: 'relative',
                  overflow: 'hidden',
                  marginBottom: '12px',
                }}>
                  {/* Simplified visualization */}
                  <div style={{
                    position: 'absolute',
                    left: '50%',
                    top: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: '20px',
                    height: '20px',
                    borderRadius: '50%',
                    background: 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)',
                  }} />
                  {[...Array(4)].map((_, i) => (
                    <div
                      key={i}
                      style={{
                        position: 'absolute',
                        width: '12px',
                        height: '12px',
                        borderRadius: '50%',
                        background: '#D1D5DB',
                        left: `${25 + i * 15}%`,
                        top: i % 2 === 0 ? '25%' : '65%',
                      }}
                    />
                  ))}
                </div>

                {/* Footer */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}>
                  <span style={{ 
                    fontSize: '12px', 
                    color: '#9CA3AF'
                  }}>
                    Updated {formatDate(map.lastModified)}
                  </span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleViewMap(map);
                    }}
                    style={{
                      padding: '4px 12px',
                      borderRadius: '6px',
                      border: 'none',
                      background: '#EEEBFF',
                      color: '#8629FF',
                      fontSize: '12px',
                      fontWeight: '500',
                      cursor: 'pointer',
                    }}
                  >
                    View
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Create New Button */}
      <div style={{
        padding: '16px',
        borderTop: '1px solid #E5E7EB',
      }}>
        <button style={{
          width: '100%',
          padding: '12px',
          borderRadius: '10px',
          border: 'none',
          background: 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)',
          color: '#FFFFFF',
          fontSize: '14px',
          fontWeight: '500',
          cursor: 'pointer',
        }}>
          ✨ Create New Mind Map
        </button>
      </div>
    </div>
  );
};

export default MindMapPanel;