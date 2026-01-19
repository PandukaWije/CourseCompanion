import React from "react";
import { History, MessageSquarePlus } from "lucide-react";

/**
 * ChatHeader Component
 * LEFT: Chat title  + History + New Chat buttons
 * RIGHT: Course Companion
 */
export const ChatHeader = ({
  onToggleHistory,
  onNewChat,
  selectedCourses,
  showNewChatHistory,
}) => {
  return (
    <div className="cc-chat-header">
      {/* LEFT SIDE - Chat Title */}
      <div className="cc-chat-header-left">
        <span className="cc-chat-title">Chat</span>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="22"
          height="22"
          viewBox="0 0 22 22"
          fill="#374151"
        >
          <path d="M17.4168 15.5833L19.8616 16.5L17.4168 17.4167L16.5002 19.8614L15.5835 17.4167L13.1387 16.5L15.5835 15.5833L16.5002 13.1386L17.4168 15.5833ZM11.0002 2.75C16.0418 2.75 20.1668 6.03167 20.1668 10.0833C20.1668 10.7858 20.0401 11.4642 19.8088 12.1073C19.3179 11.737 18.7637 11.4461 18.1643 11.256C18.274 10.8779 18.3335 10.4859 18.3335 10.0833C18.3335 7.04917 15.0518 4.58333 11.0002 4.58333C6.9485 4.58333 3.66683 7.04917 3.66683 10.0833C3.66683 13.1175 6.9485 15.5833 11.0002 15.5833C11.0262 15.5833 11.0521 15.5818 11.0781 15.5815C11.0278 15.8803 11.0002 16.187 11.0002 16.5C11.0002 16.8118 11.0273 17.1173 11.0772 17.4148C11.0515 17.415 11.0258 17.4167 11.0002 17.4167C9.90933 17.4167 8.80908 17.2608 7.76408 16.9583C6.0866 18.3332 4.00593 19.1492 1.8335 19.25C3.96933 17.1142 4.35433 15.675 4.35433 15.125C2.80516 13.9058 1.87933 12.0542 1.8335 10.0833C1.8335 6.03167 5.9585 2.75 11.0002 2.75Z" />
        </svg>
        {selectedCourses && selectedCourses.length > 0 && (
          <p style={{ fontSize: "13px", color: "#6B7280" }}>
            {selectedCourses.map((c) => c.name).join(", ")}
          </p>
        )}
        {/* Conditional Display - History + New Chat Buttons */}
        {showNewChatHistory && (
          <>
            {/* Divider */}
            <div
              style={{
                width: "1px",
                height: "30px",
                background: "#E5E7EB",
              }}
            />

            {/* Action Buttons */}
            <div style={{ display: "flex", gap: "12px" }}>
              {/* History Button */}
              <button
                onClick={onToggleHistory}
                style={{
                  padding: "8px 16px",
                  borderRadius: "8px",
                  border: "1px solid #E5E7EB",
                  background: "#FFFFFF",
                  color: "#6B7280",
                  fontSize: "14px",
                  fontWeight: "500",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  transition: "all 0.2s",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = "#F9FAFB";
                  e.currentTarget.style.borderColor = "#8629FF";
                  e.currentTarget.style.color = "#8629FF";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = "#FFFFFF";
                  e.currentTarget.style.borderColor = "#E5E7EB";
                  e.currentTarget.style.color = "#6B7280";
                }}
              >
                <History size={16} />
                <span>History</span>
              </button>

              {/* New Chat Button */}
              <button
                onClick={onNewChat}
                style={{
                  padding: "8px 16px",
                  borderRadius: "8px",
                  border: "none",
                  background:
                    "linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)",
                  color: "#FFFFFF",
                  fontSize: "14px",
                  fontWeight: "500",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  transition: "all 0.2s",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-1px)";
                  e.currentTarget.style.boxShadow =
                    "0 4px 12px rgba(134, 41, 255, 0.3)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow = "none";
                }}
              >
                <MessageSquarePlus size={16} />
                <span>New Chat</span>
              </button>
            </div>
          </>
        )}
      </div>

      {/* RIGHT SIDE - Course Companion Label + Buttons */}
      <div className="cc-chat-header-right">
        <span className="cc-companion-title">Course Companion</span>
      </div>
    </div>
  );
};

export default ChatHeader;
