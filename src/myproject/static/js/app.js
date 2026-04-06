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

        // Update select if it exists
        const select = document.getElementById("theme-select");
        if (select) {
            select.value = theme;
        }
    }

    // Apply stored theme immediately on load
    applyTheme(getStoredTheme());

    document.addEventListener("DOMContentLoaded", function () {
        // Theme toggle
        const themeSelect = document.getElementById("theme-select");
        if (themeSelect) {
            themeSelect.value = getStoredTheme();
            themeSelect.addEventListener("change", function () {
                applyTheme(this.value);
            });
        }

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
