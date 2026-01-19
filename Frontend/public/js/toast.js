/**
 * Toast Notification System
 * Displays floating alerts to the user.
 * Requires: toast.css
 */

class Toast {
    static container = null;

    /**
     * Initialize container if needed
     */
    static init() {
        if (!document.querySelector('.toast-container')) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        } else {
            this.container = document.querySelector('.toast-container');
        }
    }

    /**
     * Show a toast message
     * @param {string} message - The body text
     * @param {string} type - 'success', 'error', 'info', 'warning'
     * @param {string} title - Optional bold title
     * @param {number} duration - ms to show (default 4000)
     */
    static show(message, type = 'info', title = '', duration = 4000) {
        this.init();

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;

        // Icons mapping
        const icons = {
            success: '✓',
            error: '✕',
            info: 'ℹ',
            warning: '⚠'
        };

        toast.innerHTML = `
            <div class="toast-icon">${icons[type]}</div>
            <div class="toast-content">
                ${title ? `<div class="toast-title">${title}</div>` : ''}
                <div class="toast-message">${message}</div>
            </div>
        `;

        this.container.appendChild(toast);

        // Auto remove
        setTimeout(() => {
            this.remove(toast);
        }, duration);

        // Click to remove
        toast.onclick = () => this.remove(toast);
    }

    static remove(el) {
        el.classList.add('hiding');
        el.addEventListener('animationend', () => {
            if (el.parentElement) el.remove();
        });
    }

    // Convenience methods
    static success(msg, title = 'Success') { this.show(msg, 'success', title); }
    static error(msg, title = 'Error') { this.show(msg, 'error', title); }
    static warning(msg, title = 'Warning') { this.show(msg, 'warning', title); }
    static info(msg, title = 'Info') { this.show(msg, 'info', title); }
}

// Global Export
window.Toast = Toast;
