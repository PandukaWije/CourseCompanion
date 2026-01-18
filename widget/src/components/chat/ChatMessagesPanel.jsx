import React, { useState, useEffect, useRef } from 'react';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';

/**
 * ChatMessagesPanel Component
 * Left panel containing chat messages and input section
 */
export const ChatMessagesPanel = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: 'Hello! I\'m your Course Companion. How can I help you today?',
      timestamp: new Date(),
    },
  ]);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = (content, tab) => {
    // Add user message
    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      content,
      timestamp: new Date(),
      tab,
    };
    setMessages([...messages, userMessage]);

    // Simulate bot response
    setTimeout(() => {
      const botMessage = {
        id: messages.length + 2,
        type: 'bot',
        content: `I received your message: "${content}". This is a placeholder response. In production, this will connect to the backend API.`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMessage]);
    }, 1000);
  };

  return (
    <div className="cc-chat-messages-panel">
      {/* Messages Area */}
      <div className="cc-messages-container">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Section */}
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatMessagesPanel;