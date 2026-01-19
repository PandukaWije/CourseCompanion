import React, { useState } from "react";
import { ChatHeader } from "./ChatHeader";
import { ChatMessagesPanel } from "./ChatMessagesPanel";
import { ChatHistory } from "./ChatHistory";
import { ToolsPanel } from "./ToolsPanel";
import { useWidgetStore } from "../../store/widgetStore";
import { ArrowRight } from "lucide-react";

/**
 * ChatPageLayout Component
 * Layout: Chat (left) | Tools (right)
 * History appears inline in chat area when toggled
 */
export const ChatPageLayout = () => {
  const [showHistory, setShowHistory] = useState(false);
  const { selectedCourses, createNewChat, openChat, openPanel } = useWidgetStore();

  const handleToggleHistory = () => {
    setShowHistory(!showHistory);
  };

  const handleNewChat = () => {
    setShowHistory(false);
    createNewChat("New Chat");
  };

  const handleOpenChat = (chatId, courses) => {
    // If courses provided (from context switch), update selected courses
    if (courses) {
      useWidgetStore.getState().setSelectedCourses(courses);
    }

    // Close history and open chat
    setShowHistory(false);
    openChat(chatId);
  };

  const handleStartNewChat = (courses) => {
    setShowHistory(false);
    createNewChat("New Chat");
  };

  // Handle no selected courses - redirect to discovery
  const handleNoCourses = () => {
    openPanel('discovery');
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        width: "100%",
      }}
    >
      {/* Header: Chat (left)  + Buttons | Course Companion (right) */}
      <ChatHeader
        onToggleHistory={handleToggleHistory}
        onNewChat={handleNewChat}
        selectedCourses={selectedCourses}
        showNewChatHistory={selectedCourses && selectedCourses.length > 0}
      />

      {/* If no course selected Direct them to course discovery */}
      {selectedCourses && selectedCourses.length > 0 ? (
        <>
          {/* Two-Panel Layout: Chat (left) | Tools (right) */}
          <div
            style={{
              display: "flex",
              flex: 1,
              overflow: "hidden",
            }}
          >
            {/* LEFT PANEL - Chat Area */}
            <div
              style={{
                flex: "1 1 60%",
                display: "flex",
                flexDirection: "column",
                borderRight: "1px solid #E5E7EB",
                overflow: "hidden",
                background: "#FFFFFF",
              }}
            >
              {showHistory ? (
                <ChatHistory
                  selectedCourses={selectedCourses}
                  onOpenChat={handleOpenChat}
                  onStartNewChat={handleStartNewChat}
                  onBack={handleToggleHistory}
                />
              ) : (
                <ChatMessagesPanel />
              )}
            </div>

            {/* RIGHT PANEL - Tools (with scrolling + expand) */}
            <div
              style={{
                flex: "1 1 40%",
                display: "flex",
                flexDirection: "column",
                overflow: "auto",
                background: "#F9FAFB",
              }}
            >
              <ToolsPanel />
            </div>
          </div>
        </>
      ) : (
        <>
          {/* No course selected direct them to course discovery */}
          <div 
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              height: "100%",
              padding: "40px 20px",
              gap: "20px",
            }}
          >
            <div 
              style={{
                textAlign: "center",
                maxWidth: "500px",
              }}
            >
              <h3 
                style={{
                  fontSize: "20px",
                  fontWeight: "600",
                  color: "#111827",
                  marginBottom: "12px",
                }}
              >
                No Course Selected
              </h3>
              <p 
                style={{
                  fontSize: "14px",
                  color: "#6B7280",
                  marginBottom: "24px",
                }}
              >
                To start chatting with your AI companion, please select a course from the course discovery page.
              </p>
              <button
                onClick={handleNoCourses}
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "8px",
                  padding: "12px 24px",
                  background: "linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)",
                  color: "#FFFFFF",
                  border: "none",
                  borderRadius: "8px",
                  fontSize: "14px",
                  fontWeight: "500",
                  cursor: "pointer",
                  transition: "all 0.2s",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-2px)";
                  e.currentTarget.style.boxShadow = "0 4px 12px rgba(134, 41, 255, 0.3)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow = "none";
                }}
              >
                <span>Go to Course Discovery</span>
                <ArrowRight size={18} />
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ChatPageLayout;