import React from 'react';
import { X } from 'lucide-react';
import { useWidgetStore } from '../store/widgetStore';

/**
 * LogoIcon Component - Brand logo with sparkles
 */
const LogoIcon = () => (
  <img 
    src="/svg/Logo Icon.svg" 
    alt="CourseCompanion" 
    style={{ width: '60px', height: '60px' }}
  />
);

/**
 * FloatingButton Component
 * The initial circular gradient button that opens the menu
 */
export const FloatingButton = () => {
  const { isButtonVisible, isMenuOpen, toggleMenu } = useWidgetStore();

  if (!isButtonVisible) return null;

  return (
    <button
      className="cc-floating-button"
      onClick={toggleMenu}
      aria-label={isMenuOpen ? 'Close menu' : 'Open menu'}
      style={{ pointerEvents: 'auto' }} // Enable clicks on this element
    >
      {isMenuOpen ? (
        <X size={28} strokeWidth={2.5} color="white" />
      ) : (
        <LogoIcon />
      )}
    </button>
  );
};

export default FloatingButton;