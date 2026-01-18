import React, { useState } from 'react';
import { History, MessageSquarePlus } from 'lucide-react';
import { ChatHistory } from './ChatHistory';
import { useWidgetStore } from '../../store/widgetStore';

/**
 * ChatHeader Component
 * Shows header with title, new chat button, and chat history access
 */
export const ChatHeader = () => {
  const [showHistory, setShowHistory] = useState(false);
  const { selectedCourses } = useWidgetStore();

  const handleOpenChat = (chatId, courses) => {
    // If courses provided (from context switch), update selected courses
    if (courses) {
      // TODO: Update selected courses in store
      console.log('Switching to courses:', courses);
    }
    
    // Close history
    setShowHistory(false);
    
    // TODO: Load chat messages for chatId
    console.log('Opening chat:', chatId);
  };

  const handleStartNewChat = (courses) => {
    setShowHistory(false);
    // TODO: Create new chat with courses
    console.log('Starting new chat with courses:', courses);
  };

  return (
    <>
      {/* Header Bar */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '16px 20px',
        borderBottom: '1px solid #E5E7EB',
        background: '#FFFFFF',
      }}>
        {/* Title */}
        <div>
          <h1 style={{
            fontSize: '20px',
            fontWeight: '600',
            color: '#111827',
            marginBottom: '4px',
          }}>
            Course Companion
          </h1>
          {selectedCourses && selectedCourses.length > 0 && (
            <p style={{
              fontSize: '13px',
              color: '#6B7280',
            }}>
              {selectedCourses.map(c => c.name).join(', ')}
            </p>
          )}
        </div>

        {/* Actions */}
        <div style={{
          display: 'flex',
          gap: '12px',
          alignItems: 'center',
        }}>
          {/* Chat History Button */}
          <button
            onClick={() => setShowHistory(!showHistory)}
            style={{
              padding: '8px 16px',
              borderRadius: '8px',
              border: '1px solid #E5E7EB',
              background: showHistory ? '#EEEBFF' : '#FFFFFF',
              color: showHistory ? '#8629FF' : '#6B7280',
              fontSize: '14px',
              fontWeight: '500',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'all 0.2s',
            }}
            onMouseEnter={(e) => {
              if (!showHistory) {
                e.currentTarget.style.background = '#F9FAFB';
              }
            }}
            onMouseLeave={(e) => {
              if (!showHistory) {
                e.currentTarget.style.background = '#FFFFFF';
              }
            }}
          >
            <History size={16} />
            <span>History</span>
          </button>

          {/* New Chat Button */}
          <button
            onClick={() => handleStartNewChat(selectedCourses)}
            style={{
              padding: '8px 16px',
              borderRadius: '8px',
              border: 'none',
              background: 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)',
              color: '#FFFFFF',
              fontSize: '14px',
              fontWeight: '500',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'all 0.2s',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-1px)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(134, 41, 255, 0.3)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <MessageSquarePlus size={16} />
            <span>New Chat</span>
          </button>
        </div>
      </div>

      {/* Chat History Sidebar */}
      {showHistory && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 9999,
            display: 'flex',
          }}
          onClick={() => setShowHistory(false)}
        >
          {/* Backdrop */}
          <div
            style={{
              flex: 1,
              background: 'rgba(0, 0, 0, 0.3)',
              backdropFilter: 'blur(2px)',
              animation: 'cc-fadeIn 0.2s ease',
            }}
          />
          
          {/* Sidebar */}
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              width: '400px',
              background: '#FFFFFF',
              boxShadow: '-4px 0 24px rgba(0, 0, 0, 0.15)',
              animation: 'cc-slideInRight 0.3s ease',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <ChatHistory
              selectedCourses={selectedCourses}
              onOpenChat={handleOpenChat}
              onStartNewChat={handleStartNewChat}
            />
          </div>
        </div>
      )}

      {/* Animations */}
      <style>{`
        @keyframes cc-fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }

        @keyframes cc-slideInRight {
          from {
            opacity: 0;
            transform: translateX(100%);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }
      `}</style>
    </>
  );
};

export default ChatHeader;