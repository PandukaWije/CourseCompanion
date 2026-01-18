import React, { useState } from 'react';

/**
 * NotesPanel Component
 * Allows users to take notes and save important chat messages
 */
export const NotesPanel = () => {
  const [notes, setNotes] = useState([
    {
      id: 1,
      title: 'Key Concepts from Chat',
      content: 'Remember to review the three main principles discussed...',
      source: 'chat',
      timestamp: new Date('2024-01-18T10:30:00'),
      tags: ['important', 'review'],
    },
    {
      id: 2,
      title: 'Study Plan',
      content: 'Week 1: Focus on fundamentals\nWeek 2: Practice problems\nWeek 3: Review',
      source: 'manual',
      timestamp: new Date('2024-01-17T14:20:00'),
      tags: ['planning'],
    },
  ]);

  const [isAdding, setIsAdding] = useState(false);
  const [newNoteTitle, setNewNoteTitle] = useState('');
  const [newNoteContent, setNewNoteContent] = useState('');
  const [selectedNote, setSelectedNote] = useState(null);
  const [filter, setFilter] = useState('all');

  const handleAddNote = () => {
    if (!newNoteTitle.trim() || !newNoteContent.trim()) return;

    const newNote = {
      id: Date.now(),
      title: newNoteTitle,
      content: newNoteContent,
      source: 'manual',
      timestamp: new Date(),
      tags: [],
    };

    setNotes([newNote, ...notes]);
    setNewNoteTitle('');
    setNewNoteContent('');
    setIsAdding(false);
  };

  const handleSaveChatMessage = (message) => {
    // This would be called from the chat component
    const newNote = {
      id: Date.now(),
      title: `Chat Note - ${new Date().toLocaleDateString()}`,
      content: message,
      source: 'chat',
      timestamp: new Date(),
      tags: ['from-chat'],
    };
    setNotes([newNote, ...notes]);
  };

  const filterNotes = () => {
    if (filter === 'all') return notes;
    return notes.filter(note => note.source === filter);
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

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <div style={{ padding: '16px', borderBottom: '1px solid #E5E7EB' }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '8px'
        }}>
          <h3 style={{ 
            fontSize: '18px', 
            fontWeight: '600',
            color: '#111827'
          }}>
            Notes
          </h3>
          <button
            onClick={() => setIsAdding(true)}
            style={{
              padding: '6px 12px',
              borderRadius: '8px',
              border: 'none',
              background: 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)',
              color: '#FFFFFF',
              fontSize: '13px',
              fontWeight: '500',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
            }}
          >
            <span>+</span>
            <span>New Note</span>
          </button>
        </div>
        <p style={{ 
          fontSize: '13px', 
          color: '#6B7280',
          marginBottom: '12px'
        }}>
          Save important information and chat messages
        </p>

        {/* Filter Tabs */}
        <div style={{ display: 'flex', gap: '8px' }}>
          {['all', 'manual', 'chat'].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              style={{
                padding: '4px 12px',
                borderRadius: '6px',
                border: 'none',
                background: filter === f ? '#EEEBFF' : 'transparent',
                color: filter === f ? '#8629FF' : '#6B7280',
                fontSize: '12px',
                fontWeight: '500',
                cursor: 'pointer',
                textTransform: 'capitalize',
              }}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {/* Add Note Form */}
      {isAdding && (
        <div style={{
          padding: '16px',
          background: '#F9FAFB',
          borderBottom: '1px solid #E5E7EB',
        }}>
          <input
            type="text"
            placeholder="Note title..."
            value={newNoteTitle}
            onChange={(e) => setNewNoteTitle(e.target.value)}
            style={{
              width: '100%',
              padding: '10px',
              marginBottom: '8px',
              border: '1px solid #E5E7EB',
              borderRadius: '8px',
              fontSize: '14px',
              fontWeight: '500',
            }}
          />
          <textarea
            placeholder="Write your note..."
            value={newNoteContent}
            onChange={(e) => setNewNoteContent(e.target.value)}
            rows={4}
            style={{
              width: '100%',
              padding: '10px',
              marginBottom: '8px',
              border: '1px solid #E5E7EB',
              borderRadius: '8px',
              fontSize: '14px',
              resize: 'vertical',
              fontFamily: 'inherit',
            }}
          />
          <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
            <button
              onClick={() => {
                setIsAdding(false);
                setNewNoteTitle('');
                setNewNoteContent('');
              }}
              style={{
                padding: '8px 16px',
                borderRadius: '8px',
                border: '1px solid #E5E7EB',
                background: '#FFFFFF',
                color: '#6B7280',
                fontSize: '13px',
                fontWeight: '500',
                cursor: 'pointer',
              }}
            >
              Cancel
            </button>
            <button
              onClick={handleAddNote}
              style={{
                padding: '8px 16px',
                borderRadius: '8px',
                border: 'none',
                background: 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)',
                color: '#FFFFFF',
                fontSize: '13px',
                fontWeight: '500',
                cursor: 'pointer',
              }}
            >
              Save Note
            </button>
          </div>
        </div>
      )}

      {/* Notes List */}
      <div style={{ 
        flex: 1, 
        overflowY: 'auto',
        padding: '16px',
      }}>
        {filterNotes().length === 0 ? (
          <div style={{
            textAlign: 'center',
            padding: '32px 16px',
            color: '#9CA3AF',
          }}>
            <div style={{ fontSize: '32px', marginBottom: '8px' }}>📝</div>
            <p style={{ fontSize: '14px' }}>No notes yet</p>
            <p style={{ fontSize: '12px', marginTop: '4px' }}>
              Create a note or save messages from chat
            </p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {filterNotes().map(note => (
              <div
                key={note.id}
                onClick={() => setSelectedNote(note)}
                style={{
                  padding: '16px',
                  background: '#FFFFFF',
                  border: selectedNote?.id === note.id 
                    ? '2px solid #8629FF' 
                    : '1px solid #E5E7EB',
                  borderRadius: '12px',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                }}
                onMouseEnter={(e) => {
                  if (selectedNote?.id !== note.id) {
                    e.currentTarget.style.borderColor = '#D1D5DB';
                  }
                }}
                onMouseLeave={(e) => {
                  if (selectedNote?.id !== note.id) {
                    e.currentTarget.style.borderColor = '#E5E7EB';
                  }
                }}
              >
                {/* Header */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  marginBottom: '8px',
                }}>
                  <h4 style={{ 
                    fontSize: '14px', 
                    fontWeight: '600',
                    color: '#111827',
                    flex: 1,
                  }}>
                    {note.title}
                  </h4>
                  {note.source === 'chat' && (
                    <span style={{
                      padding: '2px 8px',
                      borderRadius: '4px',
                      background: '#EEEBFF',
                      color: '#8629FF',
                      fontSize: '11px',
                      fontWeight: '500',
                    }}>
                      From Chat
                    </span>
                  )}
                </div>

                {/* Content Preview */}
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
                  {note.content}
                </p>

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
                    {formatDate(note.timestamp)}
                  </span>
                  {note.tags && note.tags.length > 0 && (
                    <div style={{ display: 'flex', gap: '4px' }}>
                      {note.tags.slice(0, 2).map(tag => (
                        <span
                          key={tag}
                          style={{
                            padding: '2px 6px',
                            borderRadius: '4px',
                            background: '#F3F4F6',
                            color: '#6B7280',
                            fontSize: '11px',
                          }}
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Save from Chat Hint */}
      <div style={{
        padding: '12px 16px',
        background: '#F9FAFB',
        borderTop: '1px solid #E5E7EB',
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          fontSize: '12px',
          color: '#6B7280',
        }}>
          <span style={{ fontSize: '16px' }}>💡</span>
          <span>Tip: Click the save icon on chat messages to add them to notes</span>
        </div>
      </div>
    </div>
  );
};

export default NotesPanel;