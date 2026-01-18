import React, { useState } from 'react';
import { MessageSquare, Clock, Tag } from 'lucide-react';

/**
 * ChatHistory Component
 * Displays chat history with immutable course context
 * Shows course tags and handles context mismatches
 */
export const ChatHistory = ({ selectedCourses, onOpenChat, onStartNewChat }) => {
  const [filterMode, setFilterMode] = useState('related'); // 'related' | 'exact' | 'all'
  const [showContextModal, setShowContextModal] = useState(false);
  const [pendingChat, setPendingChat] = useState(null);

  // Mock chat data with course context
  const [chatHistory] = useState([
    {
      chatId: 'chat_001',
      title: 'Python Basics and C++ Pointers',
      courseContext: [
        { id: 'py101', name: 'Python Fundamentals', primary: true },
        { id: 'cpp201', name: 'C++ Advanced', primary: false }
      ],
      lastMessage: 'Can you explain the difference between pointers in C++ and references in Python?',
      messageCount: 24,
      lastActivity: new Date('2024-01-18T10:30:00'),
      createdAt: new Date('2024-01-18T09:15:00'),
    },
    {
      chatId: 'chat_002',
      title: 'DevOps CI/CD Pipeline Setup',
      courseContext: [
        { id: 'devops301', name: 'DevOps Fundamentals', primary: true },
        { id: 'py101', name: 'Python Fundamentals', primary: false }
      ],
      lastMessage: 'How do I configure GitHub Actions for automated testing?',
      messageCount: 15,
      lastActivity: new Date('2024-01-17T15:45:00'),
      createdAt: new Date('2024-01-17T14:20:00'),
    },
    {
      chatId: 'chat_003',
      title: 'Data Structures Quiz Prep',
      courseContext: [
        { id: 'py101', name: 'Python Fundamentals', primary: true },
        { id: 'cpp201', name: 'C++ Advanced', primary: false }
      ],
      lastMessage: 'What are the time complexities for common operations on hash tables?',
      messageCount: 31,
      lastActivity: new Date('2024-01-16T11:20:00'),
      createdAt: new Date('2024-01-16T09:00:00'),
    },
    {
      chatId: 'chat_004',
      title: 'ML Model Deployment',
      courseContext: [
        { id: 'ml401', name: 'Machine Learning', primary: true },
        { id: 'devops301', name: 'DevOps Fundamentals', primary: false }
      ],
      lastMessage: 'Best practices for deploying ML models in production?',
      messageCount: 18,
      lastActivity: new Date('2024-01-15T14:30:00'),
      createdAt: new Date('2024-01-15T13:00:00'),
    },
  ]);

  // Helper functions for course matching
  const getSelectedCourseIds = () => selectedCourses.map(c => c.id);

  const matchesExactly = (chatCourses, selectedCourseIds) => {
    const chatCourseIds = chatCourses.map(c => c.id).sort();
    const selectedIds = [...selectedCourseIds].sort();
    
    return chatCourseIds.length === selectedIds.length &&
           chatCourseIds.every((id, index) => id === selectedIds[index]);
  };

  const hasOverlap = (chatCourses, selectedCourseIds) => {
    return chatCourses.some(course => selectedCourseIds.includes(course.id));
  };

  const getMatchType = (chat) => {
    const selectedIds = getSelectedCourseIds();
    
    if (matchesExactly(chat.courseContext, selectedIds)) return 'exact';
    if (hasOverlap(chat.courseContext, selectedIds)) return 'partial';
    return 'none';
  };

  // Filter chats based on selected mode
  const filterChats = () => {
    const selectedIds = getSelectedCourseIds();
    
    switch (filterMode) {
      case 'exact':
        return chatHistory.filter(chat => matchesExactly(chat.courseContext, selectedIds));
      case 'related':
        return chatHistory.filter(chat => hasOverlap(chat.courseContext, selectedIds));
      case 'all':
        return chatHistory;
      default:
        return chatHistory;
    }
  };

  const handleChatClick = (chat) => {
    const matchType = getMatchType(chat);
    
    if (matchType === 'exact') {
      // Perfect match - open directly
      onOpenChat(chat.chatId);
    } else {
      // Show context mismatch modal
      setPendingChat(chat);
      setShowContextModal(true);
    }
  };

  const handleContinueWithOriginal = () => {
    if (pendingChat) {
      // Switch to original courses and open chat
      const originalCourses = pendingChat.courseContext;
      onOpenChat(pendingChat.chatId, originalCourses);
      setShowContextModal(false);
      setPendingChat(null);
    }
  };

  const handleStartNewWithCurrent = () => {
    setShowContextModal(false);
    setPendingChat(null);
    onStartNewChat(selectedCourses);
  };

  const formatDate = (date) => {
    const now = new Date();
    const diff = now - new Date(date);
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (minutes < 60) return `${minutes} min ago`;
    if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    if (days === 1) return 'Yesterday';
    if (days < 7) return `${days} days ago`;
    return new Date(date).toLocaleDateString();
  };

  const filteredChats = filterChats();

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <div style={{ padding: '16px 20px', borderBottom: '1px solid #E5E7EB' }}>
        <h2 style={{ 
          fontSize: '20px', 
          fontWeight: '600', 
          color: '#111827',
          marginBottom: '8px' 
        }}>
          Chat History
        </h2>
        <p style={{ fontSize: '14px', color: '#6B7280' }}>
          Showing chats for your selected courses
        </p>
      </div>

      {/* Filter Tabs */}
      <div style={{
        display: 'flex',
        gap: '8px',
        padding: '12px 20px',
        borderBottom: '1px solid #E5E7EB',
        background: '#F9FAFB',
      }}>
        <button
          onClick={() => setFilterMode('related')}
          style={{
            padding: '8px 16px',
            borderRadius: '8px',
            border: 'none',
            background: filterMode === 'related' 
              ? 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)' 
              : '#FFFFFF',
            color: filterMode === 'related' ? '#FFFFFF' : '#6B7280',
            fontSize: '13px',
            fontWeight: '500',
            cursor: 'pointer',
            transition: 'all 0.2s',
          }}
        >
          Related ({chatHistory.filter(c => hasOverlap(c.courseContext, getSelectedCourseIds())).length})
        </button>
        <button
          onClick={() => setFilterMode('exact')}
          style={{
            padding: '8px 16px',
            borderRadius: '8px',
            border: 'none',
            background: filterMode === 'exact' 
              ? 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)' 
              : '#FFFFFF',
            color: filterMode === 'exact' ? '#FFFFFF' : '#6B7280',
            fontSize: '13px',
            fontWeight: '500',
            cursor: 'pointer',
            transition: 'all 0.2s',
          }}
        >
          Exact Match ({chatHistory.filter(c => matchesExactly(c.courseContext, getSelectedCourseIds())).length})
        </button>
        <button
          onClick={() => setFilterMode('all')}
          style={{
            padding: '8px 16px',
            borderRadius: '8px',
            border: 'none',
            background: filterMode === 'all' 
              ? 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)' 
              : '#FFFFFF',
            color: filterMode === 'all' ? '#FFFFFF' : '#6B7280',
            fontSize: '13px',
            fontWeight: '500',
            cursor: 'pointer',
            transition: 'all 0.2s',
          }}
        >
          All Chats ({chatHistory.length})
        </button>
      </div>

      {/* Chat List */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px 20px' }}>
        {filteredChats.length === 0 ? (
          <div style={{
            textAlign: 'center',
            padding: '48px 20px',
            color: '#9CA3AF',
          }}>
            <MessageSquare size={48} style={{ margin: '0 auto 16px' }} />
            <p style={{ fontSize: '16px', fontWeight: '500', color: '#6B7280', marginBottom: '8px' }}>
              No chats found
            </p>
            <p style={{ fontSize: '14px' }}>
              {filterMode === 'exact' 
                ? 'No chats match your exact course selection'
                : 'Start a new chat to get started'}
            </p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {filteredChats.map(chat => {
              const matchType = getMatchType(chat);
              
              return (
                <div
                  key={chat.chatId}
                  onClick={() => handleChatClick(chat)}
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
                  {/* Title */}
                  <h3 style={{
                    fontSize: '15px',
                    fontWeight: '600',
                    color: '#111827',
                    marginBottom: '8px',
                  }}>
                    {chat.title}
                  </h3>

                  {/* Course Tags */}
                  <div style={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: '6px',
                    marginBottom: '12px',
                  }}>
                    {chat.courseContext.map(course => {
                      const isMatched = getSelectedCourseIds().includes(course.id);
                      
                      return (
                        <span
                          key={course.id}
                          style={{
                            padding: '4px 10px',
                            borderRadius: '6px',
                            background: isMatched ? '#EEEBFF' : '#F3F4F6',
                            color: isMatched ? '#8629FF' : '#6B7280',
                            fontSize: '12px',
                            fontWeight: '500',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px',
                          }}
                        >
                          <Tag size={12} />
                          {course.name}
                          {isMatched && <span>✓</span>}
                        </span>
                      );
                    })}
                  </div>

                  {/* Match Warning */}
                  {matchType !== 'exact' && (
                    <div style={{
                      padding: '8px 12px',
                      borderRadius: '8px',
                      background: matchType === 'partial' ? '#FEF3C7' : '#FEE2E2',
                      border: `1px solid ${matchType === 'partial' ? '#F59E0B' : '#EF4444'}`,
                      marginBottom: '12px',
                    }}>
                      <p style={{
                        fontSize: '12px',
                        color: matchType === 'partial' ? '#854D0E' : '#991B1B',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                      }}>
                        ⚠️ {matchType === 'partial' 
                          ? 'Different course selection - click to switch' 
                          : 'Unrelated courses'}
                      </p>
                    </div>
                  )}

                  {/* Last Message Preview */}
                  <p style={{
                    fontSize: '13px',
                    color: '#6B7280',
                    lineHeight: '1.5',
                    marginBottom: '12px',
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden',
                  }}>
                    {chat.lastMessage}
                  </p>

                  {/* Footer */}
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    fontSize: '12px',
                    color: '#9CA3AF',
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Clock size={12} />
                        {formatDate(chat.lastActivity)}
                      </span>
                      <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <MessageSquare size={12} />
                        {chat.messageCount} messages
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Context Mismatch Modal */}
      {showContextModal && pendingChat && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0, 0, 0, 0.5)',
            backdropFilter: 'blur(4px)',
            zIndex: 10001,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            animation: 'cc-fadeIn 0.2s ease',
          }}
          onClick={() => {
            setShowContextModal(false);
            setPendingChat(null);
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              width: '90%',
              maxWidth: '500px',
              background: '#FFFFFF',
              borderRadius: '16px',
              padding: '24px',
              boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
              animation: 'cc-slideUp 0.3s ease',
            }}
          >
            <h3 style={{
              fontSize: '18px',
              fontWeight: '600',
              color: '#111827',
              marginBottom: '16px',
            }}>
              ⚠️ Different Course Context
            </h3>

            <p style={{
              fontSize: '14px',
              color: '#6B7280',
              lineHeight: '1.6',
              marginBottom: '20px',
            }}>
              This chat was created with different courses. Choose how you'd like to proceed:
            </p>

            {/* Course Comparison */}
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '16px',
              marginBottom: '24px',
            }}>
              {/* Original Courses */}
              <div>
                <p style={{
                  fontSize: '12px',
                  fontWeight: '600',
                  color: '#6B7280',
                  marginBottom: '8px',
                }}>
                  Original Chat Courses:
                </p>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {pendingChat.courseContext.map(course => (
                    <span
                      key={course.id}
                      style={{
                        padding: '6px 12px',
                        borderRadius: '6px',
                        background: '#EEEBFF',
                        color: '#8629FF',
                        fontSize: '13px',
                        fontWeight: '500',
                      }}
                    >
                      {course.name}
                    </span>
                  ))}
                </div>
              </div>

              {/* Current Courses */}
              <div>
                <p style={{
                  fontSize: '12px',
                  fontWeight: '600',
                  color: '#6B7280',
                  marginBottom: '8px',
                }}>
                  Your Current Courses:
                </p>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {selectedCourses.map(course => (
                    <span
                      key={course.id}
                      style={{
                        padding: '6px 12px',
                        borderRadius: '6px',
                        background: '#F3F4F6',
                        color: '#6B7280',
                        fontSize: '13px',
                        fontWeight: '500',
                      }}
                    >
                      {course.name}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Actions */}
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '12px',
            }}>
              <button
                onClick={handleContinueWithOriginal}
                style={{
                  width: '100%',
                  padding: '12px 20px',
                  borderRadius: '10px',
                  border: 'none',
                  background: 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)',
                  color: '#FFFFFF',
                  fontSize: '14px',
                  fontWeight: '500',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                }}
              >
                Continue with Original Courses
              </button>
              <button
                onClick={handleStartNewWithCurrent}
                style={{
                  width: '100%',
                  padding: '12px 20px',
                  borderRadius: '10px',
                  border: '1px solid #E5E7EB',
                  background: '#FFFFFF',
                  color: '#6B7280',
                  fontSize: '14px',
                  fontWeight: '500',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                }}
              >
                Start New Chat with Current Courses
              </button>
              <button
                onClick={() => {
                  setShowContextModal(false);
                  setPendingChat(null);
                }}
                style={{
                  width: '100%',
                  padding: '12px 20px',
                  borderRadius: '10px',
                  border: 'none',
                  background: 'transparent',
                  color: '#9CA3AF',
                  fontSize: '14px',
                  fontWeight: '500',
                  cursor: 'pointer',
                }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatHistory;