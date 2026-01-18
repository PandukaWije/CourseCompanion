/**
 * Style Injection Utility for Shadow DOM
 * Handles loading and injecting styles into the Shadow DOM
 */

/**
 * Inject CSS string into Shadow DOM
 * @param {ShadowRoot} shadowRoot - The shadow root to inject styles into
 * @param {string} cssText - CSS text to inject
 */
export function injectCSSText(shadowRoot, cssText) {
  const styleEl = document.createElement('style');
  styleEl.textContent = cssText;
  shadowRoot.appendChild(styleEl);
}

/**
 * Inject external stylesheet into Shadow DOM
 * @param {ShadowRoot} shadowRoot - The shadow root to inject styles into
 * @param {string} href - URL of the stylesheet
 */
export function injectStylesheet(shadowRoot, href) {
  const linkEl = document.createElement('link');
  linkEl.rel = 'stylesheet';
  linkEl.href = href;
  shadowRoot.appendChild(linkEl);
}

/**
 * Inject all widget styles into Shadow DOM
 * This function will inject the compiled CSS that includes Tailwind
 * @param {ShadowRoot} shadowRoot - The shadow root to inject styles into
 */
export async function injectWidgetStyles(shadowRoot) {
  try {
    // Inject Google Fonts
    injectStylesheet(
      shadowRoot,
      'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
    );
    
    console.log('✅ Styles injected into Shadow DOM');
  } catch (error) {
    console.error('❌ Failed to inject styles:', error);
  }
}