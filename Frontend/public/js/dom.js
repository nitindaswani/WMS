/**
 * Component Loader
 * Fetches HTML fragments and injects them into specific DOM elements.
 */



// Security Utility
window.escapeHTML = function (str) {
    if (!str) return '';
    return str.toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
};

async function loadComponent(elementId, componentPath) {
    const element = document.getElementById(elementId);
    if (!element) return;

    try {
        const response = await fetch(componentPath);
        if (!response.ok) throw new Error(`Failed to load ${componentPath}`);
        const html = await response.text();
        element.innerHTML = html;

        // Execute any scripts found in the injected HTML (security warning: trusted content only)
        const scripts = element.querySelectorAll("script");
        scripts.forEach(oldScript => {
            const newScript = document.createElement("script");
            Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
            newScript.appendChild(document.createTextNode(oldScript.innerHTML));
            oldScript.parentNode.replaceChild(newScript, oldScript);
        });

    } catch (error) {
        console.error("Error loading component:", error);
        element.innerHTML = `<div style="color: red; padding: 10px;">Error loading ${componentPath}</div>`;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // Auto-load standard components if placeholders exist
    // Auto-load components based on path
    const isAdmin = window.location.pathname.includes('/admin/');
    const isUser = window.location.pathname.includes('/user/');

    // Sidebar
    if (isAdmin) {
        loadComponent("sidebar", "/components/sidebar-admin.html");
    } else if (isUser) {
        if (Auth.getRole() === 'speaker') {
            loadComponent("sidebar", "/components/sidebar-speaker.html");
        } else {
            loadComponent("sidebar", "/components/user-sidebar.html");
        }
    } else {
        loadComponent("sidebar", "/components/sidebar.html");
    }

    // Navbar
    if (isAdmin) {
        loadComponent("navbar", "/components/admin-navbar.html");
    } else if (isUser) {
        loadComponent("navbar", "/components/user-navbar.html");
    } else {
        loadComponent("navbar", "/components/navbar.html");
    }
    loadComponent("footer", "/components/footer.html");

    // Highlight active sidebar link
    setTimeout(() => {
        const currentPath = window.location.pathname;
        const links = document.querySelectorAll('.nav-link');
        links.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }, 100); // Small delay to wait for fetch
});

