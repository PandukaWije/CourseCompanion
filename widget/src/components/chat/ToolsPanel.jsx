import React, { useState } from 'react';
import { Maximize2, X } from 'lucide-react';
import { ToolButton } from './ToolButton';
import { ArtifactsPanel } from './ArtifactsPanel';
import { NotesPanel } from './NotesPanel';
import { QuizPanel } from './QuizPanel';
import { MindMapPanel } from './MindMapPanel';

/**
 * ToolsPanel Component
 * Shows tools in small panel with expand option for full-screen modal
 */
export const ToolsPanel = () => {
  const [activeTool, setActiveTool] = useState(null);
  const [expandedTool, setExpandedTool] = useState(null);

  const tools = [
    { id: 'artifacts', label: 'Artifacts', icon: '📦' },
    { id: 'notes', label: 'Notes', icon: '📝' },
    { id: 'quiz', label: 'Quiz', icon: '📊' },
    { id: 'mindmap', label: 'Mind Map', icon: '🗺️' },
  ];

  const handleToolClick = (toolId) => {
    setActiveTool(activeTool === toolId ? null : toolId);
  };

  const handleExpandTool = (toolId) => {
    setExpandedTool(toolId);
    document.body.style.overflow = 'hidden';
  };

  const handleCloseExpanded = () => {
    setExpandedTool(null);
    document.body.style.overflow = 'auto';
  };

  const renderToolContent = (toolId, isExpanded = false) => {
    switch (toolId) {
      case 'artifacts':
        return <ArtifactsPanel isExpanded={isExpanded} />;
      case 'notes':
        return <NotesPanel isExpanded={isExpanded} />;
      case 'quiz':
        return <QuizPanel isExpanded={isExpanded} />;
      case 'mindmap':
        return <MindMapPanel isExpanded={isExpanded} />;
      default:
        return null;
    }
  };

  const getToolTitle = (toolId) => {
    return tools.find(t => t.id === toolId)?.label || '';
  };

  return (
    <>
      {/* Regular Tools Panel */}
      <div className="cc-tools-panel">
        {/* Tools Grid */}
        <div className="cc-tools-grid">
          {tools.map((tool) => (
            <ToolButton
              key={tool.id}
              icon={tool.icon}
              label={tool.label}
              onClick={() => handleToolClick(tool.id)}
              active={activeTool === tool.id}
            />
          ))}
        </div>

        {/* Content Preview Area */}
        <div className="cc-tools-content">
          {activeTool ? (
            <div style={{ height: '100%', display: 'flex', flexDirection: 'column', }}>
              {/* Expand Button */}
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '12px 16px',
                borderBottom: '1px solid #E5E7EB',
              }}>
                <h3 style={{
                  fontSize: '16px',
                  fontWeight: '600',
                  color: '#111827',
                }}>
                  {getToolTitle(activeTool)}
                </h3>
                <button
                  onClick={() => handleExpandTool(activeTool)}
                  style={{
                    padding: '6px 12px',
                    borderRadius: '8px',
                    border: '1px solid #E5E7EB',
                    background: '#FFFFFF',
                    color: '#6B7280',
                    fontSize: '13px',
                    fontWeight: '500',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    transition: 'all 0.2s',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = '#F9FAFB';
                    e.currentTarget.style.color = '#8629FF';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = '#FFFFFF';
                    e.currentTarget.style.color = '#6B7280';
                  }}
                >
                  <Maximize2 size={14} />
                  <span>Expand</span>
                </button>
              </div>

              {/* Tool Content (Compact View) */}
              <div style={{ flex: 1, overflow: 'hidden' }}>
                {renderToolContent(activeTool, false)}
              </div>
            </div>
          ) : (
            <div style={{ 
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              textAlign: 'center', 
              color: '#9CA3AF', 
              padding: '32px 16px'
            }}>
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>🎯</div>
              <p style={{ fontSize: '16px', fontWeight: '500', color: '#6B7280', marginBottom: '8px' }}>
                Select a tool to get started
              </p>
              <p style={{ fontSize: '14px', lineHeight: '1.5' }}>
                Choose from Artifacts, Notes, Quiz, or Mind Map to enhance your learning experience
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Full-Screen Modal */}
      {expandedTool && (
        <div 
          className="cc-tool-modal-overlay"
          onClick={handleCloseExpanded}
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0, 0, 0, 0.4)',
            backdropFilter: 'blur(4px)',
            zIndex: 10000,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            animation: 'cc-fadeIn 0.2s ease',
          }}
        >
          <div 
            className="cc-tool-modal"
            onClick={(e) => e.stopPropagation()}
            style={{
              width: '90%',
              maxWidth: '1400px',
              height: '90vh',
              background: '#FFFFFF',
              borderRadius: '16px',
              boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
              display: 'flex',
              flexDirection: 'column',
              animation: 'cc-slideUp 0.3s ease',
              overflow: 'hidden',
            }}
          >
            {/* Modal Header */}
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '20px 24px',
              borderBottom: '1px solid #E5E7EB',
              background: 'linear-gradient(90deg, #8629FF 0%, #FF1F38 100%)',
            }}>
              <button
                onClick={handleCloseExpanded}
                style={{
                  padding: '8px 16px',
                  borderRadius: '8px',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  background: 'rgba(255, 255, 255, 0.15)',
                  color: '#FFFFFF',
                  fontSize: '14px',
                  fontWeight: '500',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  transition: 'all 0.2s',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.25)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.15)';
                }}
              >
                ← Back to Chat
              </button>

              <h2 style={{
                fontSize: '20px',
                fontWeight: '600',
                color: '#FFFFFF',
                margin: 0,
              }}>
                {getToolTitle(expandedTool)}
              </h2>

              <button
                onClick={handleCloseExpanded}
                style={{
                  padding: '8px',
                  borderRadius: '8px',
                  border: 'none',
                  background: 'rgba(255, 255, 255, 0.15)',
                  color: '#FFFFFF',
                  fontSize: '20px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: '36px',
                  height: '36px',
                  transition: 'all 0.2s',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.25)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.15)';
                }}
              >
                <X size={20} />
              </button>
            </div>

            {/* Modal Content */}
            <div style={{
              flex: 1,
              overflow: 'auto',
              background: '#F9FAFB',
            }}>
              {renderToolContent(expandedTool, true)}
            </div>
          </div>
        </div>
      )}

      {/* CSS Animations */}
      <style>{`
        @keyframes cc-fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        @keyframes cc-slideUp {
          from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }

        /* Smooth scrollbar for modal */
        .cc-tool-modal::-webkit-scrollbar {
          width: 8px;
        }

        .cc-tool-modal::-webkit-scrollbar-track {
          background: #F3F4F6;
        }

        .cc-tool-modal::-webkit-scrollbar-thumb {
          background: #D1D5DB;
          border-radius: 4px;
        }

        .cc-tool-modal::-webkit-scrollbar-thumb:hover {
          background: #9CA3AF;
        }
      `}</style>
    </>
  );
};

export default ToolsPanel;