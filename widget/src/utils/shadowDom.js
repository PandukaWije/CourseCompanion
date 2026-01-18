/**
 * Shadow DOM Injector
 * Handles the injection of the widget into the host page using Shadow DOM
 * This ensures complete style isolation from the host page
 */

export class WidgetInjector {
  constructor(config = {}) {
    this.config = config;
    this.container = null;
    this.shadowRoot = null;
  }

  /**
   * Inject the widget into the host page
   * @returns {ShadowRoot} The shadow root where React will render
   */
  inject() {
    try {
      // Create container element
      this.container = document.createElement('div');
      this.container.id = 'coursecompanion-widget-root';
      this.container.className = 'coursecompanion-widget';
      
      // Apply positioning styles to container
      this.container.style.position = 'fixed';
      this.container.style.zIndex = '9999';
      this.container.style.pointerEvents = 'none'; // Allow clicks to pass through
      
      // Attach Shadow DOM (mode: 'open' allows external access if needed)
      this.shadowRoot = this.container.attachShadow({ mode: 'open' });
      
      // Add container to page
      document.body.appendChild(this.container);
      
      console.log('✅ CourseCompanion Widget injected successfully');
      
      return this.shadowRoot;
    } catch (error) {
      console.error('❌ Failed to inject CourseCompanion Widget:', error);
      throw error;
    }
  }

  /**
   * Remove the widget from the page
   */
  destroy() {
    if (this.container && this.container.parentNode) {
      this.container.parentNode.removeChild(this.container);
      this.container = null;
      this.shadowRoot = null;
      console.log('✅ CourseCompanion Widget removed');
    }
  }

  /**
   * Check if widget is already injected
   * @returns {boolean}
   */
  isInjected() {
    return document.getElementById('coursecompanion-widget-root') !== null;
  }

  /**
   * Get the shadow root
   * @returns {ShadowRoot|null}
   */
  getShadowRoot() {
    return this.shadowRoot;
  }
}

/**
 * Utility function to check if Shadow DOM is supported
 * @returns {boolean}
 */
export function isShadowDOMSupported() {
  return !!document.body.attachShadow;
}

/**
 * Prevent event propagation outside shadow DOM
 * Useful for preventing clicks inside widget from affecting host page
 */
export function isolateEvent(event) {
  event.stopPropagation();
}