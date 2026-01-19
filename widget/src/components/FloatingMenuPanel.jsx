import React from 'react';
import { useWidgetStore } from '../store/widgetStore';

/**
 * Custom Icon Components using SVGs with proper fill colors
 */
const DiscoveryIcon = ({ isActive }) => (
    <svg 
    xmlns="http://www.w3.org/2000/svg" 
    height="24px" 
    viewBox="0 -960 960 960" 
    width="24px" 
    fill={isActive ? '#000000' : '#FFFFFF'}
  >
    <path d="M784-120 532-372q-30 24-69 38t-83 14q-109 0-184.5-75.5T120-580q0-109 75.5-184.5T380-840q109 0 184.5 75.5T640-580q0 44-14 83t-38 69l252 252-56 56ZM380-400q75 0 127.5-52.5T560-580q0-75-52.5-127.5T380-760q-75 0-127.5 52.5T200-580q0 75 52.5 127.5T380-400Z"/>
  </svg>

);

const ProfileIcon = ({ isActive }) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    height="24px" 
    viewBox="0 -960 960 960" 
    width="24px" 
    fill={isActive ? '#000000' : '#FFFFFF'}
  >
    <path 
    d="M680-360q-42 0-71-29t-29-71q0-42 29-71t71-29q42 0 71 29t29 71q0 42-29 71t-71 29ZM480-160v-56q0-24 12.5-44.5T528-290q36-15 74.5-22.5T680-320q39 0 77.5 7.5T832-290q23 9 35.5 29.5T880-216v56H480Zm-80-320q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47Zm0-160ZM80-160v-112q0-34 17-62.5t47-43.5q60-30 124.5-46T400-440q35 0 70 6t70 14l-34 34-34 34q-18-5-36-6.5t-36-1.5q-58 0-113.5 14T180-306q-10 5-15 14t-5 20v32h240v80H80Zm320-80Zm0-320q33 0 56.5-23.5T480-640q0-33-23.5-56.5T400-720q-33 0-56.5 23.5T320-640q0 33 23.5 56.5T400-560Z"
    fill={isActive ? '#000000' : '#FFFFFF'}
    />
  </svg>
);

const ChatIcon = ({ isActive }) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    width="22" 
    height="22" 
    viewBox="0 0 22 22" 
    fill="none"
  >
    <path 
      d="M17.4168 15.5833L19.8616 16.5L17.4168 17.4167L16.5002 19.8614L15.5835 17.4167L13.1387 16.5L15.5835 15.5833L16.5002 13.1386L17.4168 15.5833ZM11.0002 2.75C16.0418 2.75 20.1668 6.03167 20.1668 10.0833C20.1668 10.7858 20.0401 11.4642 19.8088 12.1073C19.3179 11.737 18.7637 11.4461 18.1643 11.256C18.274 10.8779 18.3335 10.4859 18.3335 10.0833C18.3335 7.04917 15.0518 4.58333 11.0002 4.58333C6.9485 4.58333 3.66683 7.04917 3.66683 10.0833C3.66683 13.1175 6.9485 15.5833 11.0002 15.5833C11.0262 15.5833 11.0521 15.5818 11.0781 15.5815C11.0278 15.8803 11.0002 16.187 11.0002 16.5C11.0002 16.8118 11.0273 17.1173 11.0772 17.4148C11.0515 17.415 11.0258 17.4167 11.0002 17.4167C9.90933 17.4167 8.80908 17.2608 7.76408 16.9583C6.0866 18.3332 4.00593 19.1492 1.8335 19.25C3.96933 17.1142 4.35433 15.675 4.35433 15.125C2.80516 13.9058 1.87933 12.0542 1.8335 10.0833C1.8335 6.03167 5.9585 2.75 11.0002 2.75Z" 
      fill={isActive ? '#000000' : '#FFFFFF'}
    />
  </svg>
);

/**
 * FloatingMenuPanel Component
 * The horizontal icon menu that appears when the button is clicked
 */
export const FloatingMenuPanel = () => {
  const { isMenuOpen, activeIcon, openPanel } = useWidgetStore();

  if (!isMenuOpen) return null;

  const menuIcons = [
    {
      id: 'Profile',
      icon: ProfileIcon,
      label: 'View Profile',
      view: 'profile',
    },
    {
      id: 'discovery',
      icon: DiscoveryIcon,
      label: 'Course Discovery',
      view: 'discovery',
    },
    {
      id: 'chat',
      icon: ChatIcon,
      label: 'Chat',
      view: 'chat',
    },
  ];

  const handleIconClick = (view) => {
    openPanel(view);
  };

  return (
    <div 
      className="cc-floating-menu"
      style={{ pointerEvents: 'auto' }} // Enable clicks
    >
      {menuIcons.map(({ id, icon: Icon, label, view }) => (
        <button
          key={id}
          className={`cc-menu-icon-button ${activeIcon === id ? 'active' : ''}`}
          onClick={() => handleIconClick(view)}
          aria-label={label}
          title={label}
        >
          <Icon isActive={activeIcon === id} />
        </button>
      ))}
    </div>
  );
};

export default FloatingMenuPanel;