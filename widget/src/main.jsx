import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { WidgetInjector, isShadowDOMSupported } from './utils/shadowDom';
import { injectWidgetStyles } from './utils/styleInjector';
import './styles/widget.css'; // CRITICAL: Import Tailwind CSS

/**
 * CourseCompanion Widget Main Entry Point
 * Handles injection, initialization, and global API exposure
 */
class CourseCompanionWidget {
  constructor() {
    this.injector = null;
    this.root = null;
    this.config = null;
  }

  /**
   * Initialize the widget
   * @param {Object} config - Configuration options
   * @param {string} config.userId - User ID for personalization
   * @param {string} config.apiUrl - Backend API URL
   * @param {string} config.theme - Theme (light/dark)
   * @param {string} config.position - Position (bottom-right/bottom-left/top-right/top-left)
   */
  async init(config = {}) {
    // Check if already initialized
    if (this.root) {
      console.warn('⚠️ CourseCompanion Widget is already initialized');
      return;
    }

    // Check Shadow DOM support
    if (!isShadowDOMSupported()) {
      console.error('❌ Shadow DOM is not supported in this browser');
      return;
    }

    try {
      // Store configuration
      this.config = {
        userId: config.userId || null,
        apiUrl: config.apiUrl || 'http://localhost:8000',
        theme: config.theme || 'light',
        position: config.position || 'bottom-right',
        ...config,
      };

      console.log('🚀 Initializing CourseCompanion Widget...');
      console.log('📋 Configuration:', this.config);

      // Create and inject Shadow DOM
      this.injector = new WidgetInjector(this.config);
      const shadowRoot = this.injector.inject();

      // Inject styles into Shadow DOM (fonts, etc.)
      await injectWidgetStyles(shadowRoot);

      // CRITICAL: For development, inject the compiled Tailwind styles into shadow DOM
      if (import.meta.env.DEV) {
        // Small delay to ensure Vite has injected the styles
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Get all style elements from document head (Vite dev styles)
        const styles = Array.from(document.querySelectorAll('style[data-vite-dev-id]'));
        styles.forEach(style => {
          const clonedStyle = style.cloneNode(true);
          shadowRoot.appendChild(clonedStyle);
        });
        
        console.log(`✅ Cloned ${styles.length} dev style(s) into shadow DOM`);
      }

      // Create a div inside shadow root for React to mount
      const reactRoot = document.createElement('div');
      reactRoot.id = 'coursecompanion-react-root';
      reactRoot.className = 'coursecompanion-widget';
      shadowRoot.appendChild(reactRoot);

      // Create React root and render
      this.root = ReactDOM.createRoot(reactRoot);
      this.root.render(
        <React.StrictMode>
          <App config={this.config} />
        </React.StrictMode>
      );

      console.log('✅ CourseCompanion Widget initialized successfully!');
      console.log('💡 User ID:', this.config.userId || 'Not set');
      console.log('🔗 API URL:', this.config.apiUrl);
    } catch (error) {
      console.error('❌ Failed to initialize CourseCompanion Widget:', error);
    }
  }

  /**
   * Destroy the widget and clean up
   */
  destroy() {
    if (this.root) {
      this.root.unmount();
      this.root = null;
    }

    if (this.injector) {
      this.injector.destroy();
      this.injector = null;
    }

    this.config = null;
    console.log('✅ CourseCompanion Widget destroyed');
  }

  /**
   * Update widget configuration
   * @param {Object} newConfig - New configuration to merge
   */
  updateConfig(newConfig) {
    if (!this.root) {
      console.warn('⚠️ Widget is not initialized. Call init() first.');
      return;
    }

    this.config = { ...this.config, ...newConfig };
    console.log('✅ Configuration updated:', this.config);

    // Re-render with new config
    const reactRoot = this.injector.getShadowRoot().getElementById('coursecompanion-react-root');
    if (reactRoot) {
      this.root.render(
        <React.StrictMode>
          <App config={this.config} />
        </React.StrictMode>
      );
    }
  }

  /**
   * Get current configuration
   * @returns {Object} Current configuration
   */
  getConfig() {
    return this.config ? { ...this.config } : null;
  }

  /**
   * Check if widget is initialized
   * @returns {boolean}
   */
  isInitialized() {
    return this.root !== null;
  }
}

// Create singleton instance
const widgetInstance = new CourseCompanionWidget();

// Expose to global window object
window.CourseCompanion = widgetInstance;

// For development: Auto-initialize if config is provided
if (import.meta.env.DEV) {
  console.log('🔧 Development mode detected');
  
  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      widgetInstance.init({
        userId: 'dev-user-123',
        apiUrl: 'http://localhost:8000',
        theme: 'light',
        position: 'bottom-right',
      });
    });
  } else {
    widgetInstance.init({
      userId: 'dev-user-123',
      apiUrl: 'http://localhost:8000',
      theme: 'light',
      position: 'bottom-right',
    });
  }
}

export default widgetInstance;