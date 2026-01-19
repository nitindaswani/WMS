/**
 * Component Loader
 * Handles dynamic fetching and injection of HTML components.
 */

class Components {
  static cache = new Map();

  /**
   * Load a component into a target element.
   * @param {string} targetId - The ID of the element to inject content into.
   * @param {string} url - The URL of the HTML component.
   * @param {Object} options - Optional settings (e.g., callback after load).
   */
  static async load(targetId, url, options = {}) {
    const target = document.getElementById(targetId);
    if (!target) {
      console.warn(`Target element #${targetId} not found for component ${url}`);
      return;
    }

    try {
      let content;
      if (this.cache.has(url)) {
        content = this.cache.get(url);
      } else {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Failed to load ${url}: ${response.status}`);
        content = await response.text();
        this.cache.set(url, content);
      }

      // Safe injection (basic prevention, but really we trust our own components)
      target.innerHTML = content;

      // Executescripts if present in the component (fetch/innerHTML doesn't run <script> tags by default)
      // For simple components, this is handled by the parent page, but valid to know.
      
      if (options.onLoad) {
        options.onLoad();
      }
      
      // Accessibility update
      target.setAttribute('data-loaded', 'true');
      
    } catch (error) {
      console.error(`Component Load Error (${url}):`, error);
      target.innerHTML = `<div class="component-error">Failed to load content.</div>`;
    }
  }

  /**
   * Load multiple components defined by data attributes.
   * Looks for elements with `data-component="url"`.
   */
  static async loadAll() {
    const elements = document.querySelectorAll('[data-component]');
    const promises = Array.from(elements).map(el => {
      const url = el.getAttribute('data-component');
      return this.load(el.id, url);
    });
    await Promise.all(promises);
  }
}

// Global export
window.Components = Components;
