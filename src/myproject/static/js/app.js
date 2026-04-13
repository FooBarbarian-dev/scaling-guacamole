/**
 * HTMX initialization and theme toggle logic.
 */
(function () {
    "use strict";

    // Theme management
    const THEME_KEY = "theme";
    const VALID_THEMES = ["light", "dark", "colorblind"];

    function getStoredTheme() {
        const stored = localStorage.getItem(THEME_KEY);
        return VALID_THEMES.includes(stored) ? stored : "light";
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem(THEME_KEY, theme);

        // Update toggle button active state
        document.querySelectorAll(".theme-toggle-btn").forEach(function (btn) {
            btn.classList.toggle("active", btn.dataset.theme === theme);
        });
    }

    // Apply stored theme immediately on load
    applyTheme(getStoredTheme());

    document.addEventListener("DOMContentLoaded", function () {
        // Theme toggle — 3-way button group
        document.querySelectorAll(".theme-toggle-btn").forEach(function (btn) {
            btn.addEventListener("click", function () {
                applyTheme(this.dataset.theme);
            });
        });
        // Set initial active state
        applyTheme(getStoredTheme());

        // HTMX configuration
        if (typeof htmx !== "undefined") {
            // Include CSRF token in HTMX requests
            document.body.addEventListener("htmx:configRequest", function (event) {
                const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
                if (csrfToken) {
                    event.detail.headers["X-CSRFToken"] = csrfToken.value;
                }
            });
        }
    });
})();
