import React from 'react';

/**
 * ToolButton Component
 * Reusable button for tools grid (Artifacts, Notes, Quiz, Mind Map)
 * 
 * @param {string} icon - Emoji or icon to display
 * @param {string} label - Button label text
 * @param {function} onClick - Click handler
 * @param {boolean} active - Whether button is active/selected
 */
export const ToolButton = ({ icon, label, onClick, active = false }) => {
  return (
    <button
      className={`cc-tool-button ${active ? 'active' : ''}`}
      onClick={onClick}
      aria-label={label}
    >
      <span className="cc-tool-label">{label}</span>
    </button>
  );
};

export default ToolButton;