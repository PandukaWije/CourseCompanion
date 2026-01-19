import React, { useEffect } from 'react';
import { useWidgetStore } from './store/widgetStore';
import FloatingButton from './components/FloatingButton';
import FloatingMenuPanel from './components/FloatingMenuPanel';
import WidgetPanel from './components/WidgetPanel';
import DiscoveryView from './components/DiscoveryView';
import SearchView from './components/SearchView';
import ChatView from './components/ChatView';
import ProfileView from './components/ProfileView';

/**
 * Main App Component
 * Orchestrates all widget components and manages the overall state
 */
function App({ config = {} }) {
  const { currentView, initWidget } = useWidgetStore();

  // Initialize widget with configuration
  useEffect(() => {
    initWidget(config);
    console.log('✅ CourseCompanion Widget initialized with config:', config);
  }, [config, initWidget]);

  // Render the appropriate view based on currentView
  const renderView = () => {
    switch (currentView) {
      case 'discovery':
        return <DiscoveryView />;
      case 'search':
        return <SearchView />;
      case 'chat':
        return <ChatView />;
      case 'profile':
        return <ProfileView />;
      default:
        return null;
    }
  };

  return (
    <div className="coursecompanion-widget">
      {/* Floating Button */}
      <FloatingButton />

      {/* Floating Menu Panel */}
      <FloatingMenuPanel />

      {/* Full Panel with Content */}
      <WidgetPanel>
        {renderView()}
      </WidgetPanel>
    </div>
  );
}

export default App;