import React, { useState } from 'react';
import { Send } from 'lucide-react';

/**
 * ChatInput Component
 * Input section with tabs (Action, Agents, Flows) and send button
 */
export const ChatInput = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');
  const [activeTab, setActiveTab] = useState('action');

  const tabs = [
    { id: 'action', label: 'Action' },
    { id: 'agents', label: 'Agents' },
    { id: 'flows', label: 'Flows' },
  ];

  const handleSend = () => {
    if (message.trim()) {
      onSendMessage?.(message, activeTab);
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="cc-chat-input-section">
      {/* Tabs */}
      <div className="cc-chat-tabs">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`cc-chat-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Input Field */}
      <div className="cc-input-wrapper">
        <input
          type="text"
          className="cc-chat-input"
          placeholder="Ask anything..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button
          className="cc-send-button"
          onClick={handleSend}
          disabled={!message.trim()}
          aria-label="Send message"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
};

export default ChatInput;