import React, { useState } from 'react';
import { User, Save, Copy, Check } from 'lucide-react';

/**
 * ChatMessage Component
 * Displays a single chat message (bot or user) with action buttons
 * 
 * @param {object} message - Message object with type, content, timestamp
 * @param {function} onSaveToNotes - Callback to save message to notes
 */
export const ChatMessage = ({ message, onSaveToNotes }) => {
  const isBot = message.type === 'bot';
  const [showActions, setShowActions] = useState(false);
  const [copied, setCopied] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSave = () => {
    if (onSaveToNotes) {
      onSaveToNotes(message);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    }
  };

  return (
    <div
      className={`flex items-start gap-3 ${
        isBot ? '' : 'flex-row-reverse'
      }`}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
      style={{ position: 'relative' }}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isBot ? '' : 'bg-gray-200'
        }`}
        style={
          isBot
            ? { background: 'linear-gradient(135deg, #8629FF 0%, #FF1F38 100%)' }
            : {}
        }
      >
        {isBot ? (
          <img
            src="/svg/Logo Icon.svg"
            alt="Bot"
            style={{ width: '32px', height: '32px' }}
          />
        ) : (
          <User size={20} color="#6B7280" />
        )}
      </div>

      {/* Message Bubble */}
      <div
        className={`flex-1 !px-4 !py-3 rounded-lg max-w-[80%] ${
          isBot ? 'bg-gray-100' : ''
        }`}
        style={
          isBot
            ? {}
            : {
                background: 'var(--cc-secondary-bg)',
                color: 'black',
              }
        }
      >
        <p
          className="text-sm leading-relaxed"
          style={isBot ? { color: '#1F2937' } : { color: 'black' }}
        >
          {message.content}
        </p>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginTop: '8px'
        }}>
          <p
            className="text-xs"
            style={{ color: '#9CA3AF' }}
          >
            {message.timestamp.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>

          {/* Action Buttons - Only show for bot messages on hover */}
          {isBot && showActions && (
            <div style={{ 
              display: 'flex', 
              gap: '8px',
              opacity: showActions ? 1 : 0,
              transition: 'opacity 0.2s'
            }}>
              <button
                onClick={handleCopy}
                style={{
                  padding: '4px 8px',
                  borderRadius: '4px',
                  border: 'none',
                  background: copied ? '#DCFCE7' : 'transparent',
                  color: copied ? '#166534' : '#6B7280',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  fontSize: '11px',
                  fontWeight: '500',
                  transition: 'all 0.2s',
                }}
                title="Copy message"
              >
                {copied ? <Check size={12} /> : <Copy size={12} />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>
              <button
                onClick={handleSave}
                style={{
                  padding: '4px 8px',
                  borderRadius: '4px',
                  border: 'none',
                  background: saved ? '#DCFCE7' : 'transparent',
                  color: saved ? '#166534' : '#8629FF',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  fontSize: '11px',
                  fontWeight: '500',
                  transition: 'all 0.2s',
                }}
                title="Save to notes"
              >
                {saved ? <Check size={12} /> : <Save size={12} />}
                <span>{saved ? 'Saved' : 'Save'}</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;