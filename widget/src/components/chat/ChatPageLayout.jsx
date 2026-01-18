import React from 'react';
import { ChatHeader } from './ChatHeader';
import { ChatMessagesPanel } from './ChatMessagesPanel';
import { ToolsPanel } from './ToolsPanel';

/**
 * ChatPageLayout Component
 * Main layout component for the chat page with two-panel design
 * Left: Chat messages and input
 * Right: Tools (Artifacts, Notes, Quiz, Mind Map)
 */
export const ChatPageLayout = () => {
  return (
    <>
      {/* Header */}
      <ChatHeader />

      {/* Two-Panel Layout */}
      <div className="cc-chat-layout">
        {/* Left Panel - Chat */}
        <ChatMessagesPanel />

        {/* Right Panel - Tools */}
        <ToolsPanel />
      </div>
    </>
  );
};

export default ChatPageLayout;